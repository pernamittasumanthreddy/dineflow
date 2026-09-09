from decimal import Decimal
from django.db import transaction
from django.utils import timezone
from apps.inventory.models import (
    Stock, StockBatch, StockMovement, StockAdjustment,
    WasteRecord, InventoryAlert, InventoryItem
)
from apps.purchases.models import GoodsReceipt
from apps.orders.models import Order
from apps.audit.models import AuditLog


class InventoryService:
    @classmethod
    @transaction.atomic
    def process_goods_receipt(cls, grn: GoodsReceipt, user=None):
        """
        Atomically inward goods from GoodsReceipt (GRN), creating or updating batches,
        adjusting branch stock levels, and creating immutable StockMovement ledger entries.
        """
        if grn.status == 'VERIFIED':
            return grn

        branch = grn.branch
        po = grn.purchase_order

        for item in grn.items.select_related('inventory_item', 'po_item').all():
            accepted_qty = item.quantity_accepted
            if accepted_qty <= Decimal('0.000'):
                continue

            inv_item = item.inventory_item

            # Lock stock record
            stock_obj, _ = Stock.objects.select_for_update().get_or_create(
                branch=branch,
                inventory_item=inv_item,
                defaults={
                    'quantity_on_hand': Decimal('0.000'),
                    'reserved_quantity': Decimal('0.000'),
                    'available_quantity': Decimal('0.000'),
                }
            )

            bal_before = stock_obj.quantity_on_hand
            bal_after = bal_before + accepted_qty

            stock_obj.quantity_on_hand = bal_after
            stock_obj.available_quantity = stock_obj.available_quantity + accepted_qty
            stock_obj.last_stock_take_date = timezone.now()
            stock_obj.save()

            # Create or update Stock Batch
            batch_num = item.batch_number or f"BATCH-{grn.grn_number}-{inv_item.item_code}"
            batch_obj = StockBatch.objects.create(
                branch=branch,
                inventory_item=inv_item,
                batch_number=batch_num,
                received_date=grn.received_date,
                expiry_date=item.expiry_date,
                purchase_unit_price=item.unit_price,
                initial_quantity=accepted_qty,
                remaining_quantity=accepted_qty,
            )

            # Record Traceable Stock Movement
            StockMovement.objects.create(
                branch=branch,
                inventory_item=inv_item,
                batch=batch_obj,
                movement_type='PURCHASE_RECEIPT',
                quantity=accepted_qty,
                balance_before=bal_before,
                balance_after=bal_after,
                reference_id=f"GRN #{grn.grn_number}",
                created_by=user,
                notes=f"Received from {grn.supplier.name} via GRN #{grn.grn_number}"
            )

            # Update PO item received quantity if linked
            if item.po_item:
                po_item = item.po_item
                po_item.quantity_received += accepted_qty
                po_item.save(update_fields=['quantity_received'])

            # If stock was low and is now above reorder level, resolve alerts
            if bal_after >= inv_item.reorder_level:
                InventoryAlert.objects.filter(
                    branch=branch,
                    inventory_item=inv_item,
                    alert_type__in=['LOW_STOCK', 'OUT_OF_STOCK'],
                    is_resolved=False
                ).update(is_resolved=True, resolved_at=timezone.now())

        # Update GRN status
        grn.status = 'VERIFIED'
        grn.save(update_fields=['status', 'updated_at'])

        # Update PO status if all items received
        if po:
            all_received = all(
                pi.quantity_received >= pi.quantity_ordered for pi in po.items.all()
            )
            po.status = 'COMPLETED' if all_received else 'PARTIALLY_RECEIVED'
            po.save(update_fields=['status', 'updated_at'])

        AuditLog.objects.create(
            action='INVENTORY_ADJUSTMENT',
            model_name='GoodsReceipt',
            object_id=str(grn.id),
            object_repr=str(grn),
            user=user,
            branch=branch,
            changes={'status': ['PENDING_INSPECTION', 'VERIFIED']}
        )

        return grn

    @classmethod
    @transaction.atomic
    def consume_recipe_ingredients_for_order(cls, order: Order, user=None):
        """
        Deducts raw food ingredients from branch inventory according to the Bill of Materials (BOM)
        recipes of ordered menu items. Records traceable StockMovement for every deduction.
        """
        branch = order.branch

        for order_item in order.items.select_related('menu_item').all():
            menu_item = order_item.menu_item
            order_qty = Decimal(str(order_item.quantity))

            if not hasattr(menu_item, 'recipe') or not menu_item.recipe:
                continue

            recipe = menu_item.recipe
            for food_ing in recipe.ingredients.select_related('inventory_item').all():
                inv_item = food_ing.inventory_item
                needed_qty = (food_ing.quantity_required * order_qty).quantize(Decimal('0.001'))

                # Lock stock record
                stock_obj, _ = Stock.objects.select_for_update().get_or_create(
                    branch=branch,
                    inventory_item=inv_item,
                    defaults={
                        'quantity_on_hand': Decimal('0.000'),
                        'reserved_quantity': Decimal('0.000'),
                        'available_quantity': Decimal('0.000'),
                    }
                )

                bal_before = stock_obj.quantity_on_hand
                bal_after = max(Decimal('0.000'), bal_before - needed_qty)

                stock_obj.quantity_on_hand = bal_after
                stock_obj.available_quantity = max(Decimal('0.000'), stock_obj.available_quantity - needed_qty)
                stock_obj.save(update_fields=['quantity_on_hand', 'available_quantity', 'updated_at'])

                # Record Stock Movement
                StockMovement.objects.create(
                    branch=branch,
                    inventory_item=inv_item,
                    movement_type='RECIPE_CONSUMPTION',
                    quantity=-needed_qty,
                    balance_before=bal_before,
                    balance_after=bal_after,
                    reference_id=f"ORDER #{order.order_number}",
                    created_by=user,
                    notes=f"Recipe consumption for {order_item.quantity}x {menu_item.name}"
                )

                # Check low stock alert
                if bal_after <= inv_item.reorder_level:
                    alert_type = 'OUT_OF_STOCK' if bal_after == 0 else 'LOW_STOCK'
                    InventoryAlert.objects.get_or_create(
                        branch=branch,
                        inventory_item=inv_item,
                        alert_type=alert_type,
                        is_resolved=False,
                        defaults={
                            'message': f"Stock level for {inv_item.name} is {bal_after} {inv_item.primary_unit.symbol}, at or below reorder level {inv_item.reorder_level}."
                        }
                    )

    @classmethod
    @transaction.atomic
    def adjust_stock(
        cls,
        branch,
        inventory_item: InventoryItem,
        adjustment_type: str,  # 'INCREASE' or 'DECREASE'
        quantity: Decimal,
        reason: str,
        cost_impact: Decimal = Decimal('0.00'),
        user=None
    ) -> StockAdjustment:
        """
        Manually adjust stock with variance tracking, manager sign-off, and movement logging.
        """
        stock_obj, _ = Stock.objects.select_for_update().get_or_create(
            branch=branch,
            inventory_item=inventory_item,
            defaults={
                'quantity_on_hand': Decimal('0.000'),
                'reserved_quantity': Decimal('0.000'),
                'available_quantity': Decimal('0.000'),
            }
        )

        bal_before = stock_obj.quantity_on_hand
        if adjustment_type == 'INCREASE':
            bal_after = bal_before + quantity
            movement_type = 'ADJUSTMENT_ADD'
            delta_qty = quantity
        else:
            bal_after = max(Decimal('0.000'), bal_before - quantity)
            movement_type = 'ADJUSTMENT_SUB'
            delta_qty = -quantity

        stock_obj.quantity_on_hand = bal_after
        stock_obj.available_quantity = bal_after
        stock_obj.save(update_fields=['quantity_on_hand', 'available_quantity', 'updated_at'])

        adj = StockAdjustment.objects.create(
            branch=branch,
            inventory_item=inventory_item,
            adjustment_type=adjustment_type,
            quantity=quantity,
            reason=reason,
            cost_impact=cost_impact,
            approved_by=user,
        )

        StockMovement.objects.create(
            branch=branch,
            inventory_item=inventory_item,
            movement_type=movement_type,
            quantity=delta_qty,
            balance_before=bal_before,
            balance_after=bal_after,
            reference_id=f"ADJ #{adj.id}",
            created_by=user,
            notes=f"Stock adjustment: {reason}"
        )

        AuditLog.objects.create(
            action='INVENTORY_ADJUSTMENT',
            model_name='StockAdjustment',
            object_id=str(adj.id),
            object_repr=str(adj),
            user=user,
            branch=branch,
            changes={'quantity': [str(bal_before), str(bal_after)]}
        )

        return adj

    @classmethod
    @transaction.atomic
    def record_kitchen_waste(
        cls,
        branch,
        inventory_item: InventoryItem,
        quantity: Decimal,
        reason: str,
        cost_impact: Decimal,
        user=None
    ) -> WasteRecord:
        """
        Records kitchen spoilage or preparation waste, deducting stock and creating movement logs.
        """
        stock_obj, _ = Stock.objects.select_for_update().get_or_create(
            branch=branch,
            inventory_item=inventory_item,
            defaults={
                'quantity_on_hand': Decimal('0.000'),
                'reserved_quantity': Decimal('0.000'),
                'available_quantity': Decimal('0.000'),
            }
        )

        bal_before = stock_obj.quantity_on_hand
        bal_after = max(Decimal('0.000'), bal_before - quantity)

        stock_obj.quantity_on_hand = bal_after
        stock_obj.available_quantity = max(Decimal('0.000'), stock_obj.available_quantity - quantity)
        stock_obj.save(update_fields=['quantity_on_hand', 'available_quantity', 'updated_at'])

        waste = WasteRecord.objects.create(
            branch=branch,
            inventory_item=inventory_item,
            quantity=quantity,
            reason=reason,
            cost_impact=cost_impact,
            recorded_by=user,
        )

        StockMovement.objects.create(
            branch=branch,
            inventory_item=inventory_item,
            movement_type='WASTAGE',
            quantity=-quantity,
            balance_before=bal_before,
            balance_after=bal_after,
            reference_id=f"WASTE #{waste.id}",
            created_by=user,
            notes=f"Kitchen wastage: {reason}"
        )

        return waste

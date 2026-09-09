"""Internal Notification Engine & In-App Alert Broadcast Services."""
from apps.notifications.models import Notification, NotificationType

def send_low_stock_notification(ingredient, recipient=None):
    """
    Emits a low-stock alert when an ingredient falls below minimum stock level.
    """
    title = f"Low Stock: {ingredient.name}"
    msg = f"Stock level for {ingredient.name} is {ingredient.current_stock} {ingredient.unit} (Reorder threshold: {ingredient.minimum_stock_level} {ingredient.unit})."
    return Notification.objects.create(
        recipient=recipient,
        title=title,
        message=msg,
        notification_type=NotificationType.LOW_STOCK,
        url="/inventory/"
    )

def send_new_order_notification(order, recipient=None):
    """
    Emits an operational notification to kitchen and cashiers for new dining orders.
    """
    table_str = f"Table {order.table.table_number}" if order.table else "Counter / Takeaway"
    title = f"New Order #{order.order_number}"
    msg = f"Order #{order.order_number} received for {table_str} ({order.guest_count} guests) - ₹{order.grand_total}."
    return Notification.objects.create(
        recipient=recipient,
        title=title,
        message=msg,
        notification_type=NotificationType.NEW_ORDER,
        url="/kitchen/"
    )

def send_payment_received_notification(payment, recipient=None):
    """
    Emits a payment settlement notification.
    """
    title = f"Payment Settled: ₹{payment.amount}"
    msg = f"Payment of ₹{payment.amount} settled via {payment.get_payment_method_display()} for Order #{payment.order.order_number} ({payment.transaction_reference})."
    return Notification.objects.create(
        recipient=recipient,
        title=title,
        message=msg,
        notification_type=NotificationType.PAYMENT,
        url="/billing/"
    )

def mark_all_notifications_read(user):
    """
    Marks all unread notifications for a user as read.
    """
    count = Notification.objects.filter(recipient=user, is_read=False).update(is_read=True)
    return count

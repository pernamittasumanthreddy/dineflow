/**
 * DineFlow POS & Indian GST Billing Engine
 * Supports real-time cart computation, Indian food menu catalog,
 * CGST + SGST tax split, dynamic UPI QR modal, KOT print simulation, and bill settlement.
 */

window.POSEngine = (function() {
  'use strict';

  // State
  const state = {
    selectedTable: 'T-04 (AC Hall)',
    orderType: 'dine_in',
    cart: [
      { id: 101, name: 'Hyderabadi Chicken Dum Biryani', category: 'Biryani', price: 340, qty: 2, diet: 'nonveg', notes: 'Extra spicy, serve raita' },
      { id: 102, name: 'Paneer Butter Masala', category: 'Curries', price: 260, qty: 1, diet: 'veg', notes: 'Less butter' },
      { id: 103, name: 'Butter Garlic Naan', category: 'Breads', price: 65, qty: 4, diet: 'veg', notes: 'Crispy' },
      { id: 104, name: 'Gulab Jamun with Rabdi', category: 'Desserts', price: 140, qty: 2, diet: 'veg', notes: 'Warm' }
    ],
    discountPercent: 0,
    cgstRate: 2.5,
    sgstRate: 2.5,
    serviceChargePercent: 0
  };

  function init() {
    renderCart();
    bindEvents();
  }

  function bindEvents() {
    // Category tabs
    const catPills = document.querySelectorAll('.df-pos-category-pill');
    catPills.forEach(pill => {
      pill.addEventListener('click', () => {
        catPills.forEach(p => p.classList.remove('active'));
        pill.classList.add('active');
        const cat = pill.getAttribute('data-category');
        filterCatalog(cat);
      });
    });

    // Order type tabs
    const typeTabs = document.querySelectorAll('.df-pos-type-tab');
    typeTabs.forEach(tab => {
      tab.addEventListener('click', () => {
        typeTabs.forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        state.orderType = tab.getAttribute('data-type');
      });
    });

    // Food item search
    const searchInput = document.getElementById('df-pos-search');
    if (searchInput) {
      searchInput.addEventListener('input', (e) => {
        const query = e.target.value.toLowerCase();
        const cards = document.querySelectorAll('.df-food-card');
        cards.forEach(card => {
          const name = card.querySelector('.df-food-name').textContent.toLowerCase();
          const cat = card.querySelector('.df-food-category-tag').textContent.toLowerCase();
          card.style.display = (name.includes(query) || cat.includes(query)) ? 'flex' : 'none';
        });
      });
    }
  }

  function filterCatalog(category) {
    const cards = document.querySelectorAll('.df-food-card');
    cards.forEach(card => {
      const itemCat = card.getAttribute('data-category');
      if (category === 'all' || itemCat === category) {
        card.style.display = 'flex';
      } else {
        card.style.display = 'none';
      }
    });
  }

  function addItem(id, name, price, category, diet) {
    const existing = state.cart.find(item => item.id === id);
    if (existing) {
      existing.qty += 1;
    } else {
      state.cart.push({
        id,
        name,
        category,
        price: parseFloat(price),
        qty: 1,
        diet: diet || 'veg',
        notes: ''
      });
    }
    renderCart();
    DineFlow.showToast('Item Added', `${name} added to cart.`, 'success', 2000);
  }

  function updateQty(id, delta) {
    const item = state.cart.find(i => i.id === id);
    if (!item) return;
    item.qty += delta;
    if (item.qty <= 0) {
      state.cart = state.cart.filter(i => i.id !== id);
    }
    renderCart();
  }

  function clearCart() {
    if (state.cart.length === 0) return;
    state.cart = [];
    renderCart();
    DineFlow.showToast('Cart Cleared', 'All items removed.', 'info');
  }

  function calculateTotals() {
    const subtotal = state.cart.reduce((sum, item) => sum + (item.price * item.qty), 0);
    const discountAmount = (subtotal * state.discountPercent) / 100;
    const taxableAmount = Math.max(0, subtotal - discountAmount);
    
    const cgstAmount = (taxableAmount * state.cgstRate) / 100;
    const sgstAmount = (taxableAmount * state.sgstRate) / 100;
    const totalGst = cgstAmount + sgstAmount;
    
    const serviceCharge = (taxableAmount * state.serviceChargePercent) / 100;
    const rawGrandTotal = taxableAmount + totalGst + serviceCharge;
    const grandTotal = Math.round(rawGrandTotal);
    const roundOff = (grandTotal - rawGrandTotal).toFixed(2);

    return {
      subtotal,
      discountAmount,
      taxableAmount,
      cgstAmount,
      sgstAmount,
      totalGst,
      serviceCharge,
      roundOff,
      grandTotal,
      itemCount: state.cart.reduce((cnt, item) => cnt + item.qty, 0)
    };
  }

  function renderCart() {
    const container = document.getElementById('df-pos-cart-items-container');
    if (!container) return;

    if (state.cart.length === 0) {
      container.innerHTML = `
        <div style="text-align: center; padding: 3rem 1rem; color: var(--df-text-muted);">
          <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🍽️</div>
          <div style="font-weight: 600; color: var(--df-charcoal-700);">No items in order</div>
          <div style="font-size: 0.8125rem; margin-top: 0.25rem;">Select dishes from the menu to start ordering</div>
        </div>
      `;
    } else {
      container.innerHTML = state.cart.map(item => `
        <div class="df-pos-cart-row">
          <div class="df-cart-item-info">
            <div class="df-cart-item-name">
              <span class="df-diet-mark ${item.diet === 'nonveg' ? 'nonveg-mark' : 'veg-mark'}"></span>
              <span>${item.name}</span>
            </div>
            <div class="df-cart-item-unit-price">${DineFlow.formatINR(item.price)} each ${item.notes ? `• <span style="color:var(--df-terracotta-700); font-style:italic;">${item.notes}</span>` : ''}</div>
          </div>
          <div class="df-cart-qty-ctrl">
            <button class="df-qty-btn" onclick="POSEngine.updateQty(${item.id}, -1)">−</button>
            <span class="df-qty-val">${item.qty}</span>
            <button class="df-qty-btn" onclick="POSEngine.updateQty(${item.id}, 1)">+</button>
          </div>
          <div class="df-cart-item-total">
            ${DineFlow.formatINR(item.price * item.qty)}
          </div>
        </div>
      `).join('');
    }

    const totals = calculateTotals();
    const subtotalEl = document.getElementById('df-pos-subtotal');
    const cgstEl = document.getElementById('df-pos-cgst');
    const sgstEl = document.getElementById('df-pos-sgst');
    const grandTotalEl = document.getElementById('df-pos-grand-total');
    const itemCountEl = document.getElementById('df-pos-item-count');

    if (subtotalEl) subtotalEl.textContent = DineFlow.formatINR(totals.subtotal);
    if (cgstEl) cgstEl.textContent = DineFlow.formatINR(totals.cgstAmount);
    if (sgstEl) sgstEl.textContent = DineFlow.formatINR(totals.sgstAmount);
    if (grandTotalEl) grandTotalEl.textContent = DineFlow.formatINR(totals.grandTotal);
    if (itemCountEl) itemCountEl.textContent = `${totals.itemCount} items`;
  }

  function fireKOT() {
    if (state.cart.length === 0) {
      DineFlow.showToast('Empty Order', 'Please add items before firing KOT.', 'warning');
      return;
    }
    const kotNum = Math.floor(1000 + Math.random() * 9000);
    DineFlow.showToast(
      'KOT Fired to Kitchen',
      `KOT #${kotNum} for ${state.selectedTable} sent to Tandoor & Curry stations.`,
      'success',
      4000
    );
  }

  function showSettlementModal() {
    if (state.cart.length === 0) {
      DineFlow.showToast('Empty Cart', 'Cannot settle empty bill.', 'warning');
      return;
    }
    const totals = calculateTotals();
    const modalAmountEl = document.getElementById('df-settle-amount');
    if (modalAmountEl) modalAmountEl.textContent = DineFlow.formatINR(totals.grandTotal);
    
    // Draw UPI QR simulator
    drawUpiQr(totals.grandTotal);
    DineFlow.openModal('df-settlement-modal');
  }

  function drawUpiQr(amount) {
    const canvas = document.getElementById('df-upi-qr-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const w = canvas.width = 160;
    const h = canvas.height = 160;

    ctx.fillStyle = '#FFFFFF';
    ctx.fillRect(0, 0, w, h);

    // Render stylized QR pattern
    ctx.fillStyle = '#1E1E24';
    const gridSize = 16;
    const cellSize = w / gridSize;

    // Outer anchor boxes
    drawQrAnchor(ctx, 0, 0, cellSize);
    drawQrAnchor(ctx, (gridSize - 5) * cellSize, 0, cellSize);
    drawQrAnchor(ctx, 0, (gridSize - 5) * cellSize, cellSize);

    // Random pseudo data pattern based on amount
    const seed = Math.floor(amount);
    for (let r = 0; r < gridSize; r++) {
      for (let c = 0; c < gridSize; c++) {
        if ((r < 5 && c < 5) || (r < 5 && c >= gridSize - 5) || (r >= gridSize - 5 && c < 5)) continue;
        if (((r * 31 + c * 17 + seed) % 5) > 2) {
          ctx.fillRect(c * cellSize + 1, r * cellSize + 1, cellSize - 2, cellSize - 2);
        }
      }
    }
  }

  function drawQrAnchor(ctx, x, y, cellSize) {
    ctx.fillStyle = '#1E1E24';
    ctx.fillRect(x, y, cellSize * 5, cellSize * 5);
    ctx.fillStyle = '#FFFFFF';
    ctx.fillRect(x + cellSize, y + cellSize, cellSize * 3, cellSize * 3);
    ctx.fillStyle = '#C24312';
    ctx.fillRect(x + cellSize * 1.5, y + cellSize * 1.5, cellSize * 2, cellSize * 2);
  }

  function completePayment(method) {
    const totals = calculateTotals();
    const invNumber = 'INV-' + Math.floor(100000 + Math.random() * 900000);
    DineFlow.closeModal('df-settlement-modal');
    
    DineFlow.showToast(
      'Payment Received',
      `Bill settled via ${method.toUpperCase()} for ${DineFlow.formatINR(totals.grandTotal)}. Tax Invoice #${invNumber} generated.`,
      'success',
      5000
    );

    // Open GST Tax Invoice Preview
    openTaxInvoice(invNumber, method, totals);
    state.cart = [];
    renderCart();
  }

  function openTaxInvoice(invNumber, method, totals) {
    const invoiceEl = document.getElementById('df-invoice-preview-container');
    if (!invoiceEl) return;

    invoiceEl.innerHTML = `
      <div style="background:#FFF; padding:1.5rem; font-family:var(--df-font-sans); font-size:0.875rem; color:#1E1E24; border:1px solid #EFE9E0;">
        <div style="text-align:center; border-bottom:1px dashed #333; padding-bottom:0.75rem; margin-bottom:0.75rem;">
          <h3 style="font-family:var(--df-font-serif); font-size:1.4rem; color:var(--df-maroon-800); margin-bottom:0.2rem;">Andhra Spice Kitchen & Grand Dine</h3>
          <div style="font-size:0.75rem; color:#585866;">Branch: Indiranagar 100ft Road, Bangalore - 560038</div>
          <div style="font-size:0.75rem; color:#585866;">GSTIN: 29AABCS1429B1Z5 | FSSAI: 11223334000121</div>
          <div style="font-size:0.8125rem; font-weight:700; margin-top:0.35rem; color:var(--df-terracotta-700);">TAX INVOICE (GST RULES COMPLIANT)</div>
        </div>
        <div style="display:flex; justify-content:space-between; font-size:0.78rem; margin-bottom:0.75rem;">
          <div><strong>Inv #:</strong> ${invNumber}<br><strong>Table:</strong> ${state.selectedTable}</div>
          <div style="text-align:right;"><strong>Date:</strong> ${new Date().toLocaleDateString('en-IN')}<br><strong>Mode:</strong> ${method.toUpperCase()}</div>
        </div>
        <table style="width:100%; border-collapse:collapse; font-size:0.8125rem; margin-bottom:0.75rem;">
          <thead>
            <tr style="border-bottom:1px solid #333; text-align:left;">
              <th style="padding:4px 0;">Item</th>
              <th style="text-align:center;">Qty</th>
              <th style="text-align:right;">Rate</th>
              <th style="text-align:right;">Amount</th>
            </tr>
          </thead>
          <tbody>
            <tr style="border-bottom:1px dashed #DDD;"><td style="padding:4px 0;">Hyderabadi Chicken Biryani</td><td style="text-align:center;">2</td><td style="text-align:right;">₹340.00</td><td style="text-align:right;">₹680.00</td></tr>
            <tr style="border-bottom:1px dashed #DDD;"><td style="padding:4px 0;">Paneer Butter Masala</td><td style="text-align:center;">1</td><td style="text-align:right;">₹260.00</td><td style="text-align:right;">₹260.00</td></tr>
            <tr style="border-bottom:1px dashed #DDD;"><td style="padding:4px 0;">Butter Garlic Naan</td><td style="text-align:center;">4</td><td style="text-align:right;">₹65.00</td><td style="text-align:right;">₹260.00</td></tr>
            <tr style="border-bottom:1px dashed #DDD;"><td style="padding:4px 0;">Gulab Jamun with Rabdi</td><td style="text-align:center;">2</td><td style="text-align:right;">₹140.00</td><td style="text-align:right;">₹280.00</td></tr>
          </tbody>
        </table>
        <div style="border-top:1px dashed #333; padding-top:0.5rem; font-size:0.8125rem;">
          <div style="display:flex; justify-content:space-between;"><span>Subtotal:</span><span>${DineFlow.formatINR(totals.subtotal)}</span></div>
          <div style="display:flex; justify-content:space-between; font-size:0.75rem; color:#585866;"><span>CGST (2.5%):</span><span>${DineFlow.formatINR(totals.cgstAmount)}</span></div>
          <div style="display:flex; justify-content:space-between; font-size:0.75rem; color:#585866;"><span>SGST (2.5%):</span><span>${DineFlow.formatINR(totals.sgstAmount)}</span></div>
          <div style="display:flex; justify-content:space-between; font-weight:800; font-size:1.1rem; color:var(--df-maroon-800); margin-top:0.35rem; border-top:1px solid #333; padding-top:0.35rem;">
            <span>GRAND TOTAL:</span><span>${DineFlow.formatINR(totals.grandTotal)}</span>
          </div>
        </div>
        <div style="text-align:center; font-size:0.75rem; color:#777; margin-top:1rem;">
          *** Thank You for Dining with Us! Visit Again ***<br>
          For digital bill & loyalty points, scan QR code on receipt.
        </div>
      </div>
    `;
    DineFlow.openModal('df-tax-invoice-modal');
  }

  return {
    init,
    addItem,
    updateQty,
    clearCart,
    fireKOT,
    showSettlementModal,
    completePayment
  };
})();

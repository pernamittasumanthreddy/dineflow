/**
 * DineFlow Kitchen Display System (KDS) Controller
 * Live preparation timers, station routing, and Kanban stage transitions
 */

window.KDSEngine = (function() {
  'use strict';

  // State
  const orders = [
    {
      id: 'KOT-1042',
      table: 'T-04 (AC Hall)',
      waiter: 'Ravi Teja',
      type: 'Dine-In',
      station: 'tandoor',
      status: 'preparing',
      elapsedSeconds: 740, // 12m 20s
      targetMinutes: 15,
      items: [
        { name: 'Murg Malai Tikka (8 pcs)', qty: 2, notes: 'Extra mint chutney' },
        { name: 'Tandoori Roti (Butter)', qty: 4, notes: '' },
        { name: 'Dal Makhani Handi', qty: 1, notes: 'Rich cream top' }
      ]
    },
    {
      id: 'KOT-1043',
      table: 'T-08 (Terrace)',
      waiter: 'Arjun Varma',
      type: 'Dine-In',
      station: 'biryani',
      status: 'new',
      elapsedSeconds: 160, // 2m 40s
      targetMinutes: 12,
      items: [
        { name: 'Hyderabadi Chicken Dum Biryani', qty: 3, notes: 'Double masala, salan' },
        { name: 'Mirchi Ka Salan', qty: 2, notes: '' },
        { name: 'Double Ka Meetha', qty: 2, notes: 'Warm' }
      ]
    },
    {
      id: 'KOT-1044',
      table: 'Zomato #4891',
      waiter: 'Delivery Dispatch',
      type: 'Online / Zomato',
      station: 'curry',
      status: 'preparing',
      elapsedSeconds: 980, // 16m 20s (Urgent)
      targetMinutes: 15,
      items: [
        { name: 'Paneer Butter Masala', qty: 2, notes: 'Jain preparation' },
        { name: 'Butter Naan', qty: 6, notes: 'Pack tightly in foil' },
        { name: 'Jeera Rice Large', qty: 1, notes: '' }
      ]
    },
    {
      id: 'KOT-1040',
      table: 'T-12 (PDR-1)',
      waiter: 'Sneha Reddy',
      type: 'Dine-In',
      station: 'curry',
      status: 'ready',
      elapsedSeconds: 820,
      targetMinutes: 15,
      items: [
        { name: 'Andhra Chettinad Mutton Curry', qty: 2, notes: 'Very spicy' },
        { name: 'Steamed Sona Masoori Rice', qty: 2, notes: 'Hot ghee separate' }
      ]
    }
  ];

  let activeStation = 'all';

  function init() {
    renderBoard();
    setInterval(updateTimers, 1000);
    bindStationFilters();
  }

  function bindStationFilters() {
    const btns = document.querySelectorAll('.df-kds-station-btn');
    btns.forEach(btn => {
      btn.addEventListener('click', () => {
        btns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        activeStation = btn.getAttribute('data-station');
        renderBoard();
      });
    });
  }

  function updateTimers() {
    orders.forEach(order => {
      if (order.status !== 'completed') {
        order.elapsedSeconds += 1;
      }
    });
    // Update timer badges on DOM
    document.querySelectorAll('[data-kot-timer]').forEach(el => {
      const kotId = el.getAttribute('data-kot-timer');
      const order = orders.find(o => o.id === kotId);
      if (order) {
        const mins = Math.floor(order.elapsedSeconds / 60);
        const secs = order.elapsedSeconds % 60;
        el.textContent = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
        
        if (mins >= order.targetMinutes) {
          el.className = 'df-kds-timer timer-red';
          const card = el.closest('.df-kds-card');
          if (card) card.classList.add('urgent');
        } else if (mins >= order.targetMinutes - 3) {
          el.className = 'df-kds-timer timer-amber';
        } else {
          el.className = 'df-kds-timer timer-green';
        }
      }
    });
  }

  function bumpOrder(kotId, nextStatus) {
    const order = orders.find(o => o.id === kotId);
    if (!order) return;
    order.status = nextStatus;
    renderBoard();
    DineFlow.showToast(
      'KDS Updated',
      `${order.id} for ${order.table} moved to ${nextStatus.toUpperCase()}.`,
      'success',
      2500
    );
  }

  function renderBoard() {
    const newCol = document.getElementById('df-kds-col-new');
    const prepCol = document.getElementById('df-kds-col-prep');
    const readyCol = document.getElementById('df-kds-col-ready');
    const doneCol = document.getElementById('df-kds-col-done');

    if (!newCol || !prepCol || !readyCol || !doneCol) return;

    const filtered = orders.filter(o => activeStation === 'all' || o.station === activeStation);

    newCol.innerHTML = renderColumnCards(filtered.filter(o => o.status === 'new'), 'preparing', 'Start Cooking 👨‍🍳', 'btn-bump-prep');
    prepCol.innerHTML = renderColumnCards(filtered.filter(o => o.status === 'preparing'), 'ready', 'Mark Ready 🔔', 'btn-bump-ready');
    readyCol.innerHTML = renderColumnCards(filtered.filter(o => o.status === 'ready'), 'completed', 'Order Served / Dispatched 🚀', 'btn-bump-done');
    doneCol.innerHTML = renderColumnCards(filtered.filter(o => o.status === 'completed'), 'archived', 'Archived', 'btn-bump-done', true);
  }

  function renderColumnCards(cards, nextStatus, nextLabel, btnClass, isDone = false) {
    if (cards.length === 0) {
      return `<div style="text-align:center; padding:2rem 1rem; color:#666; font-size:0.8125rem;">No active tickets</div>`;
    }
    return cards.map(order => {
      const isUrgent = (order.elapsedSeconds / 60) >= order.targetMinutes;
      const mins = Math.floor(order.elapsedSeconds / 60);
      const secs = order.elapsedSeconds % 60;
      const timerStr = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
      
      return `
        <div class="df-kds-card ${isUrgent ? 'urgent' : ''}">
          <div class="df-kds-card-top">
            <span class="df-kds-kot-num">${order.id}</span>
            <span data-kot-timer="${order.id}" class="df-kds-timer ${isUrgent ? 'timer-red' : 'timer-green'}">${timerStr}</span>
          </div>
          <div class="df-kds-meta">
            <span><strong>${order.table}</strong></span>
            <span style="color:var(--df-saffron-400);">${order.waiter}</span>
          </div>
          <ul class="df-kds-items">
            ${order.items.map(item => `
              <li class="df-kds-item-row">
                <span><span class="df-kds-item-qty">${item.qty}×</span> ${item.name}</span>
              </li>
              ${item.notes ? `<div class="df-kds-item-notes">📝 ${item.notes}</div>` : ''}
            `).join('')}
          </ul>
          ${!isDone ? `
            <button class="df-kds-bump-btn ${btnClass}" onclick="KDSEngine.bumpOrder('${order.id}', '${nextStatus}')">
              ${nextLabel}
            </button>
          ` : `
            <div style="font-size:0.75rem; color:#888; text-align:center; padding:0.4rem;">Order Completed</div>
          `}
        </div>
      `;
    }).join('');
  }

  return {
    init,
    bumpOrder
  };
})();

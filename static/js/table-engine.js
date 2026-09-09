/**
 * DineFlow Floor Plan & Table Management Engine
 * Visual table layout, live occupancy states, timer countdowns, and quick actions.
 */

window.TableEngine = (function() {
  'use strict';

  const tables = [
    { id: 'T-01', zone: 'ac_dining', seats: 2, status: 'available', orderTotal: 0, waiter: '-', occupiedMins: 0 },
    { id: 'T-02', zone: 'ac_dining', seats: 4, status: 'occupied', orderTotal: 1450, waiter: 'Ravi Teja', occupiedMins: 38 },
    { id: 'T-03', zone: 'ac_dining', seats: 4, status: 'available', orderTotal: 0, waiter: '-', occupiedMins: 0 },
    { id: 'T-04', zone: 'ac_dining', seats: 6, status: 'occupied', orderTotal: 2680, waiter: 'Sneha Reddy', occupiedMins: 52 },
    { id: 'T-05', zone: 'ac_dining', seats: 2, status: 'reserved', orderTotal: 0, waiter: 'Arjun Varma', occupiedMins: 0, reservedFor: 'Dr. Anjali (8:00 PM)' },
    { id: 'T-06', zone: 'ac_dining', seats: 8, status: 'cleaning', orderTotal: 0, waiter: 'Ravi Teja', occupiedMins: 0 },
    
    { id: 'TR-01', zone: 'terrace', seats: 4, status: 'occupied', orderTotal: 1820, waiter: 'Pavan V', occupiedMins: 25 },
    { id: 'TR-02', zone: 'terrace', seats: 4, status: 'available', orderTotal: 0, waiter: '-', occupiedMins: 0 },
    { id: 'TR-03', zone: 'terrace', seats: 6, status: 'occupied', orderTotal: 3450, waiter: 'Arjun Varma', occupiedMins: 45 },
    { id: 'TR-04', zone: 'terrace', seats: 2, status: 'reserved', orderTotal: 0, waiter: '-', occupiedMins: 0, reservedFor: 'Mr. Vikram (8:30 PM)' },
    
    { id: 'PDR-01', zone: 'pdr', seats: 12, status: 'occupied', orderTotal: 8900, waiter: 'Sneha Reddy', occupiedMins: 70 },
    { id: 'PDR-02', zone: 'pdr', seats: 16, status: 'reserved', orderTotal: 0, waiter: 'Ravi Teja', occupiedMins: 0, reservedFor: 'Infosys Corp Dinner' },
    
    { id: 'BAR-01', zone: 'bar', seats: 2, status: 'available', orderTotal: 0, waiter: '-', occupiedMins: 0 },
    { id: 'BAR-02', zone: 'bar', seats: 2, status: 'occupied', orderTotal: 980, waiter: 'Pavan V', occupiedMins: 15 },
    { id: 'BAR-03', zone: 'bar', seats: 2, status: 'available', orderTotal: 0, waiter: '-', occupiedMins: 0 },
  ];

  let currentZone = 'all';

  function init() {
    renderFloorPlan();
    bindZoneTabs();
  }

  function bindZoneTabs() {
    const tabs = document.querySelectorAll('.df-zone-tab');
    tabs.forEach(tab => {
      tab.addEventListener('click', () => {
        tabs.forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        currentZone = tab.getAttribute('data-zone');
        renderFloorPlan();
      });
    });
  }

  function setTableStatus(tableId, newStatus) {
    const table = tables.find(t => t.id === tableId);
    if (!table) return;
    table.status = newStatus;
    renderFloorPlan();
    DineFlow.closeModal('df-table-action-modal');
    DineFlow.showToast(
      'Table Status Updated',
      `Table ${table.id} marked as ${newStatus.toUpperCase()}.`,
      'success'
    );
  }

  function openTableModal(tableId) {
    const table = tables.find(t => t.id === tableId);
    if (!table) return;

    const modalTitle = document.getElementById('df-table-modal-title');
    const modalBody = document.getElementById('df-table-modal-body');
    if (!modalTitle || !modalBody) return;

    modalTitle.textContent = `Table ${table.id} (${table.seats} Seater)`;
    modalBody.innerHTML = `
      <div style="display:flex; flex-direction:column; gap:1rem;">
        <div style="display:flex; justify-content:space-between; padding:0.75rem; background:var(--df-bg-cream); border-radius:var(--df-radius-md);">
          <div><strong>Status:</strong> <span class="df-badge badge-${table.status === 'available' ? 'success' : (table.status === 'occupied' ? 'warning' : 'info')}">${table.status}</span></div>
          <div><strong>Waiter:</strong> ${table.waiter}</div>
          <div><strong>Running Bill:</strong> ${DineFlow.formatINR(table.orderTotal)}</div>
        </div>
        ${table.occupiedMins > 0 ? `<div><strong>Occupied for:</strong> ${table.occupiedMins} minutes</div>` : ''}
        ${table.reservedFor ? `<div><strong>Reservation:</strong> ${table.reservedFor}</div>` : ''}
        <div style="border-top:1px solid #EFE9E0; padding-top:1rem;">
          <div style="font-weight:700; margin-bottom:0.65rem;">Quick Status Change:</div>
          <div style="display:grid; grid-template-columns:repeat(2, 1fr); gap:0.65rem;">
            <button class="df-btn df-btn-success" onclick="TableEngine.setTableStatus('${table.id}', 'available')">Mark Available</button>
            <button class="df-btn df-btn-saffron" onclick="TableEngine.setTableStatus('${table.id}', 'occupied')">Mark Occupied</button>
            <button class="df-btn df-btn-maroon" onclick="TableEngine.setTableStatus('${table.id}', 'reserved')">Mark Reserved</button>
            <button class="df-btn df-btn-outline" onclick="TableEngine.setTableStatus('${table.id}', 'cleaning')">Mark Cleaning</button>
          </div>
        </div>
        <div style="border-top:1px solid #EFE9E0; padding-top:0.85rem; display:flex; gap:0.75rem;">
          <a href="/pos/?table=${table.id}" class="df-btn df-btn-terracotta" style="flex:1;">Open in POS Terminal 🍽️</a>
        </div>
      </div>
    `;
    DineFlow.openModal('df-table-action-modal');
  }

  function renderFloorPlan() {
    const grid = document.getElementById('df-floor-grid');
    if (!grid) return;

    const filtered = tables.filter(t => currentZone === 'all' || t.zone === currentZone);

    grid.innerHTML = filtered.map(t => {
      let statusColor = '#279C44';
      let statusBadge = 'Available';
      let icon = '🪑';

      if (t.status === 'occupied') {
        statusColor = '#E0531A';
        statusBadge = `${t.occupiedMins}m | ${DineFlow.formatINR(t.orderTotal)}`;
        icon = '🍽️';
      } else if (t.status === 'reserved') {
        statusColor = '#9E222F';
        statusBadge = 'Reserved';
        icon = '📅';
      } else if (t.status === 'cleaning') {
        statusColor = '#8C8C9E';
        statusBadge = 'Cleaning';
        icon = '🧹';
      }

      return `
        <div class="df-card" style="padding:1.2rem; cursor:pointer; border-top:4px solid ${statusColor}; transition:transform 0.18s ease;" onclick="TableEngine.openTableModal('${t.id}')">
          <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.75rem;">
            <div>
              <div style="font-size:1.2rem; font-weight:800; color:var(--df-charcoal-900);">${t.id}</div>
              <div style="font-size:0.75rem; color:var(--df-text-secondary); text-transform:uppercase;">${t.zone.replace('_', ' ')} • ${t.seats} Seats</div>
            </div>
            <div style="font-size:1.4rem;">${icon}</div>
          </div>
          <div style="display:flex; align-items:center; justify-content:space-between; margin-top:0.5rem; font-size:0.8125rem;">
            <span style="font-weight:700; color:${statusColor};">${statusBadge}</span>
            <span style="color:var(--df-text-muted); font-size:0.75rem;">${t.waiter !== '-' ? t.waiter : 'Vacant'}</span>
          </div>
        </div>
      `;
    }).join('');
  }

  return {
    init,
    openTableModal,
    setTableStatus
  };
})();

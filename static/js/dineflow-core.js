/**
 * DineFlow Core UI Framework
 * Handles role switching, toasts, accessible modals, slide-out drawers,
 * search filters, and audio feedback.
 */

window.DineFlow = (function() {
  'use strict';

  // State
  const state = {
    activeModals: [],
    activeDrawers: []
  };

  /**
   * Format numbers to Indian Rupee Currency Format (₹ 1,25,000.00)
   */
  function formatINR(val) {
    const num = parseFloat(val);
    if (isNaN(num)) return '₹0.00';
    const isNegative = num < 0;
    const absVal = Math.abs(num);
    const parts = absVal.toFixed(2).split('.');
    let intPart = parts[0];
    const decPart = parts[1];

    if (intPart.length > 3) {
      const lastThree = intPart.substring(intPart.length - 3);
      let otherNumbers = intPart.substring(0, intPart.length - 3);
      otherNumbers = otherNumbers.replace(/\B(?=(\d{2})+(?!\d))/g, ",");
      intPart = otherNumbers + "," + lastThree;
    }
    return (isNegative ? '-' : '') + '₹' + intPart + '.' + decPart;
  }

  /**
   * Global Toast Notification Engine
   */
  function showToast(title, message, type = 'info', duration = 4000) {
    let container = document.querySelector('.df-toast-container');
    if (!container) {
      container = document.createElement('div');
      container.className = 'df-toast-container';
      document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = 'df-toast';

    let borderCol = 'var(--df-terracotta-600)';
    let iconSymbol = '🔔';
    if (type === 'success') { borderCol = 'var(--df-green-700)'; iconSymbol = '✅'; }
    if (type === 'danger' || type === 'error') { borderCol = 'var(--df-danger-700)'; iconSymbol = '⚠️'; }
    if (type === 'warning') { borderCol = 'var(--df-saffron-600)'; iconSymbol = '⚡'; }

    toast.style.borderLeftColor = borderCol;
    toast.innerHTML = `
      <div style="font-size: 1.25rem;">${iconSymbol}</div>
      <div style="flex: 1;">
        <div style="font-weight: 700; font-size: 0.875rem; color: var(--df-charcoal-900);">${title}</div>
        <div style="font-size: 0.8125rem; color: var(--df-text-secondary); margin-top: 2px;">${message}</div>
      </div>
      <button style="background:none; border:none; color:var(--df-text-muted); cursor:pointer; font-size:1.1rem;" onclick="this.parentElement.remove()">✕</button>
    `;

    container.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateX(100%)';
      toast.style.transition = 'all 0.3s ease';
      setTimeout(() => toast.remove(), 300);
    }, duration);
  }

  /**
   * Modal Management
   */
  function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (!modal) return;
    modal.classList.add('show');
    document.body.style.overflow = 'hidden';
    state.activeModals.push(modalId);
  }

  function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (!modal) return;
    modal.classList.remove('show');
    state.activeModals = state.activeModals.filter(id => id !== modalId);
    if (state.activeModals.length === 0 && state.activeDrawers.length === 0) {
      document.body.style.overflow = '';
    }
  }

  /**
   * Drawer Management
   */
  function openDrawer(drawerId) {
    const drawer = document.getElementById(drawerId);
    const backdrop = document.getElementById(drawerId + '-backdrop') || document.querySelector('.df-drawer-backdrop');
    if (!drawer) return;
    drawer.classList.add('show');
    if (backdrop) backdrop.classList.add('show');
    document.body.style.overflow = 'hidden';
    state.activeDrawers.push(drawerId);
  }

  function closeDrawer(drawerId) {
    const drawer = document.getElementById(drawerId);
    const backdrop = document.getElementById(drawerId + '-backdrop') || document.querySelector('.df-drawer-backdrop');
    if (!drawer) return;
    drawer.classList.remove('show');
    if (backdrop) backdrop.classList.remove('show');
    state.activeDrawers = state.activeDrawers.filter(id => id !== drawerId);
    if (state.activeModals.length === 0 && state.activeDrawers.length === 0) {
      document.body.style.overflow = '';
    }
  }

  /**
   * Switch Active Role (Simulated Session Switcher)
   */
  function switchRole(roleKey) {
    fetch('/accounts/switch-role/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken') || ''
      },
      body: JSON.stringify({ role: roleKey })
    })
    .then(r => r.json())
    .then(data => {
      if (data.status === 'ok') {
        window.location.href = data.redirect_url;
      } else {
        window.location.reload();
      }
    })
    .catch(() => {
      // Fallback direct redirection
      window.location.href = `/dashboard/${roleKey}/`;
    });
  }

  /**
   * Switch Active Branch
   */
  function switchBranch(branchName) {
    fetch('/accounts/switch-branch/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken') || ''
      },
      body: JSON.stringify({ branch: branchName })
    })
    .then(() => {
      window.location.reload();
    })
    .catch(() => {
      window.location.reload();
    });
  }

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  /**
   * Live Table Filtering
   */
  function initTableFilter(searchInputId, tableId) {
    const input = document.getElementById(searchInputId);
    const table = document.getElementById(tableId);
    if (!input || !table) return;

    input.addEventListener('keyup', function() {
      const filter = input.value.toLowerCase();
      const rows = table.querySelectorAll('tbody tr');
      rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(filter) ? '' : 'none';
      });
    });
  }

  // Mobile sidebar toggle handler
  document.addEventListener('DOMContentLoaded', () => {
    const sidebarToggle = document.getElementById('df-sidebar-toggle');
    const sidebar = document.querySelector('.df-sidebar');
    if (sidebarToggle && sidebar) {
      sidebarToggle.addEventListener('click', () => {
        sidebar.classList.toggle('show');
      });
    }

    // Close modals on Esc key
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        if (state.activeModals.length > 0) {
          closeModal(state.activeModals[state.activeModals.length - 1]);
        } else if (state.activeDrawers.length > 0) {
          closeDrawer(state.activeDrawers[state.activeDrawers.length - 1]);
        }
      }
    });
  });

  return {
    formatINR,
    showToast,
    openModal,
    closeModal,
    openDrawer,
    closeDrawer,
    switchRole,
    switchBranch,
    initTableFilter
  };
})();

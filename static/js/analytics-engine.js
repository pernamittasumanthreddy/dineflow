/**
 * DineFlow Analytics & BI Visualization Engine
 * Pure Canvas visualizer for sales curves, hourly heatmaps,
 * dish category breakdown, and AI demand forecasting.
 */

window.AnalyticsEngine = (function() {
  'use strict';

  function renderRevenueChart(canvasId, dataPoints) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const width = canvas.width = canvas.parentElement.clientWidth || 600;
    const height = canvas.height = 280;

    const padding = { top: 30, right: 30, bottom: 40, left: 60 };
    const chartW = width - padding.left - padding.right;
    const chartH = height - padding.top - padding.bottom;

    const data = dataPoints || [
      { label: 'Mon', sales: 64000, profit: 24000 },
      { label: 'Tue', sales: 72500, profit: 28500 },
      { label: 'Wed', sales: 81000, profit: 32000 },
      { label: 'Thu', sales: 89400, profit: 36200 },
      { label: 'Fri', sales: 135000, profit: 58000 },
      { label: 'Sat', sales: 182000, profit: 79000 },
      { label: 'Sun', sales: 195000, profit: 86000 }
    ];

    const maxVal = 220000;

    ctx.clearRect(0, 0, width, height);

    // Grid lines
    ctx.strokeStyle = '#EFE9E0';
    ctx.lineWidth = 1;
    for (let i = 0; i <= 4; i++) {
      const y = padding.top + (chartH / 4) * i;
      ctx.beginPath();
      ctx.moveTo(padding.left, y);
      ctx.lineTo(width - padding.right, y);
      ctx.stroke();

      const val = Math.round(maxVal - (maxVal / 4) * i);
      ctx.fillStyle = '#8C8C9E';
      ctx.font = '11px sans-serif';
      ctx.textAlign = 'right';
      ctx.fillText('₹' + (val / 1000) + 'k', padding.left - 10, y + 4);
    }

    const step = chartW / (data.length - 1);

    // Sales Area Gradient
    const grad = ctx.createLinearGradient(0, padding.top, 0, height - padding.bottom);
    grad.addColorStop(0, 'rgba(194, 67, 18, 0.35)');
    grad.addColorStop(1, 'rgba(194, 67, 18, 0.02)');

    ctx.beginPath();
    data.forEach((d, i) => {
      const x = padding.left + i * step;
      const y = height - padding.bottom - (d.sales / maxVal) * chartH;
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    });
    ctx.lineTo(padding.left + (data.length - 1) * step, height - padding.bottom);
    ctx.lineTo(padding.left, height - padding.bottom);
    ctx.closePath();
    ctx.fillStyle = grad;
    ctx.fill();

    // Sales Line
    ctx.beginPath();
    data.forEach((d, i) => {
      const x = padding.left + i * step;
      const y = height - padding.bottom - (d.sales / maxVal) * chartH;
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    });
    ctx.strokeStyle = '#C24312';
    ctx.lineWidth = 3;
    ctx.stroke();

    // Data Points
    data.forEach((d, i) => {
      const x = padding.left + i * step;
      const y = height - padding.bottom - (d.sales / maxVal) * chartH;

      ctx.beginPath();
      ctx.arc(x, y, 5, 0, Math.PI * 2);
      ctx.fillStyle = '#FFF';
      ctx.fill();
      ctx.strokeStyle = '#C24312';
      ctx.lineWidth = 2.5;
      ctx.stroke();

      // X Label
      ctx.fillStyle = '#585866';
      ctx.font = '600 12px sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(d.label, x, height - padding.bottom + 20);
    });
  }

  function renderCategoryDonut(canvasId) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const width = canvas.width = 240;
    const height = canvas.height = 240;

    const categories = [
      { name: 'Biryani & Rice', pct: 0.38, color: '#C24312' },
      { name: 'Tandoor & Starters', pct: 0.26, color: '#7A1A24' },
      { name: 'Gravies & Curries', pct: 0.18, color: '#E67E22' },
      { name: 'Breads & Accompaniments', pct: 0.10, color: '#D4AF37' },
      { name: 'Desserts & Beverages', pct: 0.08, color: '#1E7A35' }
    ];

    const cx = width / 2;
    const cy = height / 2;
    const outerR = 95;
    const innerR = 58;

    let startAngle = -Math.PI / 2;

    ctx.clearRect(0, 0, width, height);

    categories.forEach(cat => {
      const sliceAngle = cat.pct * Math.PI * 2;
      ctx.beginPath();
      ctx.arc(cx, cy, outerR, startAngle, startAngle + sliceAngle);
      ctx.arc(cx, cy, innerR, startAngle + sliceAngle, startAngle, true);
      ctx.closePath();
      ctx.fillStyle = cat.color;
      ctx.fill();
      startAngle += sliceAngle;
    });

    // Center text
    ctx.fillStyle = '#1E1E24';
    ctx.font = '800 1.2rem sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('₹8.28L', cx, cy - 8);
    ctx.font = '600 0.72rem sans-serif';
    ctx.fillStyle = '#8C8C9E';
    ctx.fillText('WEEKLY SALES', cx, cy + 12);
  }

  function renderHourlyHeatmap(containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
    const hours = ['11 AM', '12 PM', '1 PM', '2 PM', '3 PM', '4 PM', '5 PM', '6 PM', '7 PM', '8 PM', '9 PM', '10 PM', '11 PM'];

    let html = `
      <div style="overflow-x:auto;">
        <table style="width:100%; border-collapse:collapse; font-size:0.75rem; text-align:center;">
          <thead>
            <tr>
              <th style="padding:6px; color:#777; text-align:left;">Day / Hour</th>
              ${hours.map(h => `<th style="padding:6px; color:#555; font-weight:600;">${h}</th>`).join('')}
            </tr>
          </thead>
          <tbody>
    `;

    days.forEach((day, di) => {
      html += `<tr><td style="padding:6px; font-weight:700; color:#333; text-align:left;">${day}</td>`;
      hours.forEach((h, hi) => {
        // Peak hours are lunch (12-3) and dinner (8-11), heavier on weekends
        const isWeekend = di >= 4;
        const isPeak = (hi >= 1 && hi <= 3) || (hi >= 9 && hi <= 11);
        let intensity = 0.15;
        if (isPeak && isWeekend) intensity = 0.85;
        else if (isPeak) intensity = 0.60;
        else if (isWeekend) intensity = 0.40;

        const bg = `rgba(194, 67, 18, ${intensity})`;
        const textCol = intensity > 0.5 ? '#FFF' : '#333';
        const footfall = Math.floor(intensity * 120 + Math.random() * 15);

        html += `<td style="padding:6px; background:${bg}; color:${textCol}; border:1px solid #FFF; border-radius:3px; font-weight:600;" title="${day} ${h}: ~${footfall} guests">${footfall}</td>`;
      });
      html += `</tr>`;
    });

    html += `</tbody></table></div>`;
    container.innerHTML = html;
  }

  return {
    renderRevenueChart,
    renderCategoryDonut,
    renderHourlyHeatmap
  };
})();

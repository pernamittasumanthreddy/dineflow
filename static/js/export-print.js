/**
 * DineFlow Export & Print Utilities
 * Client-side CSV generation, print formatting, and thermal receipt trigger
 */

window.ExportPrint = (function() {
  'use strict';

  function exportTableToCSV(tableId, filename = 'dineflow_report.csv') {
    const table = document.getElementById(tableId);
    if (!table) {
      DineFlow.showToast('Export Error', 'Table not found for export.', 'danger');
      return;
    }

    const rows = Array.from(table.querySelectorAll('tr'));
    const csvContent = rows.map(row => {
      const cols = Array.from(row.querySelectorAll('th, td'));
      // Filter out action columns
      const filteredCols = cols.filter(c => !c.classList.contains('df-no-export') && !c.querySelector('.df-action-btns'));
      return filteredCols.map(col => {
        let text = col.innerText.replace(/(\r\n|\n|\r)/gm, ' ').replace(/"/g, '""').trim();
        return `"${text}"`;
      }).join(',');
    }).join('\r\n');

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    link.setAttribute('href', url);
    link.setAttribute('download', filename);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    DineFlow.showToast('Export Successful', `Downloaded ${filename} successfully.`, 'success');
  }

  function printElement(elementId) {
    const el = document.getElementById(elementId);
    if (!el) {
      window.print();
      return;
    }

    const printWin = window.open('', '_blank', 'width=800,height=600');
    printWin.document.write(`
      <html>
        <head>
          <title>DineFlow Print Document</title>
          <link rel="stylesheet" href="/static/css/dineflow-tokens.css">
          <link rel="stylesheet" href="/static/css/dineflow-base.css">
          <link rel="stylesheet" href="/static/css/dineflow-components.css">
          <style>
            body { background:#FFF; color:#000; padding:20px; }
            @media print { button { display:none; } }
          </style>
        </head>
        <body>
          ${el.innerHTML}
          <script>
            window.onload = function() { window.print(); window.close(); }
          </script>
        </body>
      </html>
    `);
    printWin.document.close();
  }

  return {
    exportTableToCSV,
    printElement
  };
})();

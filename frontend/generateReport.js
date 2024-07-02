const fs = require('fs');
const path = require('path');

const jsonFilePath = path.join(__dirname, 'data.json');

const assigneeData = {};
const statusData = {};
const reportData = [];
const allStatuses = new Set();

// Read and parse the JSON file
fs.readFile(jsonFilePath, 'utf8', (err, data) => {
  if (err) {
    console.error('Error reading the JSON file', err);
    return;
  }

  const issues = JSON.parse(data);

  issues.forEach(issue => {
    const { key, type, summary, assignee, created, duedate, status, last_comment, link } = issue;

    // Track all statuses
    allStatuses.add(status);

    // Process report data
    const dueDateDiff = calculateDueDateDifference(duedate);
    reportData.push({ key, type, summary, assignee, created, dueDateDiff, status, last_comment, link });

    // Process assignee data
    if (!assigneeData[assignee]) {
      assigneeData[assignee] = { total: 0 };
    }
    if (!assigneeData[assignee][status]) {
      assigneeData[assignee][status] = 0;
    }
    assigneeData[assignee][status]++;
    assigneeData[assignee].total++;

    // Process status data
    if (!statusData[status]) {
      statusData[status] = 0;
    }
    statusData[status]++;
  });

  generateHTMLReport();
  console.log('JSON file successfully processed and HTML report generated.');
});

function calculateDueDateDifference(duedate) {
  const currentDate = new Date();
  let dueDateObj;

  if (!duedate) {
    // Set due date to the end of the current month
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth() + 1;
    dueDateObj = new Date(year, month, 0); // Last day of the current month
  } else {
    dueDateObj = new Date(duedate);
  }

  const diffInTime = dueDateObj.getTime() - currentDate.getTime();
  const diffInDays = Math.ceil(diffInTime / (1000 * 3600 * 24));
  return diffInDays;
}

function generateHTMLReport() {
  const htmlContent = `
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>JIRA Report</title>
  <style>
    body { font-family: Arial, sans-serif; }
    .tab { display: none; }
    .tab.active { display: block; }
    table { width: 100%; border-collapse: collapse; }
    th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
    th { background-color: #f4f4f4; }
    tr:nth-child(even) { background-color: #f9f9f9; }
  </style>
</head>
<body>
  <h1>JIRA Report</h1>
  <div>
    <button onclick="openTab('reportsTab')">Reports</button>
    <button onclick="openTab('assigneeTab')">Assignee</button>
    <button onclick="openTab('statusTab')">Status</button>
  </div>
  <div id="reportsTab" class="tab active">
    <h2>Reports</h2>
    <table>
      <thead>
        <tr>
          <th>Key</th>
          <th>Type</th>
          <th>Summary</th>
          <th>Assignee</th>
          <th>Created</th>
          <th>Due Date Difference (days)</th>
          <th>Status</th>
          <th>Last Comment</th>
        </tr>
      </thead>
      <tbody>
        ${reportData.map(row => `
          <tr>
            <td><a href="${row.link}" target="_blank">${row.key}</a></td>
            <td>${row.type}</td>
            <td>${row.summary}</td>
            <td>${row.assignee}</td>
            <td>${row.created}</td>
            <td>${row.dueDateDiff}</td>
            <td>${row.status}</td>
            <td>${row.last_comment}</td>
          </tr>`).join('')}
      </tbody>
    </table>
  </div>
  <div id="assigneeTab" class="tab">
    <h2>Assignee</h2>
    <table>
      <thead>
        <tr>
          <th>Assignee</th>
          ${Array.from(allStatuses).map(status => `<th>${status}</th>`).join('')}
          <th>Total</th>
        </tr>
      </thead>
      <tbody>
        ${Object.entries(assigneeData).map(([assignee, statuses]) => `
          <tr>
            <td>${assignee}</td>
            ${Array.from(allStatuses).map(status => `<td>${statuses[status] || 0}</td>`).join('')}
            <td>${statuses.total}</td>
          </tr>`).join('')}
      </tbody>
    </table>
  </div>
  <div id="statusTab" class="tab">
    <h2>Status</h2>
    <table>
      <thead>
        <tr>
          <th>Status</th>
          <th>Count</th>
        </tr>
      </thead>
      <tbody>
        ${Object.entries(statusData).map(([status, count]) => `
          <tr>
            <td>${status}</td>
            <td>${count}</td>
          </tr>`).join('')}
      </tbody>
    </table>
  </div>
  <script>
    function openTab(tabName) {
      const tabs = document.querySelectorAll('.tab');
      tabs.forEach(tab => {
        tab.classList.toggle('active', tab.id === tabName);
      });
    }
  </script>
</body>
</html>`;

  fs.writeFileSync('index.html', htmlContent, 'utf-8');
}

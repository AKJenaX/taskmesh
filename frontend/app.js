/**
 * TaskMesh Data Story JS Logic - Guided Dashboard
 */

document.addEventListener("DOMContentLoaded", () => {
  // DOM Variables
  const uiQueue = document.getElementById("ui-queue");
  const resultTableBody = document.querySelector("#result-table tbody");
  const runBtnTop = document.getElementById("run-scheduler-btn");
  const btnText = runBtnTop.querySelector(".btn-text");
  const btnSpinner = runBtnTop.querySelector(".spinner");
  const globalStatus = document.getElementById("global-status");
  const resultsWrapper = document.getElementById("results-wrapper");
  const emptyResultsState = document.getElementById("empty-results-state");

  // Input Controls
  const addTaskBtn = document.getElementById("ui-add-task");
  const uiTaskName = document.getElementById("ui-task-name");
  const priorityBtns = document.querySelectorAll("#ui-priority .btn-toggle");
  const durationBtns = document.querySelectorAll("#ui-duration .btn-toggle");
  const customPriority = document.getElementById("custom-priority");
  const customDuration = document.getElementById("custom-duration");
  const priGroup = document.getElementById("priority-group");
  const durGroup = document.getElementById("duration-group");
  const scenarioBtns = document.querySelectorAll("#ui-scenarios .pill");
  const errorMsg = document.getElementById("validation-errors");

  // Metrics
  const metricWait = document.getElementById("metric-wait");
  const impactWait = document.getElementById("impact-wait");
  const metricThroughput = document.getElementById("metric-throughput");
  const impactThroughput = document.getElementById("impact-throughput");
  const metricLatency = document.getElementById("metric-latency");
  const impactLatency = document.getElementById("impact-latency");
  const dynamicInsight = document.getElementById("dynamic-insight");
  const headlineText = document.getElementById("headline-text");

  // Chart Instances
  let timelineChart = null;
  let comparisonChart = null;

  // State
  let taskQueue = [];
  let taskIdCounter = 1;
  let currentPriority = 3;
  let currentDuration = 30;

  // Constants
  const PRIORITY_COLORS = {
    5: 'rgba(139, 92, 246, 0.8)', // Purple (High)
    4: 'rgba(139, 92, 246, 0.6)',
    3: 'rgba(0, 229, 255, 0.8)',  // Cyan (Med)
    2: 'rgba(0, 229, 255, 0.5)',
    1: 'rgba(148, 163, 184, 0.6)' // Gray (Low)
  };

  const SCENARIOS = {
    balanced: [
      { title: "Demo review", priority: 5, duration: 30 },
      { title: "Write slides", priority: 3, duration: 45 },
      { title: "Inbox cleanup", priority: 1, duration: 20 },
    ],
    high_priority_burst: [
      { title: "Production patch", priority: 5, duration: 25 },
      { title: "Incident postmortem", priority: 5, duration: 35 },
      { title: "Customer callback", priority: 4, duration: 20 },
      { title: "Backlog grooming", priority: 2, duration: 30 },
    ],
    long_tail: [
      { title: "Architecture RFC", priority: 4, duration: 90 },
      { title: "Tech debt cleanup", priority: 2, duration: 60 },
      { title: "Docs update", priority: 1, duration: 20 },
      { title: "QA rerun", priority: 3, duration: 45 },
      { title: "Sprint planning", priority: 2, duration: 50 },
    ],
  };

  // Focus Mode
  const inputPanel = document.querySelector(".input-panel");
  if(inputPanel) {
    inputPanel.addEventListener("focusin", () => document.body.classList.add("focus-mode"));
    inputPanel.addEventListener("focusout", (e) => {
      if (!inputPanel.contains(e.relatedTarget)) document.body.classList.remove("focus-mode");
    });
  }

  // Setup Event Listeners
  priorityBtns.forEach(btn => btn.addEventListener("click", (e) => {
    priorityBtns.forEach(b => b.classList.remove("active"));
    e.target.classList.add("active");
    currentPriority = parseInt(e.target.dataset.val, 10);
    customPriority.value = ""; 
    priGroup.className = "hybrid-input-group active-btn";
  }));

  customPriority.addEventListener("blur", (e) => {
    let val = parseInt(e.target.value, 10);
    if (!isNaN(val)) {
      if (val < 1) val = 1;
      if (val > 5) val = 5;
      e.target.value = val;
      currentPriority = val;
    }
  });

  customPriority.addEventListener("input", (e) => {
    priorityBtns.forEach(b => b.classList.remove("active"));
    priGroup.className = "hybrid-input-group active-custom";
    const val = parseInt(e.target.value, 10);
    if (!isNaN(val)) currentPriority = Math.min(Math.max(val, 1), 5);
  });

  durationBtns.forEach(btn => btn.addEventListener("click", (e) => {
    durationBtns.forEach(b => b.classList.remove("active"));
    e.target.classList.add("active");
    currentDuration = parseInt(e.target.dataset.val, 10);
    customDuration.value = ""; 
    durGroup.className = "hybrid-input-group active-btn";
  }));

  customDuration.addEventListener("blur", (e) => {
    let val = parseInt(e.target.value, 10);
    if (!isNaN(val)) {
      if (val < 1) val = 1;
      e.target.value = val;
      currentDuration = val;
    }
  });

  customDuration.addEventListener("input", (e) => {
    durationBtns.forEach(b => b.classList.remove("active"));
    durGroup.className = "hybrid-input-group active-custom";
    const val = parseInt(e.target.value, 10);
    if (!isNaN(val)) currentDuration = Math.max(val, 1);
  });

  // Step Controls logic
  document.querySelector('.minus-pri').addEventListener('click', () => {
    let v = parseInt(customPriority.value) || currentPriority;
    customPriority.value = Math.max(v - 1, 1);
    customPriority.dispatchEvent(new Event('input'));
  });
  document.querySelector('.plus-pri').addEventListener('click', () => {
    let v = parseInt(customPriority.value) || currentPriority;
    customPriority.value = Math.min(v + 1, 5);
    customPriority.dispatchEvent(new Event('input'));
  });
  document.querySelector('.minus-dur').addEventListener('click', () => {
    let v = parseInt(customDuration.value) || currentDuration;
    customDuration.value = Math.max(v - 5, 1);
    customDuration.dispatchEvent(new Event('input'));
  });
  document.querySelector('.plus-dur').addEventListener('click', () => {
    let v = parseInt(customDuration.value) || currentDuration;
    customDuration.value = v + 5;
    customDuration.dispatchEvent(new Event('input'));
  });

  scenarioBtns.forEach(btn => btn.addEventListener("click", (e) => {
    scenarioBtns.forEach(b => b.classList.remove("active"));
    e.target.classList.add("active");
    loadScenario(e.target.dataset.val);
  }));

  addTaskBtn.addEventListener("click", () => {
    const title = uiTaskName.value.trim() || `Task ${taskIdCounter}`;
    
    let p = customPriority.value !== "" ? parseInt(customPriority.value, 10) : currentPriority;
    if (isNaN(p) || p < 1 || p > 5) return showError("Priority must be between 1 and 5.");
    
    let d = customDuration.value !== "" ? parseInt(customDuration.value, 10) : currentDuration;
    if (isNaN(d) || d < 1) return showError("Duration must be a positive number.");

    taskQueue.push({ id: taskIdCounter++, title, priority: p, duration: d });
    uiTaskName.value = "";
    updateUI();
    showSuccess("Task added successfully");
  });

  runBtnTop.addEventListener("click", async () => {
    if (taskQueue.length === 0) return showError("Queue is empty.");
    await runDualScheduler();
  });

  function loadScenario(key) {
    taskQueue = [];
    taskIdCounter = 1;
    (SCENARIOS[key] || SCENARIOS.balanced).forEach(p => {
      taskQueue.push({ id: taskIdCounter++, title: p.title, priority: p.priority, duration: p.duration });
    });
    updateUI();
  }

  function updateUI() {
    runBtnTop.disabled = taskQueue.length === 0;
    if (taskQueue.length === 0) {
      uiQueue.innerHTML = `<div style="text-align:center; padding: 20px; font-style:italic; color: var(--text-muted); font-size:12px;">Queue is empty. Select a preset or add a task.</div>`;
      return;
    }
    uiQueue.innerHTML = taskQueue.map(t => `
      <div class="queue-card">
        <div class="q-title">${t.title}</div>
        <div class="q-badges">
          <span class="badge pri-badge">Imp: ${t.priority}</span>
          <span class="badge dur-badge">${t.duration}m</span>
        </div>
      </div>
    `).join("");
  }

  function showError(msg) {
    errorMsg.textContent = msg;
    errorMsg.style.color = "var(--danger)";
    setTimeout(() => errorMsg.textContent = "", 3000);
  }

  function showSuccess(msg) {
    errorMsg.textContent = msg;
    errorMsg.style.color = "var(--emerald)";
    setTimeout(() => errorMsg.textContent = "", 2000);
  }

  // Dual API Execution
  async function runDualScheduler() {
    console.log("TASK QUEUE LENGTH:", taskQueue.length);
    console.log("TASK QUEUE DATA:", JSON.stringify(taskQueue, null, 2));

    runBtnTop.disabled = true;
    btnText.textContent = "Processing...";
    btnSpinner.hidden = false;
    globalStatus.textContent = "Optimizing via RL & Baseline...";
    globalStatus.style.color = "#00e5ff";
    resultsWrapper.hidden = true; 
    emptyResultsState.hidden = true;

    const payloadTemplate = { tasks: taskQueue.map(t => ({ id: t.id, priority: t.priority, duration: t.duration })) };
    const sentPayload = { ...payloadTemplate, algorithm: "rl" };
    console.log("PAYLOAD SENT:", JSON.stringify(sentPayload, null, 2));

    try {
      const [baselineRes, rlRes] = await Promise.all([
        fetch("http://127.0.0.1:8000/schedule", {
          method: "POST", headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ ...payloadTemplate, algorithm: "baseline" })
        }),
        fetch("http://127.0.0.1:8000/schedule", {
          method: "POST", headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ ...payloadTemplate, algorithm: "rl" })
        })
      ]);

      if (!baselineRes.ok || !rlRes.ok) throw new Error("API call failed");

      const baselineData = await baselineRes.json();
      const rlData = await rlRes.json();

      console.log("FULL API RESPONSE:", JSON.stringify(rlData, null, 2));
      console.log("SCHEDULE LENGTH:", rlData.schedule?.length);

      if (rlData.schedule && rlData.schedule.length === 1) {
        console.error("❌ BACKEND RETURNING ONLY ONE TASK");
      }

      renderDataStory(baselineData, rlData);

    } catch (err) {
      console.error(err);
      globalStatus.textContent = "Execution Failed";
      globalStatus.style.color = "#ef4444";
      showError("Scheduler failed to respond.");
      emptyResultsState.hidden = false;
    } finally {
      runBtnTop.disabled = false;
      btnText.textContent = "Run Scheduler";
      btnSpinner.hidden = true;
    }
  }

  function renderDataStory(baseline, rl) {
    resultsWrapper.hidden = false;
    globalStatus.textContent = "Schedule Optimized";
    globalStatus.style.color = "#10b981";

    const schedule = rl.schedule || [];
    if (!schedule.length) {
      showError("No tasks scheduled");
      emptyResultsState.hidden = false;
      resultsWrapper.hidden = true;
      return;
    }

    console.log("RENDERING TASK COUNT:", schedule.length);

    // Clear the table first
    resultTableBody.innerHTML = "";

    // Append rows individually to avoid overwriting or slicing
    schedule.forEach((item, index) => {
      const orig = taskQueue.find(t => t.id == item.task_id || t.id == item.id) || {};
      const t = {
        title: orig.title || `Task ${item.task_id || item.id}`,
        priority: orig.priority || item.priority || 1,
        duration: orig.duration || (item.end - item.start),
        start: item.start,
        end: item.end,
        wait: item.wait_time || item.start
      };

      const row = document.createElement("tr");
      if (t.priority === 5) row.classList.add("high-priority-row");
      row.style.animationDelay = `${index * 0.04}s`;

      row.innerHTML = `
        <td>${index + 1}</td>
        <td>${t.title}</td>
        <td>${t.priority}</td>
        <td>${t.duration}m</td>
        <td>${t.start}m</td>
        <td>${t.wait}m</td>
        <td>${t.end}m</td>
      `;
      resultTableBody.appendChild(row);
    });

    console.log("FINAL ROW COUNT IN DOM:", resultTableBody.children.length);

    const orderedTasks = Array.from(resultTableBody.children).map(row => {
      // Reconstruct for charts if needed
      return {
        title: row.cells[1].innerText,
        start: parseInt(row.cells[4].innerText),
        duration: parseInt(row.cells[3].innerText),
        priority: parseInt(row.cells[2].innerText),
        end: parseInt(row.cells[6].innerText)
      };
    });

    const blMetrics = baseline.metrics || {};
    const rlMetrics = rl.metrics || {};

    const waitDiff = blMetrics.avg_wait_time - rlMetrics.avg_wait_time;
    const waitPct = blMetrics.avg_wait_time > 0 ? (waitDiff / blMetrics.avg_wait_time * 100).toFixed(0) : 0;
    
    const tpDiff = rlMetrics.throughput - blMetrics.throughput;
    const tpPct = blMetrics.throughput > 0 ? (tpDiff / blMetrics.throughput * 100).toFixed(0) : 0;

    const latDiff = blMetrics.tail_latency - rlMetrics.tail_latency;
    const latPct = blMetrics.tail_latency > 0 ? (latDiff / blMetrics.tail_latency * 100).toFixed(0) : 0;

    function renderImpact(el, diff, pct, isLowerBetter) {
      if (diff === 0) {
        el.textContent = "Same as Baseline";
        el.className = "m-impact impact-neutral";
      } else {
        const improved = diff > 0;
        const arrow = improved ? (isLowerBetter ? '⬇' : '⬆') : (isLowerBetter ? '⬆' : '⬇');
        el.textContent = `${arrow} ${Math.abs(pct)}% vs Baseline`;
        el.className = `m-impact ${improved ? 'impact-positive' : 'impact-negative'}`;
      }
    }

    metricWait.textContent = `${rlMetrics.avg_wait_time}m`;
    renderImpact(impactWait, waitDiff, waitPct, true);

    metricThroughput.textContent = rlMetrics.throughput;
    renderImpact(impactThroughput, tpDiff, tpPct, false);

    metricLatency.textContent = `${rlMetrics.tail_latency}m`;
    renderImpact(impactLatency, latDiff, latPct, true);

    // Generate Insight String & Headline (Simplified)
    if (waitDiff > 0) {
      headlineText.innerHTML = `AI reduced average delay by <span class="neon">${waitPct}%</span>`;
      dynamicInsight.innerHTML = `The system prioritizes urgent tasks first while avoiding long delays.`;
    } else if (tpDiff > 0) {
      headlineText.innerHTML = `AI increased tasks completed by <span class="neon">${tpPct}%</span>`;
      dynamicInsight.innerHTML = `The system tightly packed tasks to maximize throughput in the given time window.`;
    } else {
      headlineText.innerHTML = `Baseline flow is optimal for this load`;
      dynamicInsight.innerHTML = `The default ordering was already optimal for this specific combination of tasks.`;
    }

    const grid = document.querySelector('.graphs-grid');
    if(grid) grid.style.opacity = '0';
    
    setTimeout(() => {
      drawGraphs(orderedTasks, blMetrics, rlMetrics);
      if(grid) grid.style.opacity = '1';
    }, 150);
  }

  function drawGraphs(tasks, bl, rl) {
    Chart.defaults.color = '#94a3b8';
    Chart.defaults.font.family = "'Inter', sans-serif";

    if (timelineChart) timelineChart.destroy();
    timelineChart = new Chart(document.getElementById('timeline-chart').getContext('2d'), {
      type: 'bar',
      data: {
        labels: tasks.map(t => t.title),
        datasets: [
          { label: 'Start Offset', data: tasks.map(t => t.start), backgroundColor: 'rgba(0,0,0,0)' },
          { 
            label: 'Duration', 
            data: tasks.map(t => t.duration), 
            backgroundColor: tasks.map(t => PRIORITY_COLORS[t.priority] || PRIORITY_COLORS[1]),
            borderRadius: 4 
          }
        ]
      },
      options: {
        responsive: true, maintainAspectRatio: false, indexAxis: 'y',
        plugins: { legend: { display: false }, tooltip: { callbacks: { label: c => c.datasetIndex === 0 ? '' : `Runs: ${tasks[c.dataIndex].start}m - ${tasks[c.dataIndex].end}m` }}},
        scales: { x: { stacked: true, grid: { color: 'rgba(255,255,255,0.05)' } }, y: { stacked: true, grid: { display: false }, ticks: { font: { size: 11 } } } }
      }
    });

    if (comparisonChart) comparisonChart.destroy();
    comparisonChart = new Chart(document.getElementById('comparison-chart').getContext('2d'), {
      type: 'bar',
      data: {
        labels: ['Avg Delay', 'Worst Delay'],
        datasets: [
          { label: 'Baseline', data: [bl.avg_wait_time, bl.tail_latency], backgroundColor: 'rgba(148, 163, 184, 0.4)' },
          { label: 'AI Optimized', data: [rl.avg_wait_time, rl.tail_latency], backgroundColor: 'rgba(0, 229, 255, 0.8)' }
        ]
      },
      options: {
        responsive: true, maintainAspectRatio: false,
        plugins: { legend: { position: 'top', labels: { boxWidth: 10, font: {size: 11} } } },
        scales: { y: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { font: {size: 11} } }, x: { grid: { display: false }, ticks: { font: {size: 11} } } }
      }
    });
  }

  // Init
  loadScenario('high_priority_burst');
});

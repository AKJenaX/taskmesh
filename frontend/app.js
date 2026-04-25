// Elegant cursor movement effect
const cursorGlow = document.querySelector('.cursor-glow');
const cursorTrail = document.querySelector('.cursor-trail');
const cursorLightRing = document.querySelector('.cursor-light-ring');
let mouseX = 0, mouseY = 0;
let glowX = 0, glowY = 0;
let trailX = 0, trailY = 0;
let lastParticleTime = 0;
let lastRingTime = 0;

document.addEventListener('mousemove', (e) => {
  mouseX = e.clientX;
  mouseY = e.clientY;
  
  // Show cursor effects
  cursorGlow.style.opacity = '1';
  cursorTrail.style.opacity = '1';
  
  // Create light particles periodically
  const currentTime = Date.now();
  if (currentTime - lastParticleTime > 50) {
    createLightParticle(mouseX, mouseY);
    lastParticleTime = currentTime;
  }
  
  // Create expanding rings periodically
  if (currentTime - lastRingTime > 800) {
    createLightRing(mouseX, mouseY);
    lastRingTime = currentTime;
  }
});

document.addEventListener('mouseleave', () => {
  cursorGlow.style.opacity = '0';
  cursorTrail.style.opacity = '0';
});

// Create light particle effect
function createLightParticle(x, y) {
  const particle = document.createElement('div');
  particle.className = 'cursor-light-particle';
  
  // Random offset from cursor position
  const offsetX = (Math.random() - 0.5) * 30;
  const offsetY = (Math.random() - 0.5) * 30;
  
  particle.style.left = (x + offsetX) + 'px';
  particle.style.top = (y + offsetY) + 'px';
  particle.style.opacity = '1';
  
  document.body.appendChild(particle);
  
  // Remove particle after animation
  setTimeout(() => {
    particle.remove();
  }, 1000);
}

// Create expanding ring effect
function createLightRing(x, y) {
  const ring = document.createElement('div');
  ring.className = 'cursor-light-ring';
  
  ring.style.left = x + 'px';
  ring.style.top = y + 'px';
  ring.style.opacity = '1';
  
  document.body.appendChild(ring);
  
  // Remove ring after animation
  setTimeout(() => {
    ring.remove();
  }, 1000);
}

// Smooth animation for cursor glow
function animateCursorGlow() {
  glowX += (mouseX - glowX) * 0.08;
  glowY += (mouseY - glowY) * 0.08;
  
  cursorGlow.style.left = glowX + 'px';
  cursorGlow.style.top = glowY + 'px';
  
  requestAnimationFrame(animateCursorGlow);
}

// Smooth animation for cursor trail
function animateCursorTrail() {
  trailX += (mouseX - trailX) * 0.25;
  trailY += (mouseY - trailY) * 0.25;
  
  cursorTrail.style.left = trailX + 'px';
  cursorTrail.style.top = trailY + 'px';
  cursorTrail.style.transform = 'translate(-50%, -50%)';
  
  requestAnimationFrame(animateCursorTrail);
}

// Add click effect
document.addEventListener('click', (e) => {
  createLightRing(e.clientX, e.clientY);
  
  // Create burst of particles on click
  for (let i = 0; i < 8; i++) {
    setTimeout(() => {
      createLightParticle(e.clientX, e.clientY);
    }, i * 30);
  }
});

// Start cursor animations
animateCursorGlow();
animateCursorTrail();

const dashboardRoot = document.getElementById("dashboard-root");

const form = document.getElementById("task-form");
const input = document.getElementById("tasks-input");
const apiUrlInput = document.getElementById("api-url");
const scenarioSelect = document.getElementById("scenario-select");
const loadScenarioButton = document.getElementById("load-scenario");
const statusBox = document.getElementById("status");
const validationErrorsBox = document.getElementById("validation-errors");
const resultBox = document.getElementById("result");
const metricsSection = document.getElementById("metrics");
const metricTotal = document.getElementById("metric-total");
const metricPriority = document.getElementById("metric-priority");
const metricDuration = document.getElementById("metric-duration");
const resultTableBody = document.querySelector("#result-table tbody");
const proofStage = document.getElementById("proof-stage");
const proofScore = document.getElementById("proof-score");
const proofStrategy = document.getElementById("proof-strategy");
const judgeSummary = document.getElementById("judge-summary");
const benchmarkTemplate = document.getElementById("benchmark-template");
let uiBound = false;
const requiredElements = [
  form,
  input,
  apiUrlInput,
  scenarioSelect,
  loadScenarioButton,
  statusBox,
  validationErrorsBox,
  resultBox,
  metricsSection,
  metricTotal,
  metricPriority,
  metricDuration,
  resultTableBody,
  proofStage,
  proofScore,
  proofStrategy,
  judgeSummary,
  benchmarkTemplate,
];

const SCENARIOS = {
  balanced: [
    "Demo review,5,30",
    "Write slides,3,45",
    "Inbox cleanup,1,20",
  ],
  high_priority_burst: [
    "Production patch,5,25",
    "Incident postmortem,5,35",
    "Customer callback,4,20",
    "Backlog grooming,2,30",
  ],
  long_tail: [
    "Architecture RFC,4,90",
    "Tech debt cleanup,2,60",
    "Docs update,1,20",
    "QA rerun,3,45",
    "Sprint planning,2,50",
  ],
};

function loadScenario(name) {
  const rows = SCENARIOS[name] || SCENARIOS.balanced;
  input.value = rows.join("\n");
}

function clearResults() {
  resultBox.textContent = "";
  resultTableBody.innerHTML = "";
  metricsSection.hidden = true;
}

function parseTasks(rawText) {
  const parsedTasks = [];
  const displayTasks = [];
  const errors = [];
  const lines = rawText
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean);

  lines.forEach((line, index) => {
    const [titleRaw = "", priorityRaw = "1", durationRaw = "30"] = line.split(",");
    const title = titleRaw.trim();
    const priority = Number(priorityRaw.trim());
    const duration = Number(durationRaw.trim());

    if (!title) {
      errors.push(`Line ${index + 1}: title is required.`);
      return;
    }
    if (!Number.isFinite(priority) || priority < 1 || priority > 5) {
      errors.push(`Line ${index + 1}: priority must be between 1 and 5.`);
      return;
    }
    if (!Number.isFinite(duration) || duration < 1) {
      errors.push(`Line ${index + 1}: duration must be at least 1 minute.`);
      return;
    }

    parsedTasks.push({
      id: index + 1,
      duration,
      priority,
    });
    displayTasks.push({
      id: index + 1,
      title,
      priority,
      duration_minutes: duration,
    });
  });

  return { parsedTasks, displayTasks, errors };
}

function renderValidationErrors(errors) {
  if (errors.length === 0) {
    validationErrorsBox.textContent = "";
    return;
  }
  validationErrorsBox.innerHTML = errors.map((error) => `<p>${error}</p>`).join("");
}

function renderMetrics(orderedTasks) {
  const totalTasks = orderedTasks.length;
  const totalDuration = orderedTasks.reduce((sum, task) => sum + task.duration_minutes, 0);
  const avgPriority =
    totalTasks === 0
      ? 0
      : orderedTasks.reduce((sum, task) => sum + task.priority, 0) / totalTasks;

  metricTotal.textContent = String(totalTasks);
  metricPriority.textContent = avgPriority.toFixed(2);
  metricDuration.textContent = `${totalDuration} min`;
  metricsSection.hidden = false;
}

function renderOrderedTasks(orderedTasks) {
  resultTableBody.innerHTML = orderedTasks
    .map(
      (task, index) => `
      <tr>
        <td>${index + 1}</td>
        <td>${task.title}</td>
        <td>${task.priority}</td>
        <td>${task.duration_minutes}</td>
      </tr>
    `
    )
    .join("");
}

function detectStage(tasks) {
  const avgDuration =
    tasks.length === 0
      ? 0
      : tasks.reduce((sum, task) => sum + task.duration_minutes, 0) / tasks.length;
  const avgPriority =
    tasks.length === 0 ? 0 : tasks.reduce((sum, task) => sum + task.priority, 0) / tasks.length;

  if (tasks.length >= 5 || avgDuration > 55) return "Stage 3";
  if (tasks.length >= 4 || avgPriority >= 3.5) return "Stage 2";
  return "Stage 1";
}

function bindUiEvents() {
  if (requiredElements.some((element) => !element)) {
    console.error("TaskMesh UI init failed: one or more required elements were not found.");
    return;
  }

  loadScenario("balanced");
  statusBox.textContent = "UI loaded. Select a scenario and click Generate Schedule.";

  loadScenarioButton.addEventListener("click", () => {
    loadScenario(scenarioSelect.value);
    statusBox.textContent = "Scenario loaded. You can edit tasks before sending.";
    renderValidationErrors([]);
    clearResults();
  });

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const apiBase = apiUrlInput.value.trim().replace(/\/+$/, "");
    const { parsedTasks, displayTasks, errors } = parseTasks(input.value);

    renderValidationErrors(errors);
    clearResults();
    if (!apiBase) {
      statusBox.textContent = "Provide a valid API URL first.";
      return;
    }
    if (parsedTasks.length === 0) {
      statusBox.textContent = "Add at least one valid task line.";
      return;
    }
    if (errors.length > 0) {
      statusBox.textContent = "Fix validation errors before scheduling.";
      return;
    }

    statusBox.textContent = "Scheduling tasks...";

    try {
      const strategySelect = document.getElementById("strategy-select");
      const algorithm = strategySelect ? strategySelect.value : "rl";
      const response = await fetch(`${apiBase}/schedule`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ algorithm, tasks: parsedTasks }),
      });

      if (!response.ok) {
        throw new Error(`Request failed with status ${response.status}`);
      }

      const data = await response.json();
      const orderedTasks = (data.ordered_tasks || [])
        .map((taskId) => displayTasks.find((task) => task.id === Number(taskId)))
        .filter(Boolean);
      const stageLabel = detectStage(orderedTasks);

      statusBox.textContent = `Schedule ready. Score: ${data.score} (${data.strategy})`;
      proofStage.textContent = stageLabel;
      proofScore.textContent = String(data.score ?? "--");
      proofStrategy.textContent = data.strategy || "unknown";

      judgeSummary.textContent = `Completed ${stageLabel} with ${orderedTasks.length} tasks and scheduler score ${data.score}.`;
      benchmarkTemplate.textContent = "No benchmark loaded yet. Run benchmark.py and paste real results.";

      renderMetrics(orderedTasks);
      renderOrderedTasks(orderedTasks);
      resultBox.textContent = JSON.stringify(data, null, 2);
    } catch (error) {
      statusBox.textContent = "Could not reach the API. Check backend URL and make sure FastAPI is running.";
      resultBox.textContent = error instanceof Error ? error.message : String(error);
    }
  });
}

function showDashboard() {
  if (dashboardRoot) {
    dashboardRoot.hidden = false;
    dashboardRoot.style.display = 'block';
  }
}

function initDashboard() {
  showDashboard();
  if (!uiBound) {
    if (apiUrlInput) {
      apiUrlInput.value = window.location.origin;
    }
    bindUiEvents();
    uiBound = true;
  }
}


function bindCursorSpotlight() {
  const canvas = document.createElement("canvas");
  canvas.className = "fx-canvas";
  document.body.appendChild(canvas);

  const ctx = canvas.getContext("2d");
  if (!ctx) return;

  const particles = [];
  const particleCount = 120;
  let mouseX = window.innerWidth / 2;
  let mouseY = window.innerHeight / 2;

  function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  }

  function makeParticle() {
    return {
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      vx: (Math.random() - 0.5) * 0.7,
      vy: (Math.random() - 0.5) * 0.7,
      r: Math.random() * 1.8 + 0.6,
    };
  }

  for (let i = 0; i < particleCount; i += 1) {
    particles.push(makeParticle());
  }

  window.addEventListener("resize", resize);
  window.addEventListener("mousemove", (event) => {
    mouseX = event.clientX;
    mouseY = event.clientY;
  });

  function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    for (let i = 0; i < particles.length; i += 1) {
      const p = particles[i];
      const dx = mouseX - p.x;
      const dy = mouseY - p.y;
      const d2 = dx * dx + dy * dy;
      const influence = Math.min(0.00008 * d2, 0.22);
      p.vx += (Math.random() - 0.5) * 0.02 + (dx > 0 ? 0.001 : -0.001) * influence;
      p.vy += (Math.random() - 0.5) * 0.02 + (dy > 0 ? 0.001 : -0.001) * influence;
      p.vx *= 0.985;
      p.vy *= 0.985;
      p.x += p.vx;
      p.y += p.vy;

      if (p.x < 0 || p.x > canvas.width) p.vx *= -1;
      if (p.y < 0 || p.y > canvas.height) p.vy *= -1;

      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fillStyle = "rgba(255, 255, 255, 0.75)";
      ctx.fill();
    }

    requestAnimationFrame(draw);
  }

  resize();
  draw();
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", () => {
    bindCursorSpotlight();
    initDashboard();
  });
} else {
  bindCursorSpotlight();
  initDashboard();
}

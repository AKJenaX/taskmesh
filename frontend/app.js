const form = document.getElementById("task-form");
const input = document.getElementById("tasks-input");
const statusBox = document.getElementById("status");
const resultBox = document.getElementById("result");

input.value = [
  "Demo review,5,30",
  "Write slides,3,45",
  "Inbox cleanup,1,20",
].join("\n");

function parseTasks(rawText) {
  return rawText
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean)
    .map((line, index) => {
      const [title = "", priority = "1", duration = "30"] = line.split(",");
      return {
        id: `task-${index + 1}`,
        title: title.trim(),
        priority: Number(priority.trim()) || 1,
        duration_minutes: Number(duration.trim()) || 30,
        metadata: {},
      };
    })
    .filter((task) => task.title.length > 0);
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const tasks = parseTasks(input.value);
  if (tasks.length === 0) {
    statusBox.textContent = "Add at least one valid task line.";
    resultBox.textContent = "";
    return;
  }

  statusBox.textContent = "Scheduling tasks...";
  resultBox.textContent = "";

  try {
    const response = await fetch("http://localhost:8000/schedule", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ tasks }),
    });

    if (!response.ok) {
      throw new Error(`Request failed with status ${response.status}`);
    }

    const data = await response.json();
    statusBox.textContent = `Schedule ready. Score: ${data.score}`;
    resultBox.textContent = JSON.stringify(data, null, 2);
  } catch (error) {
    statusBox.textContent = "Could not reach the API. Make sure FastAPI is running on port 8000.";
    resultBox.textContent = error.message;
  }
});

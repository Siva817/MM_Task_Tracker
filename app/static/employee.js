// ===========================
// Get HTML Elements
// ===========================

// Buttons
const parseButton = document.getElementById("parseButton");
const submitButton = document.getElementById("submitButton");
const submitButtonText = document.getElementById("submitButtonText");
const submitSpinner = document.getElementById("submitSpinner");

// Dashboard input and task display
const dashboard = document.getElementById("dashboard");
const taskCount = document.getElementById("taskCount");
const taskList = document.getElementById("taskList");

// Manager selection
const managerDropdown = document.getElementById("manager");

// Idle section controls
const idleRadio = document.getElementById("idleRadio");
const idleSection = document.getElementById("idleSection");

// ===========================
// Manager List Setup
// ===========================


// Populate dropdown with manager names
async function loadManagers() {

    try {

        const response = await fetch("/employee/managers");

        const managers = await response.json();

        managers.forEach(manager => {

            const option = document.createElement("option");

            option.value = manager;
            option.textContent = manager;

            managerDropdown.appendChild(option);

        });

    } catch (error) {

        console.error("Failed to load managers:", error);

        alert("Unable to load manager list.");

    }

}

// ===========================
// Utility: Check if a line is a Task ID
// ===========================

function isTaskId(line) {
    line = line.trim();

    if (line === "") return false;

    // Task IDs are either:
    // 1. Start with "vs-"
    // 2. Start with digits (e.g., 260210-...)
    if (line.startsWith("vs-")) return true;
    if (/^\d/.test(line)) return true;

    return false;
}

// ===========================
// Parse Tasks from Dashboard Text
// ===========================

function parseTasks(text) {
    const lines = text.split("\n");
    const tasks = [];

    const ignoredValues = [
        "Start",
        "Audio",
        "Image",
        "Text",
        "Video"
    ];

    const seenTaskIds = new Set();

    // Start from line 1 (skip header)
    for (let i = 1; i < lines.length; i++) {
        const currentLine = lines[i].trim();

        // Skip non-task lines
        if (!isTaskId(currentLine)) continue;

        // Skip duplicate task IDs
        if (seenTaskIds.has(currentLine)) continue;

        // Find the nearest non-empty line above as task name
        let j = i - 1;
        while (j >= 0 && lines[j].trim() === "") j--;

        const taskName = lines[j].trim();

        // Remove markdown formatting if needed
        const cleanTaskName = taskName
            .replace(/^\*\*(.*?)\*\*$/, "$1")
            .replace(/^#+\s*/, "")
            .trim();

        // Skip ignored values
        if (ignoredValues.includes(cleanTaskName)) continue;

        // Remember task ID
        seenTaskIds.add(currentLine);

        // Push task object
        tasks.push({
            name: cleanTaskName,
            id: currentLine,
            assessment: false,
            status: "Not Working"
        });
    }

    return tasks;
}

// ===========================
// Toggle Idle Section Visibility
// ===========================

function updateIdleSection() {
    if (idleRadio.checked) {
        idleSection.style.display = "block";
    } else {
        idleSection.style.display = "none";
    }
    console.log("Display:", idleSection.style.display);
}

// ===========================
// Parse Button Click Handler
// ===========================

parseButton.addEventListener("click", function () {
    const pastedText = dashboard.value;

    // Validate input
    if (pastedText.trim() === "") {
        alert("Please paste your MM dashboard first.");
        return;
    }

    // Parse tasks
    const tasks = parseTasks(pastedText);

    // Update task count
    taskCount.innerText = `${tasks.length} Tasks Found`;

    // Clear previous list
    taskList.innerHTML = "";

    // Render tasks into table rows
    tasks.forEach(task => {
        taskList.innerHTML += `
            <tr class="taskRow"
                data-task-id="${task.id}"
                data-task-name="${task.name}">
                <td><input type="radio" name="currentTask" value="${task.id}"></td>
                <td><b>${task.name}</b></td>
                <td><label><input type="checkbox" class="sway"> Cleared</label></td>
                <td><label><input type="checkbox" class="mm"> Cleared</label></td>
                <td>
                    <select class="jobs">
                        <option>Not Checked</option>
                        <option>Jobs Available</option>
                        <option>Jobs Not Available</option>
                        <option>Error / Can't Work</option>
                    </select>
                </td>
                <td><input type="text" class="remarks" placeholder="Optional"></td>
            </tr>
        `;
    });
});

// ===========================
// Submit Button Click Handler
// ===========================

submitButton.addEventListener("click", async function () {

    // Validate Employee ID
    if (document.getElementById("employeeId").value.trim() === "") {
        alert("Please enter Employee ID.");
        document.getElementById("employeeId").focus();
        return;
    }

    // Validate Employee Name
    if (document.getElementById("employeeName").value.trim() === "") {
        alert("Please enter Employee Name.");
        document.getElementById("employeeName").focus();
        return;
    }

    // Validate manager selection
    if (managerDropdown.value === "") {
        alert("Please select your manager.");
        return;
    }

    const taskData = [];

    // Collect task data from rows
    document.querySelectorAll(".taskRow").forEach(row => {
        taskData.push({
            id: row.dataset.taskId,
            name: row.dataset.taskName,
            sway: row.querySelector(".sway").checked,
            mm: row.querySelector(".mm").checked,
            jobs: row.querySelector(".jobs").value,
            remarks: row.querySelector(".remarks").value
        });
    });

    // Find the currently selected radio button with name="currentTask"
    const selectedTask = document.querySelector("input[name='currentTask']:checked");

    // If a task is selected, get its value; otherwise set currentTask to null
    const currentTask = selectedTask ? selectedTask.value : null;

    // If no task is selected, alert the user and stop execution
    if (currentTask === null) {
        alert("Please select your current task or choose 'Idle'.");
        return;
    }

    // Check if the selected task is "idle"
    const idle = currentTask === "idle";

    // Build submission object
    const submission = {
        employeeId: document.getElementById("employeeId").value,
        employeeName: document.getElementById("employeeName").value,
        manager: managerDropdown.value,
        currentTask: currentTask,
        idle: idle,
        driveLink: document.getElementById("driveLink").value,
        idleRemarks: document.getElementById("idleRemarks").value,
        tasks: taskData
    };

    // Disable button immediately before sending the request
    submitButton.disabled = true;
    submitButton.textContent = "Submitting...";
    submitSpinner.hidden = false;

    try {
        // Send data to server
        const response = await fetch("/employee/submit", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(submission)
        });

        const result = await response.json();

        // Show existing success/error message
        alert(result.message);

        // Re-enable button after server response
        submitButton.disabled = false;
        submitButton.textContent = "Submit";
        submitSpinner.hidden = true;

    } catch (error) {
        console.error("Submission error:", error);

        alert("Unable to submit. Please try again.");

        // Re-enable button if request failed
        submitButton.disabled = false;
        submitButton.textContent = "Submit";
        submitSpinner.hidden = true;
    }
});


// ===========================
// Page Load Setup
// ===========================

// Hide idle section initially
updateIdleSection();

// Listen for task selection changes
document.addEventListener("change", function (event) {
    if (event.target.name === "currentTask") {
        updateIdleSection();
    }
});

loadManagers();
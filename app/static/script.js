// ===========================
// Get HTML Elements
// ===========================

const parseButton = document.getElementById("parseButton");
const submitButton = document.getElementById("submitButton");
const dashboard = document.getElementById("dashboard");
const taskCount = document.getElementById("taskCount");
const taskList = document.getElementById("taskList");
const managerDropdown = document.getElementById("manager");

// Manager List
const managers = ["Rahul", "Priya", "Arun"];

// Fill the dropdown with managers
managers.forEach(manager => {
    const option = document.createElement("option");
    option.value = manager;
    option.textContent = manager;
    managerDropdown.appendChild(option);
})


// ===========================
// Check if a line is a Task ID
// ===========================

function isTaskId(line) {

    line = line.trim();

    if (line === "") {
        return false;
    }

    // MM Task IDs are either:
    // 1. vs-xxxxxxxx...
    // 2. Start with digits (260210-..., etc.)

    if (line.startsWith("vs-")) {
        return true;
    }

    if (/^\d/.test(line)) {
        return true;
    }

    return false;
}


// ===========================
// Parse Tasks from MM Dashboard
// ===========================

function parseTasks(text) {

    const lines = text.split("\n");

    const tasks = [];

    for (let i = 1; i < lines.length; i++) {

        const currentLine = lines[i].trim();

        if (!isTaskId(currentLine)) {
            continue;
        }

        const taskName = lines[i - 1].trim();

        tasks.push({
            name: taskName,
            id: currentLine,
            assessment: false,
            status: "Not Working"
        });

    }

    return tasks;

}


// ===========================
// Parse Button Click
// ===========================

parseButton.addEventListener("click", function () {

    const pastedText = dashboard.value;

    //Manager Validation
    if (managerDropdown.value === "") {
        alert("Please select your manager.");
        return;
    }

    if (pastedText.trim() === "") {
        alert("Please paste your MM dashboard first.");
        return;
    }

    const tasks = parseTasks(pastedText);

    console.log(tasks);

    taskCount.innerText = `${tasks.length} Tasks Found`;

    taskList.innerHTML = "";

    tasks.forEach(task => {

        taskList.innerHTML += `
        

    <tr>

        <td>
            <input
                type="radio"
                name="currentTask"
                value="${task.id}">
        </td>

        <td>

            <b>${task.name}</b>

        </td>

        <td>

            <label>

                <input
                    type="checkbox"
                    class="sway">

                Cleared

            </label>

        </td>

        <td>

            <label>

                <input
                    type="checkbox"
                    class="mm">

                Cleared

            </label>

        </td>

        <td>

            <select class="jobs">

                <option>Not Checked</option>

                <option>Jobs Available</option>

                <option>Jobs Not Available</option>

                <option>Error / Can't Work</option>

            </select>

        </td>

        <td>

            <input
                type="text"
                class="remarks"
                placeholder="Optional">

        </td>

    </tr>

    
        `;

    });

});

submitButton.addEventListener("click", function (){
    alert("Submit feature coming soon!");

});




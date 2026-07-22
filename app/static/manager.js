document.addEventListener("DOMContentLoaded", function () {
    /*
    ==================================================
    DASHBOARD DATA
    ==================================================
    */
    const dashboardData = window.managerDashboardData || {};
    const idleCount = dashboardData.idle || 0;
    const productionCount = dashboardData.production || 0;
    const taskVisibility = dashboardData.taskVisibility || [];

    /*
    ==================================================
    STATUS DOUGHNUT CHART
    ==================================================
    */
    const statusChartElement = document.getElementById("statusChart");

    if (statusChartElement) {
        new Chart(statusChartElement, {
            type: "doughnut",
            data: {
                labels: ["Idle", "Production"],
                datasets: [{ data: [idleCount, productionCount] }],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: "bottom" },
                    title: { display: true, text: "Idle vs Production" },
                },
            },
        });
    }

    /*
    ==================================================
    TASK VISIBILITY CHART
    ==================================================
    */
    const taskChartElement = document.getElementById("taskVisibilityChart");

    if (taskChartElement) {
        const taskLabels = taskVisibility.map(task => task.taskId);
        const employeeCounts = taskVisibility.map(task => task.employeeCount);

        new Chart(taskChartElement, {
            type: "bar",
            data: {
                labels: taskLabels,
                datasets: [{ label: "Employees", data: employeeCounts }],
            },
            options: {
                indexAxis: "y",
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    title: { display: true, text: "Task Visibility" },
                },
                scales: {
                    x: { beginAtZero: true, ticks: { stepSize: 1 } },
                },
            },
        });
    }

    /*
    ==================================================
    FILTERS
    ==================================================
    */
    const managerFilter = document.getElementById("managerFilter");
    const dateFilter = document.getElementById("dateFilter");
    const taskStatusFilter = document.getElementById("taskStatusFilter");

    /*
    ==================================================
    APPLY FILTERS
    ==================================================
    */
    function applyFilters() {
        const selectedManager = managerFilter.value;
        const selectedDate = dateFilter.value;
        const selectedTaskStatus =taskStatusFilter.value;

        const params = new URLSearchParams();

        if (selectedManager !== "All") params.set("selected_manager", selectedManager);
        if (selectedDate !== "") params.set("selected_date", selectedDate);
        if (selectedTaskStatus !== "All") params.set("task_status", selectedTaskStatus);

        const queryString = params.toString();
        window.location.href = queryString ? `/manager?${queryString}` : "/manager";
    }

    if (managerFilter) { managerFilter.addEventListener("change", applyFilters);}
    if (dateFilter) { dateFilter.addEventListener("change", applyFilters);}

    /*
    ==================================================
    TABLE TOGGLE
    ==================================================
    */
    const toggleTableButton = document.getElementById("toggleTableButton");
    const employeeTableContainer = document.getElementById("employeeTableContainer");

    if (toggleTableButton && employeeTableContainer) {
        toggleTableButton.addEventListener("click", function () {
            employeeTableContainer.classList.toggle("hidden");

            const tableIsHidden = employeeTableContainer.classList.contains("hidden");
            toggleTableButton.textContent = tableIsHidden ? "Show Employee Table" : "Hide Employee Table";

            if (!tableIsHidden) {
                setTimeout(() => {
                    employeeTableContainer.scrollIntoView({ behavior: "smooth", block: "start" });
                }, 100);
            }
        });
    }

    /*
    ==================================================
    TASK VISIBILITY LOOKUP
    ==================================================
    */
    const lookupEmployeeRadio = document.querySelector('input[name="lookupType"][value="employee"]');
    const lookupTaskRadio = document.querySelector('input[name="lookupType"][value="task"]');
    const employeeIdLookup = document.getElementById("employeeIdLookup");
    const taskIdLookup = document.getElementById("taskIdLookup");
    const lookupEmployeeId = document.getElementById("lookupEmployeeId");
    const lookupTaskId = document.getElementById("lookupTaskId");
    const lookupFetchButton = document.getElementById("lookupFetchButton");
    const lookupClearButton = document.getElementById("lookupClearButton");
    const lookupResultsSection = document.getElementById("lookupResultsSection");
    const lookupResultsTitle = document.getElementById("lookupResultsTitle");
    const lookupResultsHead = document.getElementById("lookupResultsHead");
    const lookupResultsBody = document.getElementById("lookupResultsBody");

    // Switch between Employee ID / Task ID
    lookupEmployeeRadio.addEventListener("change", function () {
        employeeIdLookup.style.display = "block";
        taskIdLookup.style.display = "none";
        lookupTaskId.value = "";
        lookupResultsSection.style.display = "none";
    });

    lookupTaskRadio.addEventListener("change", function () {
        employeeIdLookup.style.display = "none";
        taskIdLookup.style.display = "block";
        lookupEmployeeId.value = "";
        lookupResultsSection.style.display = "none";
    });

    // Fetch Lookup Data
    lookupFetchButton.addEventListener("click", async function () {
        const selectedManager = managerFilter.value;
        const isEmployeeSearch = lookupEmployeeRadio.checked;
        let lookupValue;

        if (isEmployeeSearch) {
            lookupValue = lookupEmployeeId.value.trim();
            if (!lookupValue) return alert("Please enter an Employee ID.");
        } else {
            lookupValue = lookupTaskId.value.trim();
            if (!lookupValue) return alert("Please enter a Task ID.");
        }

        const params = new URLSearchParams();
        params.append("lookup_type", isEmployeeSearch ? "employee" : "task");
        if (selectedManager !== "All") params.append("selected_manager", selectedManager);
        if (isEmployeeSearch) params.append("employee_id", lookupValue);
        else params.append("task_id", lookupValue);

        const response = await fetch("/manager/lookup?" + params.toString());
        if (!response.ok) return alert("Failed to fetch lookup data.");

        const data = await response.json();
        lookupResultsHead.innerHTML = "";
        lookupResultsBody.innerHTML = "";

        if (isEmployeeSearch) {
            lookupResultsTitle.textContent = "Latest Visible Tasks";
            lookupResultsHead.innerHTML = `
                <tr>
                    <th>Task ID</th>
                    <th>Task Name</th>
                    <th>Jobs</th>
                    <th>Remarks</th>
                    <th>Submitted At</th>
                </tr>
            `;
            data.forEach(row => {
                lookupResultsBody.innerHTML += `
                    <tr>
                        <td>${row.task_id}</td>
                        <td>${row.task_name}</td>
                        <td>${row.jobs || ""}</td>
                        <td>${row.remarks || ""}</td>
                        <td>${row.submitted_at}</td>
                    </tr>
                `;
            });
        } else {
            lookupResultsTitle.textContent = "Employees with Task Visible";
            lookupResultsHead.innerHTML = `
                <tr>
                    <th>Employee ID</th>
                    <th>Employee Name</th>
                    <th>Last Log Time</th>
                </tr>
            `;
            data.forEach(row => {
                lookupResultsBody.innerHTML += `
                    <tr>
                        <td>${row.employee_id}</td>
                        <td>${row.employee_name.replace(/\b\w/g, c => c.toUpperCase())}</td>
                        <td>${row.last_log_time}</td>
                    </tr>
                `;
            });
        }

        lookupResultsSection.style.display = "block";
    });

    // Clear Lookup
    lookupClearButton.addEventListener("click", function () {
        lookupEmployeeId.value = "";
        lookupTaskId.value = "";
        lookupResultsHead.innerHTML = "";
        lookupResultsBody.innerHTML = "";
        lookupResultsSection.style.display = "none";
    });

    /*
    ==================================================
    IDLE EMPLOYEES TABLE TOGGLE
    ==================================================
    */
    const toggleIdleEmployeesButton = document.getElementById("toggleIdleEmployeesButton");
    const idleEmployeesSection = document.getElementById("idleEmployeesSection");

    toggleIdleEmployeesButton.addEventListener("click", function () {
        if (idleEmployeesSection.style.display === "none") {
            idleEmployeesSection.style.display = "block";
            toggleIdleEmployeesButton.textContent = "Hide Idle Employees";
        } else {
            idleEmployeesSection.style.display = "none";
            toggleIdleEmployeesButton.textContent = "Show Idle Employees";
        }
    });

    // =====================================
    // Task Status Report Script
    // =====================================

    // Get references to DOM elements
    const fetchTaskStatusButton = document.getElementById("fetchTaskStatusButton");
    const hideTaskStatusButton = document.getElementById("hideTaskStatusButton");
    const taskStatusTableSection = document.getElementById("taskStatusTableSection");
    const taskStatusTableBody = document.querySelector("#taskStatusTable tbody");

    // =====================================
    // Fetch and Show Task Status Table
    // =====================================
    if (fetchTaskStatusButton) {
        fetchTaskStatusButton.addEventListener("click", async function () {
            console.log("Task status button clicked");

            // Get current filter values
            const selectedManager = managerFilter.value;
            const selectedDate = dateFilter.value;
            const selectedTaskStatus = taskStatusFilter.value;

            // Build API parameters
            const params = new URLSearchParams();

            if (selectedManager !== "All") {
                params.set("selected_manager", selectedManager);
            }

            if (selectedDate !== "") {
                params.set("selected_date", selectedDate);
            }

            if (selectedTaskStatus !== "None") {
                params.set("task_status", selectedTaskStatus);
            }

            console.log("Fetching:", "/manager/task-status-report?" + params.toString());

            try {
                // Fetch filtered data from API
                const response = await fetch("/manager/task-status-report?" + params.toString());

                if (!response.ok) {
                    const errorText = await response.text();
                    console.error("Task status API failed:", response.status, errorText);
                    throw new Error(`Task status API failed: ${response.status}`);
                }

                const data = await response.json();
                console.log("Task status report:", data);

                // Clear old table rows
                taskStatusTableBody.innerHTML = "";

                // Generate new rows from API data
                data.forEach(function (task) {
                    const row = document.createElement("tr");

                    const taskIdCell = document.createElement("td");
                    taskIdCell.textContent = task.task_id;

                    const employeeCountCell = document.createElement("td");
                    employeeCountCell.textContent = task.employee_count;

                    row.appendChild(taskIdCell);
                    row.appendChild(employeeCountCell);

                    taskStatusTableBody.appendChild(row);
                });

                // Show table section
                taskStatusTableSection.style.display = "block";

                // Smooth scroll to table
                setTimeout(function () {
                    taskStatusTableSection.scrollIntoView({
                        behavior: "smooth",
                        block: "start"
                    });
                }, 100);

            } catch (error) {
                console.error("Task status error:", error);
                alert("Failed to load task status report.");
            }
        });
    }

    // =====================================
    // Hide Task Status Table
    // =====================================
    if (hideTaskStatusButton) {
        hideTaskStatusButton.addEventListener("click", function () {
            // Hide the table section
            taskStatusTableSection.style.display = "none";
        });
    }


});

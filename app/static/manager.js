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
                datasets: [
                    {
                        data: [idleCount, productionCount]
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: "bottom" },
                    title: {
                        display: true,
                        text: "Idle vs Production"
                    }
                }
            }
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
                datasets: [
                    {
                        label: "Employees",
                        data: employeeCounts
                    }
                ]
            },
            options: {
                indexAxis: "y",
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    title: {
                        display: true,
                        text: "Task Visibility"
                    }
                },
                scales: {
                    x: {
                        beginAtZero: true,
                        ticks: { stepSize: 1 }
                    }
                }
            }
        });
    }

    /*
    ==================================================
    FILTERS
    ==================================================
    */
    const managerFilter = document.getElementById("managerFilter");
    const dateFilter = document.getElementById("dateFilter");

    /*
    ==================================================
    APPLY FILTERS
    ==================================================
    */
    function applyFilters() {
        const selectedManager = managerFilter.value;
        const selectedDate = dateFilter.value;
        const params = new URLSearchParams();

        // Manager
        if (selectedManager !== "All") {
            params.set("selected_manager", selectedManager);
        }

        // Date
        if (selectedDate !== "") {
            params.set("selected_date", selectedDate);
        }

        // Redirect
        const queryString = params.toString();
        window.location.href = queryString ? `/manager?${queryString}` : "/manager";
    }

    /*
    ==================================================
    MANAGER FILTER
    ==================================================
    */
    if (managerFilter) {
        managerFilter.addEventListener("change", applyFilters);
    }

    /*
    ==================================================
    DATE FILTER
    ==================================================
    */
    if (dateFilter) {
        dateFilter.addEventListener("change", applyFilters);
    }

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

            // Scroll down to the table when shown
            if (!tableIsHidden) {
                setTimeout(() => {
                    employeeTableContainer.scrollIntoView({
                        behavior: "smooth",
                        block: "start"
                    });
                }, 100);
            }
        });
    }

    // =====================================
    // Task Visibility Lookup
    // =====================================

    const lookupEmployeeRadio =
        document.querySelector(
            'input[name="lookupType"][value="employee"]'
        );

    const lookupTaskRadio =
        document.querySelector(
            'input[name="lookupType"][value="task"]'
        );

    const employeeIdLookup =
        document.getElementById(
            "employeeIdLookup"
        );

    const taskIdLookup =
        document.getElementById(
            "taskIdLookup"
        );

    const lookupEmployeeId =
        document.getElementById(
            "lookupEmployeeId"
        );

    const lookupTaskId =
        document.getElementById(
            "lookupTaskId"
        );

    const lookupFetchButton =
        document.getElementById(
            "lookupFetchButton"
        );

    const lookupClearButton =
        document.getElementById(
            "lookupClearButton"
        );

    const lookupResultsSection =
        document.getElementById(
            "lookupResultsSection"
        );

    const lookupResultsTitle =
        document.getElementById(
            "lookupResultsTitle"
        );

    const lookupResultsHead =
        document.getElementById(
            "lookupResultsHead"
        );

    const lookupResultsBody =
        document.getElementById(
            "lookupResultsBody"
        );


    // =====================================
    // Switch Between Employee ID / Task ID
    // =====================================

    lookupEmployeeRadio.addEventListener(
        "change",
        function () {

            employeeIdLookup.style.display =
                "block";

            taskIdLookup.style.display =
                "none";

            lookupTaskId.value = "";

            lookupResultsSection.style.display =
                "none";

        }
    );


    lookupTaskRadio.addEventListener(
        "change",
        function () {

            employeeIdLookup.style.display =
                "none";

            taskIdLookup.style.display =
                "block";

            lookupEmployeeId.value = "";

            lookupResultsSection.style.display =
                "none";

        }
    );


    // =====================================
    // Fetch Lookup Data
    // =====================================

    lookupFetchButton.addEventListener(
        "click",
        async function () {

            const selectedManager =
                managerFilter.value;

            const isEmployeeSearch =
                lookupEmployeeRadio.checked;


            let lookupValue;


            if (isEmployeeSearch) {

                lookupValue =
                    lookupEmployeeId.value.trim();

                if (!lookupValue) {

                    alert(
                        "Please enter an Employee ID."
                    );

                    return;

                }

            } else {

                lookupValue =
                    lookupTaskId.value.trim();

                if (!lookupValue) {

                    alert(
                        "Please enter a Task ID."
                    );

                    return;

                }

            }


            const params =
                new URLSearchParams();


            params.append(
                "lookup_type",
                isEmployeeSearch
                    ? "employee"
                    : "task"
            );


            if (
                selectedManager !== "All"
            ) {

                params.append(
                    "selected_manager",
                    selectedManager
                );

            }


            if (isEmployeeSearch) {

                params.append(
                    "employee_id",
                    lookupValue
                );

            } else {

                params.append(
                    "task_id",
                    lookupValue
                );

            }


            const response =
                await fetch(
                    "/manager/lookup?" +
                    params.toString()
                );


            if (!response.ok) {

                alert(
                    "Failed to fetch lookup data."
                );

                return;

            }


            const data =
                await response.json();


            lookupResultsHead.innerHTML =
                "";

            lookupResultsBody.innerHTML =
                "";


            if (isEmployeeSearch) {

                lookupResultsTitle.textContent =
                    "Latest Visible Tasks";


                lookupResultsHead.innerHTML = `
                    <tr>
                        <th>Task ID</th>
                        <th>Task Name</th>
                        <th>Jobs</th>
                        <th>Remarks</th>
                        <th>Submitted At</th>
                    </tr>
                `;


                data.forEach(
                    function (row) {

                        lookupResultsBody.innerHTML += `
                            <tr>
                                <td>${row.task_id}</td>
                                <td>${row.task_name}</td>
                                <td>${row.jobs || ""}</td>
                                <td>${row.remarks || ""}</td>
                                <td>${row.submitted_at}</td>
                            </tr>
                        `;

                    }
                );

            } else {

                lookupResultsTitle.textContent =
                    "Employees with Task Visible";


                lookupResultsHead.innerHTML = `
                    <tr>
                        <th>Employee ID</th>
                        <th>Employee Name</th>
                        <th>Last Log Time</th>
                    </tr>
                `;


                data.forEach(
                    function (row) {

                        lookupResultsBody.innerHTML += `
                            <tr>
                                <td>${row.employee_id}</td>
                                <td>${row.employee_name.replace(/\b\w/g, c => c.toUpperCase())}</td>
                                <td>${row.last_log_time}</td>
                            </tr>
                        `;

                    }
                );

            }


            lookupResultsSection.style.display =
                "block";

        }
    );


    // =====================================
    // Clear Lookup
    // =====================================

    lookupClearButton.addEventListener(
        "click",
        function () {

            lookupEmployeeId.value =
                "";

            lookupTaskId.value =
                "";

            lookupResultsHead.innerHTML =
                "";

            lookupResultsBody.innerHTML =
                "";

            lookupResultsSection.style.display =
                "none";

        }
    );




});

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
});

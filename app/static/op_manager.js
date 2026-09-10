document.addEventListener("DOMContentLoaded", function () {

    const charts = document.querySelectorAll(".manager-chart");

    charts.forEach(function (canvas) {

        const idle = Number(canvas.dataset.idle || 0);
        const production = Number(canvas.dataset.production || 0);

        new Chart(canvas, {
            type: "doughnut",
            data: {
                labels: ["Idle", "Production"],
                datasets: [{
                    data: [idle, production]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });

    });


    window.applyDate = function () {

        const selectedDate =
            document.getElementById("selected-date").value;

        const params = new URLSearchParams();

        if (selectedDate !== "") {
            params.set("selected_date", selectedDate);
        }

        const queryString = params.toString();

        window.location.href =
            queryString
                ? `/op-manager?${queryString}`
                : "/op-manager";
    };


    window.exportCSV = function () {

        const table = document.getElementById("manager-table");

        if (!table) {
            console.error("Manager table not found.");
            return;
        }

        const rows = table.querySelectorAll("tr");
        const csv = [];

        rows.forEach(function (row) {

            const cells = row.querySelectorAll("th, td");

            const rowData = Array.from(cells)
                .filter(function (cell, index) {
                    return index !== 1;
                })
                .map(function (cell) {
                    const value = cell.innerText
                        .replace(/"/g, '""');

                    return `"${value}"`;
                });

            csv.push(rowData.join(","));
        });


        const csvContent = csv.join("\n");

        const blob = new Blob(
            [csvContent],
            { type: "text/csv;charset=utf-8;" }
        );

        const url = URL.createObjectURL(blob);

        const now = new Date();

        const timestamp =
            now.getFullYear() + "-" +
            String(now.getMonth() + 1).padStart(2, "0") + "-" +
            String(now.getDate()).padStart(2, "0") + "_" +
            String(now.getHours()).padStart(2, "0") + "-" +
            String(now.getMinutes()).padStart(2, "0") + "-" +
            String(now.getSeconds()).padStart(2, "0");

        const selectedDate =
            document.getElementById("selected-date").value ||
            "all";

        const link = document.createElement("a");

        link.href = url;

        link.download =
            `OP_Manager_${selectedDate}_${timestamp}.csv`;

        document.body.appendChild(link);

        link.click();

        document.body.removeChild(link);

        URL.revokeObjectURL(url);
    };

    const sortButtons = document.querySelectorAll(".sort-button");

    sortButtons.forEach(function (button) {

        button.addEventListener("click", function () {

            const column = Number(button.dataset.column);
            const type = button.dataset.type;
            const table = document.getElementById("manager-table");
            const tbody = table.querySelector("tbody");

            const rows = Array.from(tbody.querySelectorAll("tr"));

            const currentDirection =
                button.dataset.direction || "none";

            const newDirection =
                currentDirection === "asc" ? "desc" : "asc";

            sortButtons.forEach(function (otherButton) {
                otherButton.dataset.direction = "none";
                otherButton.textContent =
                    otherButton.textContent.replace(/ [↑↓]$/, "");
            });

            button.dataset.direction = newDirection;

            const arrow =
                newDirection === "asc" ? " ↑" : " ↓";

            button.textContent =
                button.textContent.replace(/ [↑↓]$/, "") + arrow;


            rows.sort(function (rowA, rowB) {

                const valueA =
                    rowA.cells[column].innerText.trim();

                const valueB =
                    rowB.cells[column].innerText.trim();

                if (type === "number") {
                    return newDirection === "asc"
                        ? Number(valueA) - Number(valueB)
                        : Number(valueB) - Number(valueA);
                }

                return newDirection === "asc"
                    ? valueA.localeCompare(valueB)
                    : valueB.localeCompare(valueA);
            });


            rows.forEach(function (row) {
                tbody.appendChild(row);
            });

        });

    });

});
document.addEventListener("DOMContentLoaded", function () {
    const monthlyData = document.getElementById("dashboard-chart-data");
    const analyticsData = document.getElementById("analytics-data");

    if (typeof Chart === "undefined") {
        return;
    }

    const parseDataset = function (value, fallback) {
        try {
            const parsed = JSON.parse(value || "[]");
            return Array.isArray(parsed) ? parsed : fallback;
        } catch (error) {
            return fallback;
        }
    };

    const monthlyLabels = parseDataset(monthlyData?.dataset.monthlyLabels || "[]", []);
    const monthlyValues = parseDataset(monthlyData?.dataset.monthlyValues || "[]", []);

    const accountLabels = parseDataset(analyticsData?.dataset.accountLabels || "[]", []);
    const accountValues = parseDataset(analyticsData?.dataset.accountValues || "[]", []);
    const departmentLabels = parseDataset(analyticsData?.dataset.departmentLabels || "[]", []);
    const departmentValues = parseDataset(analyticsData?.dataset.departmentValues || "[]", []);
    const loanLabels = parseDataset(analyticsData?.dataset.loanLabels || "[]", []);
    const loanValues = parseDataset(analyticsData?.dataset.loanValues || "[]", []);

    const commonOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: "top",
                labels: {
                    usePointStyle: true,
                    color: "#334155",
                    padding: 16,
                    boxWidth: 10
                }
            },
            tooltip: {
                backgroundColor: "#0F172A",
                titleColor: "#fff",
                bodyColor: "#fff",
                padding: 10,
                cornerRadius: 8
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                ticks: {
                    color: "#64748b",
                    precision: 0
                },
                grid: {
                    color: "rgba(15, 23, 42, 0.08)"
                }
            },
            x: {
                ticks: {
                    color: "#64748b"
                },
                grid: {
                    display: false
                }
            }
        }
    };

    if (document.getElementById("monthlyChart") && monthlyLabels.length && monthlyValues.length) {
        new Chart(document.getElementById("monthlyChart"), {
            type: "bar",
            data: {
                labels: monthlyLabels,
                datasets: [{
                    label: "Transactions",
                    data: monthlyValues,
                    backgroundColor: "rgba(37, 99, 235, 0.16)",
                    borderColor: "#2563EB",
                    borderWidth: 2,
                    borderRadius: 6
                }]
            },
            options: commonOptions
        });
    }

    if (document.getElementById("accountTypeChart") && accountLabels.length && accountValues.length) {
        new Chart(document.getElementById("accountTypeChart"), {
            type: "doughnut",
            data: {
                labels: accountLabels,
                datasets: [{
                    data: accountValues,
                    backgroundColor: ["#2563EB", "#1E3A8A", "#38bdf8", "#16a34a"],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: "bottom",
                        labels: {
                            color: "#334155",
                            padding: 12
                        }
                    },
                    tooltip: {
                        backgroundColor: "#0F172A",
                        bodyColor: "#fff",
                        padding: 10,
                        cornerRadius: 8
                    }
                }
            }
        });
    }

    if (document.getElementById("departmentChart") && departmentLabels.length && departmentValues.length) {
        new Chart(document.getElementById("departmentChart"), {
            type: "pie",
            data: {
                labels: departmentLabels,
                datasets: [{
                    data: departmentValues,
                    backgroundColor: ["#2563EB", "#1E3A8A", "#38bdf8", "#16a34a", "#f59e0b"],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: "bottom",
                        labels: {
                            color: "#334155",
                            padding: 12
                        }
                    },
                    tooltip: {
                        backgroundColor: "#0F172A",
                        bodyColor: "#fff",
                        padding: 10,
                        cornerRadius: 8
                    }
                }
            }
        });
    }

    if (document.getElementById("loanStatusChart") && loanLabels.length && loanValues.length) {
        new Chart(document.getElementById("loanStatusChart"), {
            type: "bar",
            data: {
                labels: loanLabels,
                datasets: [{
                    label: "Loans",
                    data: loanValues,
                    backgroundColor: ["#2563EB", "#16a34a", "#f59e0b", "#dc2626"],
                    borderWidth: 0,
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: "#0F172A",
                        bodyColor: "#fff",
                        padding: 10,
                        cornerRadius: 8
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            color: "#64748b",
                            precision: 0
                        },
                        grid: {
                            color: "rgba(15, 23, 42, 0.08)"
                        }
                    },
                    x: {
                        ticks: {
                            color: "#64748b"
                        },
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });
    }
});

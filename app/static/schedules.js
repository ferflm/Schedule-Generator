document.addEventListener("DOMContentLoaded", async () => {
    const urlParams = new URLSearchParams(window.location.search);
    const sessionId = urlParams.get("session_id");

    if (!sessionId) {
        alert("No se encontró una sesión activa.");
        return;
    }

    try {
        // Obtener horarios del backend
        const response = await fetch("/api/schedules", {
            method: "GET",
            headers: { "Session-Id": sessionId },
        });

        if (response.ok) {
            const data = await response.json();
            renderSchedules(data.schedules);
        } else {
            const error = await response.json();
            alert(`Error al generar horarios: ${error.error}`);
        }
    } catch (error) {
        console.error("Error al conectarse al servidor:", error);
    }
});

// Renderizar horarios en tablas
function renderSchedules(schedules) {
    const container = document.getElementById("schedulesContainer");

    if (schedules.length === 0) {
        container.innerHTML = "<p>No se encontraron horarios válidos.</p>";
        return;
    }

    schedules.forEach((schedule, index) => {
        const table = document.createElement("table");
        table.classList.add("schedule-table");

        // Filas de datos
        schedule.schedule.forEach(option => {
            const row = document.createElement("tr");
            row.innerHTML = 
                `<td>
                    <strong>${option.professor}</strong> (${option.group})
                    <br>Días: ${option.days.join(", ")}
                    <br>Horario: ${option.time}
                    <br>Preferencia: ${option.preference}
                </td>`;
            table.appendChild(row);
        });

        // Título del horario
        const scheduleTitle = document.createElement("h2");
        scheduleTitle.textContent = `Horario ${index + 1}`;

        // Agregar al contenedor
        container.appendChild(scheduleTitle);
        container.appendChild(table);
    });
}

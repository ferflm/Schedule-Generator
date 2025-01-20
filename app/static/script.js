document.addEventListener("DOMContentLoaded", async () => {
    // Crear o recuperar la sesión
    let sessionId = localStorage.getItem("session_id");

    if (!sessionId) {
        try {
            const response = await fetch("/api/session", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
            });

            if (response.ok) {
                const data = await response.json();
                sessionId = data.session_id;
                localStorage.setItem("session_id", sessionId);
                console.log(`Sesión creada: ${sessionId}`);
            } else {
                console.error("Error al crear la sesión.");
            }
        } catch (error) {
            console.error("Error al conectarse al servidor:", error);
        }
    } else {
        console.log(`Sesión existente: ${sessionId}`);
    }

    // Cargar materias al cargar la página
    loadSubjects();

    // Manejar el evento de envío del formulario de materias
    const subjectForm = document.getElementById("subjectForm");
    subjectForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const sessionId = localStorage.getItem("session_id");
        if (!sessionId) {
            alert("No hay una sesión activa.");
            return;
        }

        const subjectName = subjectForm.querySelector("input[type='text']").value;
        if (!subjectName) {
            alert("El nombre de la materia es obligatorio.");
            return;
        }

        try {
            const response = await fetch("/api/subjects", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Session-Id": sessionId,
                },
                body: JSON.stringify({ name: subjectName }),
            });

            if (response.ok) {
                alert("Materia agregada correctamente.");
                subjectForm.reset();
                loadSubjects();
            } else {
                const error = await response.json();
                alert(`Error: ${error.error}`);
            }
        } catch (error) {
            console.error("Error al enviar la solicitud:", error);
        }
    });

    // Manejar selección de días en la tabla
    const daysTable = document.getElementById("tblDays");
    daysTable.addEventListener("click", (e) => {
        if (e.target.tagName === "TD") {
            e.target.classList.toggle("selected");
        }
    });

    // Manejar el evento de envío del formulario de opciones
const optionsForm = document.querySelector("#optionsSect .optionsForm");  // Usamos el selector correcto
optionsForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const sessionId = localStorage.getItem("session_id");
    if (!sessionId) {
        alert("No hay una sesión activa.");
        return;
    }

    const subjectId = document.getElementById("subjectSelect").value;
    const professor = document.getElementById("professor").value;
    const groupName = document.getElementById("groupName").value;
    const preference = document.getElementById("preference").value || 0;

    const selectedDays = Array.from(document.querySelectorAll("#tblDays td.selected"))
        .map(td => td.dataset.day)
        .join(" ");
    if (!selectedDays) {
        alert("Por favor, selecciona al menos un día.");
        return;
    }

    const startTime = document.getElementById("startTime").value;
    const endTime = document.getElementById("endTime").value;
    if (!startTime || !endTime) {
        alert("Por favor, selecciona un horario válido.");
        return;
    }

    const time = `${startTime} - ${endTime}`;

    try {
        const response = await fetch(`/api/subjects/${subjectId}/options`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Session-Id": sessionId,
            },
            body: JSON.stringify({
                professor,
                group_name: groupName,
                days: selectedDays,
                time,
                preference: parseInt(preference, 10),
            }),
        });

        if (response.ok) {
            alert("Opción agregada correctamente.");
            optionsForm.reset();
            Array.from(document.querySelectorAll("#tblDays td.selected"))
                .forEach(td => td.classList.remove("selected"));
            
            loadSubjects();
        } else {
            const error = await response.json();
            alert(`Error: ${error.error}`);
        }
    } catch (error) {
        console.error("Error al enviar la solicitud:", error);
    }
});


    const generateButton = document.getElementById("generateSchedulesButton");
    generateButton.addEventListener("click", () => {
        const sessionId = localStorage.getItem("session_id");
        if (!sessionId) {
            alert("No hay una sesión activa.");
            return;
        }

        // Redirigir a la página de horarios con el session_id en la URL
        window.location.href = `/schedules.html?session_id=${sessionId}`;
    });
});

// Función para cargar materias en el campo select
async function loadSubjects() {
    const sessionId = localStorage.getItem("session_id");
    if (!sessionId) {
        alert("No hay una sesión activa. Por favor, recarga la página.");
        return;
    }

    try {
        const response = await fetch("/api/subjects", {
            headers: { "Session-Id": sessionId },
        });

        if (response.ok) {
            const subjects = await response.json();
            renderSubjectSelect(subjects);
            renderSubjectsTable(subjects);
        } else {
            console.error("Error al cargar las materias.");
        }
    } catch (error) {
        console.error("Error al conectarse al servidor:", error);
    }
}

// Función para renderizar las materias en el campo <select>
function renderSubjectSelect(subjects) {
    const subjectSelect = document.getElementById("subjectSelect");
    subjectSelect.innerHTML = ""; // Limpiar el select

    subjects.forEach((subject) => {
        const option = document.createElement("option");
        option.value = subject.id;
        option.textContent = subject.name;
        subjectSelect.appendChild(option);
    });
}

function renderSubjectsTable(subjects) {
    const subjectsTable = document.getElementById("subjectsTbl");

    // Limpiar la tabla, dejando solo la fila de encabezado
    subjectsTable.innerHTML = `
        <tr>
            <th>Subjects</th>
            <th>Options</th>
            <th>Actions</th>
        </tr>
    `;

    subjects.forEach((subject) => {
        // Crear la primera fila para la materia
        const subjectRow = document.createElement("tr");

        // Celda para el nombre de la materia
        const subjectCell = document.createElement("td");
        subjectCell.rowSpan = Math.max(subject.options.length, 1); // Expandir según las opciones disponibles
        subjectCell.textContent = subject.name;

        // Botón para eliminar toda la materia y sus opciones
        const deleteSubjectButton = document.createElement("button");
        deleteSubjectButton.textContent = "Delete Subject";
        deleteSubjectButton.addEventListener("click", async () => {
            try {
                const response = await fetch(`/api/subjects/${subject.id}`, {
                    method: "DELETE",
                    headers: { "Session-Id": localStorage.getItem("session_id") },
                });

                if (response.ok) {
                    alert("Materia eliminada correctamente.");
                    loadSubjects(); // Actualizar la tabla
                } else {
                    const error = await response.json();
                    alert(`Error: ${error.error}`);
                }
            } catch (error) {
                console.error("Error al eliminar la materia:", error);
            }
        });
        subjectCell.appendChild(deleteSubjectButton);

        subjectRow.appendChild(subjectCell);

        if (subject.options.length > 0) {
            // Crear la primera fila con la primera opción
            const firstOption = subject.options[0];

            // Celda para la opción
            const optionCell = document.createElement("td");
            optionCell.innerHTML = `
                <strong>${firstOption.professor}</strong> (${firstOption.group})
                <br>Días: ${firstOption.days}
                <br>Horario: ${firstOption.time}
                <br>Preferencia: ${firstOption.preference}
            `;

            // Botón para eliminar la opción
            const deleteOptionCell = document.createElement("td");
            const deleteOptionButton = document.createElement("button");
            deleteOptionButton.textContent = "Delete Option";
            deleteOptionButton.addEventListener("click", async () => {
                try {
                    const response = await fetch(`/api/options/${firstOption.id}`, {
                        method: "DELETE",
                        headers: { "Session-Id": localStorage.getItem("session_id") },
                    });

                    if (response.ok) {
                        alert("Opción eliminada correctamente.");
                        loadSubjects(); // Actualizar la tabla
                    } else {
                        const error = await response.json();
                        alert(`Error: ${error.error}`);
                    }
                } catch (error) {
                    console.error("Error al eliminar la opción:", error);
                }
            });

            deleteOptionCell.appendChild(deleteOptionButton);
            subjectRow.appendChild(optionCell);
            subjectRow.appendChild(deleteOptionCell);

            subjectsTable.appendChild(subjectRow);

            // Crear filas para las opciones restantes
            subject.options.slice(1).forEach((option) => {
                const optionRow = document.createElement("tr");

                // Celda para la opción
                const optionCell = document.createElement("td");
                optionCell.innerHTML = `
                    <strong>${option.professor}</strong> (${option.group})
                    <br>Días: ${option.days}
                    <br>Horario: ${option.time}
                    <br>Preferencia: ${option.preference}
                `;

                // Botón para eliminar la opción
                const deleteOptionCell = document.createElement("td");
                const deleteOptionButton = document.createElement("button");
                deleteOptionButton.textContent = "Delete Option";
                deleteOptionButton.addEventListener("click", async () => {
                    try {
                        const response = await fetch(`/api/options/${option.id}`, {
                            method: "DELETE",
                            headers: { "Session-Id": localStorage.getItem("session_id") },
                        });

                        if (response.ok) {
                            alert("Opción eliminada correctamente.");
                            loadSubjects(); // Actualizar la tabla
                        } else {
                            const error = await response.json();
                            alert(`Error: ${error.error}`);
                        }
                    } catch (error) {
                        console.error("Error al eliminar la opción:", error);
                    }
                });

                deleteOptionCell.appendChild(deleteOptionButton);
                optionRow.appendChild(optionCell);
                optionRow.appendChild(deleteOptionCell);

                subjectsTable.appendChild(optionRow);
            });
        } else {
            // Si no hay opciones, agregar una fila vacía
            const emptyRow = document.createElement("tr");
            const emptyCell = document.createElement("td");
            emptyCell.colSpan = 2; // Combinar columnas de opciones y acciones
            emptyCell.textContent = "No options available";
            emptyRow.appendChild(emptyCell);
            subjectsTable.appendChild(emptyRow);
        }
    });
}

const API_URL = "http://localhost:8000/api/v1/students";

function toggleForm(formId) {
    const form = document.getElementById(formId);
    form.style.display = form.style.display === "none" ? "flex" : "none";
}

function formatName(student) {
    const parts = [];
    if (student.first_name) parts.push(student.first_name);
    if (student.middle_name) parts.push(student.middle_name);
    if (student.last_name) parts.push(student.last_name);
    return parts.join(' ') || 'No name';
}

document.addEventListener("DOMContentLoaded", () => {
    loadStudents();
    
    document.getElementById("studentForm").addEventListener("submit", async (e) => {
        e.preventDefault();

        const student = {
            first_name: document.getElementById("first_name").value || null,
            middle_name: document.getElementById("middle_name").value || null,
            last_name: document.getElementById("last_name").value,
            gender: document.getElementById("gender").value
        };

        const resp = await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(student)
        });

        if (resp.ok) {
            document.getElementById("studentForm").style.display = "none";
        }

        e.target.reset();
        loadStudents();
    });

    document.getElementById("searchForm").addEventListener("submit", async (e) => {
        e.preventDefault();
        const lastName = document.getElementById("searchLastName").value.trim();
        if (lastName) {
            searchByLastName(lastName);
        }
    });
});

async function loadStudents() {
    const response = await fetch(API_URL);
    const students = await response.json();
    renderStudents(students);
}

async function searchByLastName(lastName) {
    const response = await fetch(`${API_URL}/lastName/${encodeURIComponent(lastName)}`);
    if (!response.ok) {
        alert("No students found with that last name");
        return;
    }
    const students = await response.json();
    renderStudents(Array.isArray(students) ? students : [students]);
}

function renderStudents(students) {
    const tbody = document.querySelector("#studentsTable tbody");
    tbody.innerHTML = "";

    students.forEach(student => {
        const row = `
            <tr>
                <td>${student.student_id}</td>
                <td>${formatName(student)}</td>
                <td>${student.gender}</td>
                <td>
                    <button class="edit-btn" onclick="viewStudent(${student.student_id})">Detalles</button>
                    <button class="delete-btn" onclick="deleteStudent(${student.student_id})">Eliminar</button>
                </td>
            </tr>
        `;
        tbody.innerHTML += row;
    });
}

function viewStudent(id) {
    window.location.href = `/students/${id}/view`;
}

async function deleteStudent(id) {
    await fetch(`${API_URL}/${id}`, {
        method: "DELETE"
    });
    loadStudents();
}
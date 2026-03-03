const API_BASE = "http://localhost:8000/api/v1";

function toggleForm(formId) {
    const form = document.getElementById(formId);
    form.style.display = form.style.display === "none" ? "flex" : "none";
}

document.addEventListener("DOMContentLoaded", () => {
    loadStudent();
    loadEmails();
    loadPhones();
    loadAddresses();

    document.getElementById("emailForm").addEventListener("submit", createEmail);
    document.getElementById("phoneForm").addEventListener("submit", createPhone);
    document.getElementById("addressForm").addEventListener("submit", createAddress);
});

async function createEmail(e) {
    e.preventDefault();

    const data = {
        email: document.getElementById("newEmail").value,
        email_type: document.getElementById("emailType").value,
        student_id: studentId
    };
    console.log("creating email", data);

    const resp = await fetch(`${API_BASE}/emails`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });

    if (!resp.ok) {
        const error = await resp.json();
        alert(error.detail || "Could not create email");
        return;
    }
    
    document.getElementById("emailForm").style.display = "none";
    e.target.reset();
    loadEmails();
}

async function createPhone(e) {
    e.preventDefault();

    const data = {
        phone: document.getElementById("phoneNumber").value,
        phone_type: document.getElementById("phoneType").value,
        country_code: document.getElementById("countryCode").value,
        area_code: document.getElementById("areaCode").value,
        student_id: studentId
    };

    const resp = await fetch(`${API_BASE}/phones`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });
    
    if (!resp.ok) {
        const error = await resp.json();
        alert(error.detail || "Could not create phone");
        return;
    }
    
    document.getElementById("phoneForm").style.display = "none";
    e.target.reset();
    loadPhones();
}

async function createAddress(e) {
    e.preventDefault();

    const data = {
        address_line: document.getElementById("addressLine").value,
        city: document.getElementById("city").value,
        state: document.getElementById("state").value,
        zip_postcode: document.getElementById("zip").value,
        student_id: studentId
    };

    const resp = await fetch(`${API_BASE}/addresses`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });
    if (!resp.ok) {
        console.error("Failed to create address", await resp.text());
    } else {
        document.getElementById("addressForm").style.display = "none";
    }

    e.target.reset();
    loadAddresses();
}

// helper functions to load existing data
async function loadStudent() {
    const res = await fetch(`${API_BASE}/students/${studentId}`);
    if (!res.ok) return;
    const student = await res.json();
    const infoEl = document.getElementById("studentInfo");
    infoEl.innerHTML = `
        <div class="info-row"><span class="info-label">First Name:</span><span class="info-value">${student.first_name || ''}</span></div>
        <div class="info-row"><span class="info-label">Middle Name:</span><span class="info-value">${student.middle_name || ''}</span></div>
        <div class="info-row"><span class="info-label">Last Name:</span><span class="info-value">${student.last_name || ''}</span></div>
        <div class="info-row"><span class="info-label">Gender:</span><span class="info-value">${student.gender}</span></div>
        <button class="edit-btn" onclick="openStudentEdit('${student.first_name || ''}', '${student.middle_name || ''}', '${student.last_name || ''}', '${student.gender}')" style="margin-top:10px;">Edit</button>
    `;
}

function openStudentEdit(firstName, middleName, lastName, gender) {
    document.getElementById("editFirstName").value = firstName;
    document.getElementById("editMiddleName").value = middleName;
    document.getElementById("editLastName").value = lastName;
    document.getElementById("editGender").value = gender;
    document.getElementById("studentInfo").style.display = "none";
    document.getElementById("studentEditForm").style.display = "block";
}

function cancelStudentEdit() {
    document.getElementById("studentEditForm").style.display = "none";
    document.getElementById("studentInfo").style.display = "block";
}

async function saveStudentInfo() {
    const data = {
        first_name: document.getElementById("editFirstName").value,
        middle_name: document.getElementById("editMiddleName").value,
        last_name: document.getElementById("editLastName").value,
        gender: document.getElementById("editGender").value
    };

    const resp = await fetch(`${API_BASE}/students/${studentId}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });

    if (!resp.ok) {
        alert("Failed to update student info");
    } else {
        cancelStudentEdit();
        loadStudent();
    }
}

async function loadEmails() {
    const res = await fetch(`${API_BASE}/emails/student/${studentId}`);
    const list = document.getElementById("emailList");
    list.innerHTML = "";
    if (res.ok) {
        const emails = await res.json();
        emails.forEach(e => {
            const li = document.createElement("li");
            li.innerHTML = `
                <div class="item-info">
                    <div class="item-row"><span class="item-label">Email:</span><span class="item-value">${e.email}</span></div>
                    <div class="item-row"><span class="item-label">Type:</span><span class="item-value">${e.email_type}</span></div>
                </div>
                <div class="item-actions">
                    <button class="edit-btn" onclick="openEmailEditModal('${e.email}', '${e.email_type}')">Edit</button>
                    <button class="delete-btn" onclick="deleteEmail('${e.email}')">Delete</button>
                </div>
            `;
            list.appendChild(li);
        });
    }
}

async function loadPhones() {
    const res = await fetch(`${API_BASE}/phones/student/${studentId}`);
    const list = document.getElementById("phoneList");
    list.innerHTML = "";
    if (res.ok) {
        const phones = await res.json();
        phones.forEach(p => {
            const li = document.createElement("li");
            li.innerHTML = `
                <div class="item-info">
                    <div class="item-row"><span class="item-label">Phone:</span><span class="item-value">${p.phone}</span></div>
                    <div class="item-row"><span class="item-label">Type:</span><span class="item-value">${p.phone_type}</span></div>
                    <div class="item-row"><span class="item-label">Country:</span><span class="item-value">${p.country_code || 'N/A'}</span></div>
                    <div class="item-row"><span class="item-label">Area:</span><span class="item-value">${p.area_code || 'N/A'}</span></div>
                </div>
                <div class="item-actions">
                    <button class="edit-btn" onclick="openPhoneEditModal(${p.phone_id}, '${p.phone}', '${p.phone_type}', '${p.country_code || ''}', '${p.area_code || ''}')">Edit</button>
                    <button class="delete-btn" onclick="deletePhone(${p.phone_id})">Delete</button>
                </div>
            `;
            list.appendChild(li);
        });
    }
}

async function loadAddresses() {
    const res = await fetch(`${API_BASE}/addresses/student/${studentId}`);
    const list = document.getElementById("addressList");
    list.innerHTML = "";
    if (res.ok) {
        const addresses = await res.json();
        addresses.forEach(a => {
            const li = document.createElement("li");
            li.innerHTML = `
                <div class="item-info">
                    <div class="item-row"><span class="item-label">Address:</span><span class="item-value">${a.address_line || 'N/A'}</span></div>
                    <div class="item-row"><span class="item-label">City:</span><span class="item-value">${a.city || 'N/A'}</span></div>
                    <div class="item-row"><span class="item-label">State:</span><span class="item-value">${a.state || 'N/A'}</span></div>
                    <div class="item-row"><span class="item-label">ZIP:</span><span class="item-value">${a.zip_postcode || 'N/A'}</span></div>
                </div>
                <div class="item-actions">
                    <button class="edit-btn" onclick="openAddressEditModal(${a.address_id}, '${(a.address_line || '').replace(/'/g, "\\'")}', '${(a.city || '').replace(/'/g, "\\'")}', '${(a.state || '').replace(/'/g, "\\'")}', '${(a.zip_postcode || '').replace(/'/g, "\\'")}')">Edit</button>
                    <button class="delete-btn" onclick="deleteAddress(${a.address_id})">Delete</button>
                </div>
            `;
            list.appendChild(li);
        });
    }
}

// Email edit/delete functions
function openEmailEditModal(email, emailType) {
    document.getElementById("editEmailOld").value = email;
    document.getElementById("editEmailValue").value = email;
    document.getElementById("editEmailType").value = emailType;
    document.getElementById("emailModal").style.display = "block";
}

function closeEmailModal() {
    document.getElementById("emailModal").style.display = "none";
}

async function saveEditEmail() {
    const oldEmail = document.getElementById("editEmailOld").value;
    const newEmail = document.getElementById("editEmailValue").value;
    const emailType = document.getElementById("editEmailType").value;

    const resp = await fetch(`${API_BASE}/emails/${oldEmail}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: newEmail, email_type: emailType })
    });

    if (!resp.ok) {
        alert("Failed to update email");
    } else {
        closeEmailModal();
        loadEmails();
    }
}

async function deleteEmail(email) {
    if (!confirm(`Delete email ${email}?`)) return;
    
    const resp = await fetch(`${API_BASE}/emails/${email}`, {
        method: "DELETE"
    });

    if (!resp.ok) {
        alert("Failed to delete email");
    } else {
        loadEmails();
    }
}

// Phone edit/delete functions
function openPhoneEditModal(phoneId, phone, phoneType, countryCode, areaCode) {
    document.getElementById("editPhoneOld").value = phoneId;
    document.getElementById("editPhoneValue").value = phone;
    document.getElementById("editPhoneType").value = phoneType;
    document.getElementById("editCountryCode").value = countryCode;
    document.getElementById("editAreaCode").value = areaCode;
    document.getElementById("phoneModal").style.display = "block";
}

function closePhoneModal() {
    document.getElementById("phoneModal").style.display = "none";
}

async function saveEditPhone() {
    const phoneId = document.getElementById("editPhoneOld").value;
    const phone = document.getElementById("editPhoneValue").value;
    const phoneType = document.getElementById("editPhoneType").value;
    const countryCode = document.getElementById("editCountryCode").value;
    const areaCode = document.getElementById("editAreaCode").value;

    const resp = await fetch(`${API_BASE}/phones/${phoneId}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            phone,
            phone_type: phoneType,
            country_code: countryCode,
            area_code: areaCode
        })
    });

    if (!resp.ok) {
        alert("Failed to update phone");
    } else {
        closePhoneModal();
        loadPhones();
    }
}

async function deletePhone(phoneId) {
    if (!confirm("Delete this phone?")) return;
    
    const resp = await fetch(`${API_BASE}/phones/${phoneId}`, {
        method: "DELETE"
    });

    if (!resp.ok) {
        alert("Failed to delete phone");
    } else {
        loadPhones();
    }
}

// Address edit/delete functions
function openAddressEditModal(addressId, addressLine, city, state, zip) {
    document.getElementById("editAddressId").value = addressId;
    document.getElementById("editAddressLine").value = addressLine;
    document.getElementById("editCity").value = city;
    document.getElementById("editState").value = state;
    document.getElementById("editZip").value = zip;
    document.getElementById("addressModal").style.display = "block";
}

function closeAddressModal() {
    document.getElementById("addressModal").style.display = "none";
}

async function saveEditAddress() {
    const addressId = document.getElementById("editAddressId").value;
    const addressLine = document.getElementById("editAddressLine").value;
    const city = document.getElementById("editCity").value;
    const state = document.getElementById("editState").value;
    const zip = document.getElementById("editZip").value;

    const resp = await fetch(`${API_BASE}/addresses/${addressId}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            address_line: addressLine,
            city,
            state,
            zip_postcode: zip,
            student_id: studentId
        })
    });

    if (!resp.ok) {
        alert("Failed to update address");
    } else {
        closeAddressModal();
        loadAddresses();
    }
}

async function deleteAddress(addressId) {
    if (!confirm("Delete this address?")) return;
    
    const resp = await fetch(`${API_BASE}/addresses/${addressId}`, {
        method: "DELETE"
    });

    if (!resp.ok) {
        alert("Failed to delete address");
    } else {
        loadAddresses();
    }
}

function goBack() {
    window.location.href = "/";
}
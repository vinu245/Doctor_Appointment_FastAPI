const doctorList = document.getElementById("doctorList");
const apptList = document.getElementById("apptList");
const doctorStats = document.getElementById("doctorStats");
const apptStats = document.getElementById("apptStats");
const form = document.getElementById("bookForm");
const formMessage = document.getElementById("formMessage");
const refreshBtn = document.getElementById("refreshBtn");
const installBtn = document.getElementById("installBtn");

let installPrompt = null;

function boolText(value) {
    return value ? "Available" : "Not available";
}

function li(text) {
    const item = document.createElement("li");
    item.textContent = text;
    return item;
}

function addActionButton(container, label, className, onClick) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = `btn action ${className}`;
    button.textContent = label;
    button.addEventListener("click", onClick);
    container.appendChild(button);
}

async function updateAppointmentStatus(appointmentId, action) {
    formMessage.textContent = `Updating appointment #${appointmentId}...`;

    try {
        await fetchJson(`/appointments/${appointmentId}/${action}`, { method: "POST" });
        formMessage.textContent = `Appointment #${appointmentId} marked ${action}.`;
        await loadAll();
    } catch (err) {
        formMessage.textContent = err.message;
    }
}

async function fetchJson(path, options = {}) {
    const response = await fetch(`/api${path}`, {
        headers: { "Content-Type": "application/json" },
        ...options
    });

    let payload = {};
    try {
        payload = await response.json();
    } catch (_) {
        payload = {};
    }

    if (!response.ok) {
        const detail = payload.detail || "Request failed";
        throw new Error(detail);
    }

    return payload;
}

async function loadDoctors() {
    const data = await fetchJson("/doctors");
    doctorStats.textContent = `Total ${data.total} | Available ${data.available_count}`;
    doctorList.innerHTML = "";

    data.data.forEach((doc) => {
        doctorList.appendChild(li(`#${doc.id} ${doc.name} | ${doc.specialization} | Fee ${doc.fee} | ${boolText(doc.is_available)}`));
    });
}

async function loadAppointments() {
    const data = await fetchJson("/appointments");
    apptStats.textContent = `Total ${data.total}`;
    apptList.innerHTML = "";

    if (!data.data.length) {
        apptList.appendChild(li("No appointments yet."));
        return;
    }

    data.data.forEach((appt) => {
        const item = document.createElement("li");
        const details = document.createElement("p");
        details.className = "appt-title";
        details.textContent = `#${appt.appointment_id} ${appt.patient} with ${appt.doctor} on ${appt.date} | ${appt.status} | Final fee ${appt.final_fee}`;
        item.appendChild(details);

        const actions = document.createElement("div");
        actions.className = "action-row";

        if (appt.status === "scheduled") {
            addActionButton(actions, "Confirm", "small", () => updateAppointmentStatus(appt.appointment_id, "confirm"));
            addActionButton(actions, "Cancel", "danger", () => updateAppointmentStatus(appt.appointment_id, "cancel"));
        }

        if (appt.status === "confirmed") {
            addActionButton(actions, "Complete", "small", () => updateAppointmentStatus(appt.appointment_id, "complete"));
            addActionButton(actions, "Cancel", "danger", () => updateAppointmentStatus(appt.appointment_id, "cancel"));
        }

        if (actions.childElementCount > 0) {
            item.appendChild(actions);
        }

        apptList.appendChild(item);
    });
}

async function loadAll() {
    try {
        await Promise.all([loadDoctors(), loadAppointments()]);
    } catch (err) {
        formMessage.textContent = err.message;
    }
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();
    formMessage.textContent = "Creating appointment...";

    const formData = new FormData(form);
    const body = {
        patient_name: formData.get("patient_name"),
        doctor_id: Number(formData.get("doctor_id")),
        date: formData.get("date"),
        reason: formData.get("reason"),
        appointment_type: formData.get("appointment_type"),
        senior_citizen: formData.get("senior_citizen") === "on"
    };

    try {
        await fetchJson("/appointments", {
            method: "POST",
            body: JSON.stringify(body)
        });

        form.reset();
        formMessage.textContent = "Appointment created.";
        await loadAll();
    } catch (err) {
        formMessage.textContent = err.message;
    }
});

refreshBtn.addEventListener("click", loadAll);

window.addEventListener("beforeinstallprompt", (event) => {
    event.preventDefault();
    installPrompt = event;
    installBtn.hidden = false;
});

installBtn.addEventListener("click", async () => {
    if (!installPrompt) {
        return;
    }
    installPrompt.prompt();
    await installPrompt.userChoice;
    installPrompt = null;
    installBtn.hidden = true;
});

if ("serviceWorker" in navigator) {
    navigator.serviceWorker.register("/service-worker.js").catch(() => {});
}

loadAll();

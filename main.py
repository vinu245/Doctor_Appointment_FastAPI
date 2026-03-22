from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field
from typing import Optional
import math

app = FastAPI()

# ------------------ DATA ------------------

doctors = [
    {"id": 1, "name": "Dr. Smith", "specialization": "Cardiologist", "fee": 500, "experience_years": 10, "is_available": True},
    {"id": 2, "name": "Dr. John", "specialization": "Dermatologist", "fee": 300, "experience_years": 5, "is_available": True},
    {"id": 3, "name": "Dr. Priya", "specialization": "Pediatrician", "fee": 400, "experience_years": 8, "is_available": False},
    {"id": 4, "name": "Dr. Kumar", "specialization": "General", "fee": 200, "experience_years": 3, "is_available": True},
    {"id": 5, "name": "Dr. Meena", "specialization": "Cardiologist", "fee": 600, "experience_years": 12, "is_available": True},
    {"id": 6, "name": "Dr. Ravi", "specialization": "Dermatologist", "fee": 350, "experience_years": 6, "is_available": False}
]

appointments = []
appt_counter = 1

# ------------------ HELPERS ------------------

def find_doctor(doctor_id):
    return next((d for d in doctors if d["id"] == doctor_id), None)

def calculate_fee(base_fee, appointment_type, senior):
    fee = base_fee

    if appointment_type == "video":
        fee *= 0.8
    elif appointment_type == "emergency":
        fee *= 1.5

    original = fee

    if senior:
        fee *= 0.85

    return round(original), round(fee)

def filter_doctors_logic(specialization, max_fee, min_exp, is_available):
    result = []
    for d in doctors:
        if specialization is not None and d["specialization"] != specialization:
            continue
        if max_fee is not None and d["fee"] > max_fee:
            continue
        if min_exp is not None and d["experience_years"] < min_exp:
            continue
        if is_available is not None and d["is_available"] != is_available:
            continue
        result.append(d)
    return result

def find_appointment(appt_id):
    return next((a for a in appointments if a["appointment_id"] == appt_id), None)

# ------------------ DAY 1 ------------------

@app.get("/")
def home():
    return {"message": "Welcome to MediCare Clinic"}

@app.get("/doctors")
def get_doctors():
    return {
        "data": doctors,
        "total": len(doctors),
        "available_count": sum(d["is_available"] for d in doctors)
    }

@app.get("/doctors/summary")
def summary():
    return {
        "total": len(doctors),
        "available": sum(d["is_available"] for d in doctors),
        "most_experienced": max(doctors, key=lambda x: x["experience_years"])["name"],
        "cheapest_fee": min(doctors, key=lambda x: x["fee"])["fee"],
        "specialization_count": {
            s: sum(1 for d in doctors if d["specialization"] == s)
            for s in set(d["specialization"] for d in doctors)
        }
    }

@app.get("/appointments")
def get_appointments():
    return {"data": appointments, "total": len(appointments)}

# ------------------ FILTER BEFORE ID ------------------

@app.get("/doctors/filter")
def filter_doctors(
    specialization: Optional[str] = None,
    max_fee: Optional[int] = None,
    min_experience: Optional[int] = None,
    is_available: Optional[bool] = None
):
    result = filter_doctors_logic(specialization, max_fee, min_experience, is_available)
    return {"data": result, "count": len(result)}

# ------------------ DAY 6 (before id) ------------------

@app.get("/doctors/search")
def search_doctors(keyword: str):
    result = [d for d in doctors if keyword.lower() in d["name"].lower() or keyword.lower() in d["specialization"].lower()]
    return {"data": result, "total_found": len(result)} if result else {"message": "No doctors found"}

@app.get("/doctors/sort")
def sort_doctors(sort_by: str = "fee", order: str = "asc"):
    if sort_by not in ["fee", "name", "experience_years"]:
        raise HTTPException(400, "Invalid sort_by")
    if order not in ["asc", "desc"]:
        raise HTTPException(400, "Invalid order")

    return sorted(doctors, key=lambda x: x[sort_by], reverse=(order == "desc"))

@app.get("/doctors/page")
def paginate(page: int = 1, limit: int = 3):
    start = (page - 1) * limit
    return {
        "page": page,
        "total_pages": math.ceil(len(doctors) / limit),
        "data": doctors[start:start+limit]
    }

@app.get("/doctors/browse")
def browse(
    keyword: Optional[str] = None,
    sort_by: str = "fee",
    order: str = "asc",
    page: int = 1,
    limit: int = 4
):
    data = doctors

    if keyword:
        data = [d for d in data if keyword.lower() in d["name"].lower() or keyword.lower() in d["specialization"].lower()]

    data = sorted(data, key=lambda x: x[sort_by], reverse=(order == "desc"))

    start = (page - 1) * limit
    return {
        "total": len(data),
        "total_pages": math.ceil(len(data)/limit),
        "data": data[start:start+limit]
    }

# ------------------ ID ROUTE ------------------

@app.get("/doctors/{doctor_id}")
def get_doctor(doctor_id: int):
    doc = find_doctor(doctor_id)
    if not doc:
        raise HTTPException(404, "Doctor not found")
    return doc

# ------------------ DAY 2 ------------------

class AppointmentRequest(BaseModel):
    patient_name: str = Field(..., min_length=2)
    doctor_id: int = Field(..., gt=0)
    date: str = Field(..., min_length=8)
    reason: str = Field(..., min_length=5)
    appointment_type: str = "in-person"
    senior_citizen: bool = False

@app.post("/appointments")
def create_appointment(req: AppointmentRequest):
    global appt_counter

    doc = find_doctor(req.doctor_id)
    if not doc:
        raise HTTPException(404, "Doctor not found")

    if not doc["is_available"]:
        raise HTTPException(400, "Doctor not available")

    original, final = calculate_fee(doc["fee"], req.appointment_type, req.senior_citizen)

    appt = {
        "appointment_id": appt_counter,
        "patient": req.patient_name,
        "doctor_id": doc["id"],
        "doctor": doc["name"],
        "date": req.date,
        "type": req.appointment_type,
        "original_fee": original,
        "final_fee": final,
        "status": "scheduled"
    }

    appointments.append(appt)
    doc["is_available"] = False
    appt_counter += 1

    return appt

# ------------------ DAY 4 ------------------

class NewDoctor(BaseModel):
    name: str = Field(..., min_length=2)
    specialization: str = Field(..., min_length=2)
    fee: int = Field(..., gt=0)
    experience_years: int = Field(..., gt=0)
    is_available: bool = True

@app.post("/doctors", status_code=201)
def add_doctor(doc: NewDoctor):
    if any(d["name"].lower() == doc.name.lower() for d in doctors):
        raise HTTPException(400, "Duplicate doctor")

    new_doc = doc.dict()
    new_doc["id"] = len(doctors) + 1
    doctors.append(new_doc)
    return new_doc

@app.put("/doctors/{doctor_id}")
def update_doctor(doctor_id: int, fee: Optional[int] = None, is_available: Optional[bool] = None):
    doc = find_doctor(doctor_id)
    if not doc:
        raise HTTPException(404, "Doctor not found")

    if fee is not None:
        doc["fee"] = fee
    if is_available is not None:
        doc["is_available"] = is_available

    return doc

@app.delete("/doctors/{doctor_id}")
def delete_doctor(doctor_id: int):
    doc = find_doctor(doctor_id)
    if not doc:
        raise HTTPException(404, "Doctor not found")

    if any(a["doctor_id"] == doctor_id and a["status"] == "scheduled" for a in appointments):
        raise HTTPException(400, "Active appointments exist")

    doctors.remove(doc)
    return {"message": "Deleted"}

# ------------------ DAY 5 ------------------

@app.post("/appointments/{appointment_id}/confirm")
def confirm(appointment_id: int):
    appt = find_appointment(appointment_id)
    if not appt:
        raise HTTPException(404, "Not found")
    appt["status"] = "confirmed"
    return appt

@app.post("/appointments/{appointment_id}/cancel")
def cancel(appointment_id: int):
    appt = find_appointment(appointment_id)
    if not appt:
        raise HTTPException(404, "Not found")

    appt["status"] = "cancelled"
    doc = find_doctor(appt["doctor_id"])
    if doc:
        doc["is_available"] = True

    return appt

@app.post("/appointments/{appointment_id}/complete")
def complete(appointment_id: int):
    appt = find_appointment(appointment_id)
    if not appt:
        raise HTTPException(404, "Not found")
    appt["status"] = "completed"
    return appt

@app.get("/appointments/active")
def active():
    return [a for a in appointments if a["status"] in ["scheduled", "confirmed"]]

@app.get("/appointments/by-doctor/{doctor_id}")
def by_doctor(doctor_id: int):
    return [a for a in appointments if a["doctor_id"] == doctor_id]

# ------------------ APPOINTMENTS DAY 6 ------------------

@app.get("/appointments/search")
def search_appt(name: str):
    return [a for a in appointments if name.lower() in a["patient"].lower()]

@app.get("/appointments/sort")
def sort_appt():
    return sorted(appointments, key=lambda x: x["final_fee"])

@app.get("/appointments/page")
def page_appt(page: int = 1, limit: int = 2):
    start = (page - 1) * limit
    return appointments[start:start+limit]
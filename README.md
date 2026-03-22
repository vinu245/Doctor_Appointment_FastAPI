# 🏥 Healthcare Appointment System (FastAPI + Interactive UI)

A **full-stack healthcare management system** built using **FastAPI** with an interactive frontend UI to demonstrate real-time API communication and backend logic.

---

## 🚀 Project Overview

This project simulates a real-world healthcare system where users can:
- Manage doctors 👨‍⚕️  
- Book and track appointments 📅  
- Understand API working through a simple UI 🌐  

The frontend UI helps visualize how FastAPI works in real-time, making it easier to understand API responses and flows.

---

## 🎥 Demo Videos

- 🔹 FastAPI API Demo (Swagger UI):  
  project_demo.mp4

- 🔹 Frontend UI Demo:  
  Ui_Working.mp4 

---

## 🧰 Tech Stack

- Backend: FastAPI, Python  
- Frontend: HTML, CSS, JavaScript  
- Validation: Pydantic  
- API Docs: Swagger UI  
- Server: Uvicorn  

---

## ⚙️ Features

### 👨‍⚕️ Doctor Management
- Add new doctors  
- Update doctor details  
- Delete doctors  
- Filter by specialization, experience, fee  
- Search, sorting, and pagination  

---

### 📅 Appointment System
- Book appointments  
- Input validation using Pydantic  
- Dynamic fee calculation:
  - Video consultation → 20% discount  
  - Emergency → 50% extra  
  - Senior citizen → 15% discount  

- Appointment lifecycle:
  Scheduled → Confirmed → Completed / Cancelled  

---

### 📊 Smart Insights
- Total doctors available  
- Most experienced doctor  
- Cheapest consultation fee  
- Doctor-wise appointment history  
- Active appointment tracking  

---

## 🔄 API Methods (CRUD)

| Method | Endpoint | Description |
|--------|---------|------------|
| GET    | /doctors | Get all doctors |
| GET    | /doctors/{id} | Get doctor by ID |
| POST   | /doctors | Add doctor |
| PUT    | /doctors/{id} | Update doctor |
| DELETE | /doctors/{id} | Delete doctor |
| POST   | /appointments | Book appointment |
| GET    | /appointments | View appointments |

---

## 🌐 API Documentation

Swagger UI available at:

http://127.0.0.1:8000/docs

---

## ▶️ How to Run

### 1. Clone Repository
```bash
git clone https://github.com/YOUR_USERNAME/healthcare-fastapi-system.git
cd healthcare-fastapi-system
```

### 2. Install Dependencies
```bash
pip install fastapi uvicorn
```

### 3. Run Server
```bash
uvicorn main:app --reload
```

### 4. Open in Browser
- API Docs: http://127.0.0.1:8000/docs  
- UI: Open index.html  

---

## 📂 Project Structure

```
healthcare-fastapi-system/
│
├── main.py
├── index.html
├── app.js
├── style.css
├── README.md
```

---

## 🎯 Learning Outcomes

- FastAPI development  
- REST API design (GET, POST, PUT, DELETE)  
- Data validation using Pydantic  
- API testing using Swagger  
- Frontend & backend integration  
- Real-world backend logic  

---

## 💡 Future Enhancements

- Add database (MySQL / PostgreSQL)  
- Add authentication (JWT)  
- Deploy project (Render / AWS)  
- Build advanced UI (React)  

---

## 👩‍💻 Author

Vinutha  
Aspiring Backend Developer  

---

## ⭐ Support

If you like this project, give it a ⭐ on GitHub!

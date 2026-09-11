# Threshold Verification — Unified Single-App Prototype

## 📌 One-Line Summary

A unified FastAPI and React web application that evaluates numerical streams against a configurable variance threshold and classifies them as **STABLE** or **CRITICAL**.

---

## 📖 Overview

Threshold Verification is a lightweight, single-process web application built with **FastAPI** and **React**. It allows operators to input a numerical stream alongside an allowed maximum variance. The backend computes the stream mean and determines if any individual data point deviates past the configured limit.

The operational result is classified as:
- 🟢 **STABLE** — All stream points stay within the permitted variance boundary.
- 🔴 **CRITICAL** — One or more stream values breach the permitted variance threshold.

The solution requires **no separate frontend build tools, bundlers, or proxy servers**. FastAPI serves both the JSON REST API and the React presentation layer natively from a single port using browser-side Babel transpilation via CDN.

### Overall Workflow

```text
User enters numerical stream
            ↓
User sets maximum variance
            ↓
React Frontend (templates/index.html)
            ↓
POST /api/threshold
            ↓
FastAPI + Pydantic Schema Validation
            ↓
Calculate Arithmetic Mean
            ↓
Evaluate Deviation against Max Variance
            ↓
Return Status: STABLE / CRITICAL

## 🚀 How to Run This Project

Follow these steps to run the application locally.

### 1. Clone the Repository

```bash
git clone [GITHUB REPOSITORY URL]
cd aurvia-screening-app
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

**Windows:**

```bash
venv\Scripts\activate
```

**Linux/macOS:**

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the Application

Start the FastAPI server:

```bash
uvicorn app:app --reload
```

### 6. Open the Application

Open the following URL in your browser:

```text
http://127.0.0.1:8000/
```

The application uses a **single FastAPI process** to serve both the React frontend and the `/api/threshold` API.

No separate React server, Vite server, frontend port, or frontend build command is required.

### 7. Stop the Application

To stop the development server, press:

```text
Ctrl + C
```

            ↓
Update React UI Badge Display

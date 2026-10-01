# 🚨 EmergencyFlow AI — Multi-Agent Emergency Triage System

![EmergencyFlow AI Architecture](./Medical.png)

> An AI-powered multi-agent emergency triage and clinical decision-support prototype for analyzing medical reports and generating structured emergency assessment insights.

---

## 📌 Overview

**EmergencyFlow AI** is a Multi-Agent AI system designed to process medical reports and transform unstructured clinical information into a structured emergency assessment.

The system accepts a medical report in **PDF format** and processes it through a sequence of specialized agents that extract patient information, medical records, patient history, emergency findings, and an AI-generated clinical summary.

The project demonstrates the practical application of:

- Artificial Intelligence
- Multi-Agent Systems
- Natural Language Processing
- Large Language Models
- Workflow Orchestration
- Clinical Information Extraction
- AI-Assisted Decision Support

---

## ✨ Features

- 📄 Medical PDF report processing
- 👤 Patient information extraction
- 📋 Medical records extraction
- 🕒 Patient history and timeline organization
- 🚨 Emergency triage assessment
- 🔎 Critical clinical findings detection
- 🧠 AI-generated clinical summary
- 📊 Structured final clinical report
- ✅ Final report validation
- 💬 AI Consultation Chat
- 🌐 Custom web-based interface
- 🤖 Multi-Agent workflow architecture
- ⚡ End-to-end automated processing

---

## 🎯 Project Objective

The main objective of **EmergencyFlow AI** is to demonstrate how multiple AI agents can work together to organize and analyze information from medical reports.

The system follows a sequential workflow:

```text
Medical PDF
     ↓
Patient Data Agent
     ↓
Medical Records Agent
     ↓
History Agent
     ↓
Triage Agent
     ↓
Summary Agent
     ↓
Final Clinical Report
```

---

## 🤖 Multi-Agent Workflow

### 1. 📄 Medical PDF

The system accepts a medical report in PDF format and extracts its textual content for further processing.

### 2. 👤 Patient Data Agent

Extracts structured patient information, including:

- Age
- Gender
- Symptoms
- Vital signs
- Clinical conditions
- Other relevant information

### 3. 📋 Medical Records Agent

Identifies relevant medical records such as:

- Previous medical status
- Medications
- Tests and examinations
- Emergency interventions
- Reported pathological findings

### 4. 🕒 History Agent

Organizes the patient's history into:

- Long-term care
- Previous status
- Recent history
- Timeline events

### 5. 🚨 Triage Agent

Analyzes acute clinical findings and determines the emergency priority based on the extracted information.

The current prototype detects critical findings such as:

- Cardiac arrest
- Unresponsiveness
- No distal pulses
- Heart rate of 0
- Respiratory rate of 0

The triage component also generates a factual explanation of the emergency severity.

### 6. 🧠 Summary Agent

Generates a concise structured summary based on:

- Patient information
- Symptoms
- Acute findings
- Triage priority

### 7. 📊 Final Clinical Report

Combines the outputs of the different agents into a structured final report containing:

- Patient Data
- Medical Records
- History
- Triage
- Clinical Summary
- Source document information
- Safety note

---

## 🏗️ System Architecture

```text
                         ┌──────────────────────┐
                         │     Medical PDF      │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Patient Data Agent   │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Medical Records      │
                         │ Agent                │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ History Agent        │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Triage Agent         │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Summary Agent        │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Final Clinical       │
                         │ Report               │
                         └──────────────────────┘
```

---

## 🛠️ Technology Stack

### Backend

- 🐍 Python
- ⚡ FastAPI / Gradio backend
- 🔗 LangGraph
- 📄 PyPDF2
- 🤗 Hugging Face Transformers
- 🧠 `google/flan-t5-small`

### Frontend

- HTML5
- CSS3
- JavaScript
- Custom NightShift MD / MediCore AI interface
- PDF.js

### AI & Workflow

- Multi-Agent AI Architecture
- LangGraph Workflow Orchestration
- Local Language Model
- Natural Language Processing
- Rule-Based Clinical Information Extraction
- LLM-Based Summarization
- Structured Report Generation

---

## 📂 Project Structure

```text
EmergencyFlow-AI/
│
├── index.html
├── README.md
├── BACKEND_CORS.md
└── Medical.png
```

> The GitHub repository contains the custom frontend and project documentation, while the AI processing backend is deployed separately.

---

## 🔄 End-to-End Workflow

```text
1. Upload Medical PDF
             ↓
2. Extract PDF Text
             ↓
3. Patient Data Agent
             ↓
4. Medical Records Agent
             ↓
5. History Agent
             ↓
6. Triage Agent
             ↓
7. Summary Agent
             ↓
8. Final Report Generation
             ↓
9. AI Consultation
```

---

## 💬 AI Consultation

EmergencyFlow AI also provides an AI consultation interface that allows users to ask questions about the generated assessment.

Example:

```text
User:
Tell me about the patient.

AI:
The patient is a 59-year-old female with dyspnea on exertion,
dry cough, and atypical chest pain. The acute findings include
cardiac arrest, unresponsiveness, and no distal pulses.
```

The chat operates using the generated structured report as its context.

---

## 📊 Generated Assessment

The final assessment contains several structured sections.

### 👤 Patient Data

- Age
- Gender
- Symptoms
- Vital signs
- Clinical conditions
- Relevant information

### 📋 Medical Records

- Previous medical status
- Medications
- Tests and examinations
- Emergency interventions
- Reported pathological findings

### 🕒 Patient History

- Long-term care
- Previous status
- Recent history
- Clinical timeline

### 🚨 Triage

- Emergency priority
- Critical findings
- Clinical reasoning
- Safety note

### 🧠 Clinical Summary

A concise factual summary generated from the extracted patient information and acute clinical findings.

---

## 🧪 Testing & Evaluation

The system was tested through multiple components of the workflow:

- ✅ Patient Data Extraction
- ✅ Medical Records Extraction
- ✅ History Extraction
- ✅ Emergency Triage Detection
- ✅ LLM Summary Generation
- ✅ Final Report Structure
- ✅ End-to-End Workflow Execution
- ✅ AI Consultation
- ⚡ Workflow Efficiency Measurement

The prototype successfully processes the provided medical report and generates a structured emergency assessment.

---

## 🌐 Deployment Architecture

```text
                    User
                      │
                      ▼
            ┌──────────────────┐
            │   GitHub Pages   │
            │ Custom Frontend  │
            └────────┬─────────┘
                     │
                     │ API Requests
                     ▼
            ┌──────────────────┐
            │  AI Backend      │
            │ EmergencyFlow AI │
            └────────┬─────────┘
                     │
                     ▼
            ┌──────────────────┐
            │ Multi-Agent      │
            │ AI Workflow      │
            └──────────────────┘
```

### Frontend

The custom web interface is hosted through **GitHub Pages**.

### Backend

The AI processing backend provides:

```text
POST /api/assess
POST /api/chat
GET  /health
```

---

## 🚀 Getting Started

### Prerequisites

Make sure you have:

- Python 3.x
- Git
- Internet connection for downloading the required model

### 1. Clone the Repository

```bash
git clone https://github.com/Razan243/EmergencyFlow-AI.git
cd EmergencyFlow-AI
```

### 2. Frontend

The frontend is provided in:

```text
index.html
```

The application can be deployed using GitHub Pages.

### 3. Backend

The AI backend is deployed separately and exposes the required API endpoints:

```text
/api/assess
/api/chat
/health
```

---

## 🌐 Live Project

### GitHub Repository

https://github.com/Razan243/EmergencyFlow-AI

### GitHub Pages

https://razan243.github.io/EmergencyFlow-AI/

> GitHub Pages hosts the frontend interface, while the AI backend handles PDF processing, multi-agent execution, report generation, and AI consultation.

---

## 📄 Input

The system accepts medical reports in:

```text
PDF format
```

After uploading a report, the system extracts and organizes relevant information into structured sections.

---

## 🔍 Final Report Validation

The system validates the generated report to ensure that the required sections are available.

Required sections include:

- Patient Data
- Medical Records
- History
- Triage
- Clinical Summary

The final report also maintains information about the original source document.

---

## ⚠️ Safety Notice

> **EmergencyFlow AI is an educational and research-oriented clinical decision-support prototype.**

The system is **NOT intended to:**

- Diagnose medical conditions
- Replace healthcare professionals
- Provide treatment recommendations
- Make real-world emergency medical decisions

The project is designed for educational, research, demonstration, and AI workflow development purposes only.

---

## 🎓 Project Context

This project demonstrates practical applications of:

- 🤖 Artificial Intelligence
- 🔗 Multi-Agent Systems
- 🧠 Natural Language Processing
- 💬 Large Language Models
- 📄 Clinical Information Extraction
- 🔄 Workflow Orchestration
- 📊 Structured Data Processing
- 🏥 AI-Assisted Decision Support

---

## 👩‍💻 Author

### Razan Gewaily

**Computer Science Student — Artificial Intelligence**

GitHub:

https://github.com/Razan243

---

## ⭐ Project

If you find this project interesting, feel free to explore the repository and the implementation.

⭐ Star the repository if you would like to support the project.

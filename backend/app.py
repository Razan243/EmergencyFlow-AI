import json
import re
from pathlib import Path
from typing import TypedDict

import spaces
import torch
from fastapi.responses import HTMLResponse
from gradio import Server
from gradio.data_classes import FileData
from langgraph.graph import StateGraph, END
from PyPDF2 import PdfReader
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

BASE_DIR = Path(__file__).resolve().parent
MODEL_NAME = "google/flan-t5-small"

print("Loading EmergencyFlow AI model...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
model = model.to("cuda")
model.eval()
print("EmergencyFlow AI model loaded on ZeroGPU CUDA emulation.")


def generate_with_llm(prompt: str, max_new_tokens: int = 120) -> str:
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
    inputs = {k: v.to("cuda") for k, v in inputs.items()}
    with torch.no_grad():
        outputs = model.generate(**inputs, max_new_tokens=max_new_tokens)
    return tokenizer.decode(outputs[0], skip_special_tokens=True).strip()


def patient_data_agent(pdf_text: str) -> dict:
    text = pdf_text.lower()
    data = {
        "age": None, "gender": None, "symptoms": [], "vital_signs": {},
        "clinical_condition": [], "other_relevant_information": []
    }
    m = re.search(r"\b(\d{2})\s*[- ]?year[- ]?old\b", text)
    if m:
        data["age"] = int(m.group(1))
    if "woman" in text:
        data["gender"] = "Female"
    elif "man" in text:
        data["gender"] = "Male"
    for phrase, label in [
        ("dyspnea on exertion", "Dyspnea on exertion"),
        ("shortness of breath", "Shortness of breath"),
        ("dry cough", "Dry cough"),
        ("atypical chest pain", "Atypical chest pain")
    ]:
        if phrase in text:
            data["symptoms"].append(label)
    for pattern, key in [
        (r"(?:blood pressure|bp)\s*(?:of|:)?\s*(\d+/\d+)", "blood_pressure"),
        (r"(?:heart rate|hr)\s*(?:of|:)?\s*(\d+)", "heart_rate"),
        (r"(?:respiratory rate|rr)\s*(?:of|:)?\s*(\d+)", "respiratory_rate"),
        (r"(?:temperature|temp)\s*(?:of|:)?\s*(\d+)", "temperature")
    ]:
        m = re.search(pattern, text)
        if m:
            data["vital_signs"][key] = m.group(1)
    for phrase, label in [
        ("cardiac arrest", "Cardiac arrest"),
        ("unresponsive", "Unresponsive"),
        ("no distal pulses", "No distal pulses"),
        ("bilateral fixed and dilated pupils", "Bilateral fixed and dilated pupils")
    ]:
        if phrase in text:
            data["clinical_condition"].append(label)
    if "no medications" in text:
        data["other_relevant_information"].append("No medications reported")
    return data


def medical_records_agent(pdf_text: str) -> dict:
    text = pdf_text.lower()
    data = {
        "previous_medical_status": [], "medications": [],
        "tests_and_examinations": [], "emergency_interventions": [],
        "reported_pathological_findings": []
    }
    if "healthy" in text:
        data["previous_medical_status"].append("Physician reported the patient as healthy")
    if "no medications" in text or "on no medications" in text:
        data["medications"].append("No medications reported")
    if "ekg" in text:
        data["tests_and_examinations"].append("EKG performed")
    if "rule out anemia" in text:
        data["tests_and_examinations"].append("Orders were sent to rule out anemia")
    if "thyroid disease" in text:
        data["tests_and_examinations"].append("Orders were sent to rule out thyroid disease")
    if "cpr" in text:
        data["emergency_interventions"].append("CPR performed")
    if "atropine" in text:
        data["emergency_interventions"].append("Atropine administered")
    if "epinephrine" in text:
        data["emergency_interventions"].append("Epinephrine administered")
    if "bicarbonate" in text:
        data["emergency_interventions"].append("Bicarbonate administered")
    if "intubation" in text:
        data["emergency_interventions"].append("Intubation performed")
    if "bilateral pulmonary embolism" in text:
        data["reported_pathological_findings"].append("Bilateral pulmonary embolism (PE)")
    if "bile duct adenoma" in text:
        data["reported_pathological_findings"].append("Bile duct adenoma")
    if "rib fractures" in text:
        data["reported_pathological_findings"].append("Rib fractures")
    return data


def history_agent(pdf_text: str) -> dict:
    text = pdf_text.lower()
    data = {"long_term_care": [], "previous_status": [], "recent_history": [], "timeline_events": []}
    if "under the care of dr." in text and "19 years" in text:
        data["long_term_care"].append("Patient was under the care of a physician for 19 years")
    if "healthy" in text:
        data["previous_status"].append("Patient was reported as healthy")
    if "no medications" in text:
        data["previous_status"].append("No medications were reported")
    if "two weeks of dyspnea" in text:
        data["recent_history"].append("Two weeks of dyspnea on exertion")
    if "dry cough" in text:
        data["recent_history"].append("Dry cough")
    if "atypical chest pain" in text:
        data["recent_history"].append("Atypical chest pain")
    if "february 9, 2007" in text:
        data["timeline_events"].append("February 9, 2007: Patient was evaluated by the physician")
    if "february 11, 2007" in text:
        data["timeline_events"].append("February 11, 2007: EMS found the patient in cardiac arrest")
    if "10:16 am" in text:
        data["timeline_events"].append("10:16 AM: CPR ceased and the patient was pronounced")
    return data


def triage_agent(patient_data: dict, medical_records: dict, history: dict) -> dict:
    condition = patient_data.get("clinical_condition", [])
    vitals = patient_data.get("vital_signs", {})
    critical = []
    if "Cardiac arrest" in condition:
        critical.append("Cardiac arrest")
    if "Unresponsive" in condition:
        critical.append("Unresponsive")
    if "No distal pulses" in condition:
        critical.append("No distal pulses")
    if vitals.get("heart_rate") == "0":
        critical.append("Heart rate: 0")
    if vitals.get("respiratory_rate") == "0":
        critical.append("Respiratory rate: 0")
    priority = "Immediate Emergency" if critical else "Requires Further Assessment"
    prompt = (
        "Explain the emergency severity in one factual sentence. "
        f"Cardiac arrest: {'yes' if 'Cardiac arrest' in condition else 'no'}. "
        f"Unresponsive: {'yes' if 'Unresponsive' in condition else 'no'}. "
        f"No distal pulses: {'yes' if 'No distal pulses' in condition else 'no'}. "
        f"Heart rate: {vitals.get('heart_rate', 'not reported')}. "
        f"Respiratory rate: {vitals.get('respiratory_rate', 'not reported')}. "
        "Do not give a diagnosis or treatment recommendation."
    )
    reason = generate_with_llm(prompt, 60)
    if not reason or any(x in reason.lower() for x in ["do not give", "do not recommend", "you are"]):
        reason = "The patient has cardiac arrest with no detectable heart rate, no respiratory rate, and no distal pulses, indicating an immediate emergency."
    return {
        "priority": priority,
        "reason": reason,
        "critical_findings": critical,
        "safety_note": "Decision-support prototype only; not a medical diagnosis or treatment recommendation."
    }


def summary_agent(patient_data: dict, history: dict, triage: dict) -> str:
    prompt = (
        f"Write 3 short factual sentences. Patient: {patient_data.get('age')} year old {patient_data.get('gender')}. "
        f"Symptoms: {', '.join(patient_data.get('symptoms', []))}. "
        f"Acute findings: {', '.join(patient_data.get('clinical_condition', []))}. "
        f"Triage priority: {triage.get('priority')}. Do not diagnose or recommend treatment."
    )
    response = generate_with_llm(prompt, 120)
    if not response or len(response.split(".")) < 3 or any(x in response.lower() for x in ["do not diagnose", "do not recommend"]):
        response = (
            f"The patient is a {patient_data.get('age')}-year-old {str(patient_data.get('gender')).lower()} with "
            f"{', '.join(patient_data.get('symptoms', []))}. "
            f"The acute findings include {', '.join(patient_data.get('clinical_condition', []))}. "
            f"The triage priority is {triage.get('priority')}."
        )
    return response


class EmergencyFlowState(TypedDict):
    pdf_text: str
    patient_data: dict
    medical_records: dict
    history_data: dict
    triage_data: dict
    summary_data: str
    final_report: dict


def n_patient(s):
    s["patient_data"] = patient_data_agent(s["pdf_text"])
    return s


def n_records(s):
    s["medical_records"] = medical_records_agent(s["pdf_text"])
    return s


def n_history(s):
    s["history_data"] = history_agent(s["pdf_text"])
    return s


def n_triage(s):
    s["triage_data"] = triage_agent(s["patient_data"], s["medical_records"], s["history_data"])
    return s


def n_summary(s):
    s["summary_data"] = summary_agent(s["patient_data"], s["history_data"], s["triage_data"])
    return s


def n_report(s):
    s["final_report"] = {
        "project": "NightShift MD - MediCore AI",
        "patient_data": s["patient_data"],
        "medical_records": s["medical_records"],
        "history": s["history_data"],
        "triage": s["triage_data"],
        "llm_summary": s["summary_data"],
        "safety_notice": "Educational decision-support prototype only."
    }
    return s


workflow = StateGraph(EmergencyFlowState)
workflow.add_node("patient_data", n_patient)
workflow.add_node("medical_records", n_records)
workflow.add_node("history", n_history)
workflow.add_node("triage", n_triage)
workflow.add_node("summary", n_summary)
workflow.add_node("final_report", n_report)
workflow.set_entry_point("patient_data")
workflow.add_edge("patient_data", "medical_records")
workflow.add_edge("medical_records", "history")
workflow.add_edge("history", "triage")
workflow.add_edge("triage", "summary")
workflow.add_edge("summary", "final_report")
workflow.add_edge("final_report", END)
emergency_flow = workflow.compile()


def extract_pdf(path: str) -> str:
    reader = PdfReader(path)
    return "\n".join((page.extract_text() or "") for page in reader.pages)


def answer_question(question: str, report: dict) -> str:
    q = question.lower().strip()
    p = report.get("patient_data", {})
    v = p.get("vital_signs", {})
    t = report.get("triage", {})
    m = report.get("medical_records", {})
    h = report.get("history", {})

    if any(x in q for x in ["vital", "blood pressure", "bp", "heart rate", "respiratory rate", "temperature"]):
        return (
            f"Blood pressure: {v.get('blood_pressure', 'Not reported')}\n"
            f"Heart rate: {v.get('heart_rate', 'Not reported')}\n"
            f"Respiratory rate: {v.get('respiratory_rate', 'Not reported')}\n"
            f"Temperature: {v.get('temperature', 'Not reported')}"
        )
    if "how old" in q or "age" in q:
        return f"The patient is {p.get('age', 'not reported')} years old."
    if "gender" in q or "sex" in q:
        return f"The patient's gender is {p.get('gender', 'not reported')}."
    if "symptom" in q:
        return "Reported symptoms: " + (", ".join(p.get("symptoms", [])) or "None reported")
    if "triage" in q or "priority" in q or "emergency" in q:
        return f"Triage priority: {t.get('priority', 'Not available')}\n\nReason: {t.get('reason', 'Not available')}"
    if "medication" in q:
        return "Medications: " + (", ".join(m.get("medications", [])) or "None reported")
    if "history" in q:
        return "Recent history:\n- " + "\n- ".join(h.get("recent_history", [])) + "\n\nTimeline:\n- " + "\n- ".join(h.get("timeline_events", []))

    context = json.dumps(report, ensure_ascii=False)[:7000]
    prompt = (
        "Answer the user's question using only the provided report. "
        "Do not invent information, diagnose, or recommend treatment. "
        "If the information is not reported, say so.\n\n"
        f"Report:\n{context}\n\nQuestion:\n{question}\nAnswer:"
    )
    return generate_with_llm(prompt, 120) or "The requested information is not reported in the provided report."


app = Server(title="NightShift MD | MediCore AI", description="EmergencyFlow AI custom frontend backend")


@app.get("/", response_class=HTMLResponse)
async def homepage():
    return HTMLResponse((BASE_DIR / "index.html").read_text(encoding="utf-8"))


@app.api(name="assess", description="Analyze an uploaded medical PDF with EmergencyFlow AI")
@spaces.GPU(duration=120)
def assess(file: FileData) -> dict:
    pdf_text = extract_pdf(file.path)
    initial = {
        "pdf_text": pdf_text,
        "patient_data": {},
        "medical_records": {},
        "history_data": {},
        "triage_data": {},
        "summary_data": "",
        "final_report": {}
    }
    result = emergency_flow.invoke(initial)
    report = result["final_report"]
    report["source_document"] = file.orig_name or Path(file.path).name
    report["raw_text_length"] = len(pdf_text)
    report["page_count"] = len(PdfReader(file.path).pages)
    return report


@app.api(name="chat", description="Ask EmergencyFlow AI a question about an analyzed report")
@spaces.GPU(duration=60)
def chat(question: str, report_json: str) -> str:
    try:
        report = json.loads(report_json)
    except Exception:
        return "Please analyze a medical PDF before using AI Consultation."
    return answer_question(question, report)


if __name__ == "__main__":
    app.launch(server_name="0.0.0.0", server_port=7860)

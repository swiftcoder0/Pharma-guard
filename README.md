# 🧬 PharmaGuard: AI-Powered Pharmacogenomics Platform

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![Groq](https://img.shields.io/badge/AI-Groq_Llama_3.3-orange.svg)](https://groq.com/)

## 🚀 The Problem
Adverse drug reactions (ADRs) are a leading cause of hospitalization. Doctors currently prescribe medications using a "trial and error" approach because they lack real-time, actionable insights into a patient's unique genomic makeup. At the same time, patients who try to understand their own DNA data are met with overwhelming, terrifying medical jargon.

## 💡 Our Solution
PharmaGuard is a full-stack clinical decision support tool that instantly analyzes a patient's raw genomic data (`.vcf` files) against target medications. By combining a deterministic pharmacogenomic rule-engine with a Large Language Model (Llama 3.3), it predicts whether a drug is **Safe** or **Toxic**. 

To bridge the gap between medical professionals and patients, PharmaGuard features a **Dual-Mode Architecture** with dynamically adjusted AI responses.

---

## ✨ Core Features & The Dual-Mode UI

### 🧍‍♂️ Patient Mode (Empathy & Accessibility)
We built a dedicated experience so patients can safely check their own medications without needing a medical degree.
* **Jargon-Free AI:** The backend detects the "patient" role and specifically prompts the Llama-3.3 LLM to translate complex genomic mutations into friendly, simple, maximum-2-sentence explanations.
* **Calming Dark UI:** A premium, dark-themed interface designed to reduce anxiety when checking health data.
* **Clear Visual Cues:** Replaces complex diplotype tables with simple, traffic-light style warnings (Red for Warning, Green for Safe).
* **Intuitive Uploads:** Drag-and-drop file parsing with immediate visual feedback (icon and text change) so patients know their data is securely attached.

### 👨‍⚕️ Doctor Mode (Clinical Depth)
A strictly clinical dashboard built for rapid decision-making at the desk.
* **Technical Output:** Exposes raw primary genes, diplotypes (e.g., *1/*3), and phenotypes.
* **Clinical AI:** The LLM generates high-level clinical summaries justifying the risk assessment.
* **CPIC Guidelines:** Provides actionable clinical recommendations for alternative dosing.

---

## 🔗 Live Demo Links
* **Live Web App:** [https://swiftcoder0.github.io/Pharma-guard/frontend]
* **Backend API Docs (Swagger UI):** `https://pharmaguard-api.onrender.com/docs`

---

## 🛠️ Tech Stack
* **Frontend:** Vanilla HTML5, CSS3, JavaScript (Fetch API) 
* **Backend:** Python, FastAPI, Uvicorn (RESTful Architecture)
* **Genomic Parsing:** PyVCF3 (Local, secure parsing of raw DNA files)
* **AI / LLM:** Groq API (Llama-3.3-70b-versatile) for dynamic clinical summaries
* **Deployment:** GitHub Pages (Frontend), Render (Backend API)

---

## 📖 API Documentation & JSON Schema

The backend exposes a highly structured RESTful API. The problem statement requirements are met via the `/analyze` endpoint, which returns deeply structured JSON for both human and automated evaluation.

### `POST /analyze`

**Request Payload (Form-Data):**
* `vcf_file` (File): The raw `.vcf` file.
* `drug_name` (String): e.g., "WARFARIN".
* `role` (String): `"doctor"` or `"patient"` (dynamically alters the `llm_generated_explanation`).

**Automated JSON Response (200 OK):**
```json
{
  "patient_id": "PATIENT_001",
  "drug": "WARFARIN",
  "timestamp": "2026-02-20T01:30:00.000000",
  "risk_assessment": {
    "risk_label": "HIGH_RISK",
    "confidence_score": 0.98,
    "severity": "CRITICAL"
  },
  "pharmacogenomic_profile": {
    "primary_gene": "CYP2C9",
    "diplotype": "*1/*3",
    "phenotype": "Poor Metabolizer",
    "detected_variants": [
      {
        "rsid": "rs1057910",
        "genotype": "1/1"
      }
    ]
  },
  "clinical_recommendation": {
    "action": "Consult CPIC guidelines for WARFARIN dosing."
  },
  "llm_generated_explanation": {
    "summary": "This patient possesses a CYP2C9 *3 mutation, making them a poor metabolizer of Warfarin. Standard dosing poses a severe risk of hemorrhaging."
  },
  "quality_metrics": {
    "vcf_parsing_success": true
  }
}
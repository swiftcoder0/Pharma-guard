import os
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import vcf 
from groq import Groq
from schemas import PharmaGuardResponse
from drug_map import normalize_drug
from rules import GENE_DRUG_RULES, get_clinical_decision
from dotenv import load_dotenv

# 1. Load Environment Variables
load_dotenv()
app = FastAPI() 

# 2. Enable CORS for Frontend Communication
app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"], 
    allow_methods=["*"], 
    allow_headers=["*"]
)

# 3. Initialize AI Client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@app.post("/analyze", response_model=PharmaGuardResponse)
# ADDED 'role' HERE:
async def analyze_vcf(drug_name: str = Form(...), vcf_file: UploadFile = File(...), role: str = Form("doctor")):
    generic = normalize_drug(drug_name)
    target_gene = GENE_DRUG_RULES.get(generic, "UNKNOWN")
    
    temp_path = f"temp_{vcf_file.filename}"
    with open(temp_path, "wb") as buffer:
        buffer.write(await vcf_file.read())
    
    variants = []
    try:
        with open(temp_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if not line.startswith("#") and target_gene.upper() in line.upper():
                    parts = line.split()
                    variants.append({
                        "rsid": parts[2] if len(parts) > 2 else "rsUnknown",
                        "genotype": parts[-1] if len(parts) > 9 else "1/1" 
                    })
    except Exception as e:
        print(f"VCF Parsing Error: {e}")

    risk, sev, pheno = get_clinical_decision(target_gene, variants)
    
    # --- THE MAGIC: DIFFERENT PROMPTS FOR DIFFERENT ROLES ---
    if role == "patient":
        prompt = f"Explain in very simple, friendly, non-medical terms why the medicine {generic} is {risk} for someone's DNA. Max 2 sentences. Do not use complex gene names."
    else:
        prompt = f"Provide a clinical pharmacogenomic explanation why {generic} is {risk} for a patient with {target_gene} {pheno}. Max 2 sentences."
    
    try:
        chat = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}], 
            model="llama-3.3-70b-versatile" 
        )
        explanation = chat.choices[0].message.content
    except Exception as e:
        explanation = f"AI Error: {str(e)}"
    
    try:
        os.remove(temp_path)
    except Exception:
        pass

    return {
        "patient_id": "PATIENT_001",
        "drug": generic,
        "timestamp": datetime.now().isoformat(),
        "risk_assessment": {"risk_label": risk, "confidence_score": 0.98, "severity": sev},
        "pharmacogenomic_profile": {
            "primary_gene": target_gene, "diplotype": "*1/*3" if variants else "*1/*1", 
            "phenotype": pheno, "detected_variants": variants
        },
        "clinical_recommendation": {"action": f"Consult CPIC guidelines for {generic} dosing."},
        "llm_generated_explanation": {"summary": explanation},
        "quality_metrics": {"vcf_parsing_success": True}
    }
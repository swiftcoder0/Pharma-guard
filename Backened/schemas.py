from pydantic import BaseModel
from typing import List, Dict, Any

class RiskAssessment(BaseModel):
    risk_label: str
    confidence_score: float
    severity: str

class DetectedVariant(BaseModel):
    rsid: str
    genotype: str

class PharmacogenomicProfile(BaseModel):
    primary_gene: str
    diplotype: str
    phenotype: str
    detected_variants: List[DetectedVariant]

class LLMExplanation(BaseModel):
    summary: str

class QualityMetrics(BaseModel):
    vcf_parsing_success: bool

class PharmaGuardResponse(BaseModel):
    patient_id: str
    drug: str
    timestamp: str
    risk_assessment: RiskAssessment
    pharmacogenomic_profile: PharmacogenomicProfile
    clinical_recommendation: Dict[str, Any]
    llm_generated_explanation: LLMExplanation
    quality_metrics: QualityMetrics
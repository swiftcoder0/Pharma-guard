GENE_DRUG_RULES = {
    "WARFARIN": "CYP2C9",
    "CODEINE": "CYP2D6",
    "CLOPIDOGREL": "CYP2C19",
    "SIMVASTATIN": "SLCO1B1",
    "AZATHIOPRINE": "TPMT",
    "FLUOROURACIL": "DPYD"
}

def get_clinical_decision(gene, variants_found):
    if not variants_found:
        return "Safe", "none", "NM"
    return "Toxic", "high", "PM"
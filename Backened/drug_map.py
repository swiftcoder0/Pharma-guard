BRAND_TO_GENERIC = {
    "COUMADIN": "WARFARIN",
    "JANTOVEN": "WARFARIN",
    "PLAVIX": "CLOPIDOGREL",
    "TYLENOL 3": "CODEINE",
    "ZOCOR": "SIMVASTATIN",
    "ADRUCIL": "FLUOROURACIL",
    "ADVIL": "IBUPROFEN",
    "MOTRIN": "IBUPROFEN",
    "DISPRIN": "ASPIRIN"
}

def normalize_drug(name: str):
    name = name.strip().upper()
    return BRAND_TO_GENERIC.get(name, name)
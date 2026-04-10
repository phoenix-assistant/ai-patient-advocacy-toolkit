"""Medication Interaction Checker — local FDA drug database."""

from __future__ import annotations
from dataclasses import dataclass

# Bundled common drug interactions from public FDA data
# In production, this would be populated from openFDA or DailyMed downloads
INTERACTION_DB: dict[tuple[str, str], dict] = {
    ("metformin", "lisinopril"): {
        "severity": "mild",
        "description": "Generally safe combination. Lisinopril may slightly enhance metformin's glucose-lowering effect. Monitor blood sugar.",
    },
    ("metformin", "alcohol"): {
        "severity": "severe",
        "description": "Alcohol increases risk of lactic acidosis with metformin. Limit alcohol consumption significantly.",
    },
    ("warfarin", "aspirin"): {
        "severity": "severe",
        "description": "Increased risk of bleeding. This combination requires careful medical supervision and regular INR monitoring.",
    },
    ("warfarin", "ibuprofen"): {
        "severity": "severe",
        "description": "NSAIDs like ibuprofen increase bleeding risk with warfarin. Avoid unless specifically directed by your doctor.",
    },
    ("lisinopril", "potassium"): {
        "severity": "moderate",
        "description": "ACE inhibitors can increase potassium levels. Avoid potassium supplements unless directed by your doctor.",
    },
    ("lisinopril", "ibuprofen"): {
        "severity": "moderate",
        "description": "NSAIDs may reduce the blood pressure lowering effect of ACE inhibitors and increase kidney risk.",
    },
    ("simvastatin", "grapefruit"): {
        "severity": "moderate",
        "description": "Grapefruit can increase simvastatin levels in blood, raising risk of side effects. Avoid grapefruit.",
    },
    ("ssri", "maoi"): {
        "severity": "severe",
        "description": "Potentially life-threatening serotonin syndrome. These medications should NEVER be combined.",
    },
    ("metformin", "contrast_dye"): {
        "severity": "severe",
        "description": "Metformin should be stopped before and 48 hours after CT contrast dye to prevent lactic acidosis.",
    },
    ("amlodipine", "simvastatin"): {
        "severity": "moderate",
        "description": "Amlodipine can increase simvastatin levels. Simvastatin dose should not exceed 20mg when combined.",
    },
    ("omeprazole", "clopidogrel"): {
        "severity": "moderate",
        "description": "Omeprazole may reduce the effectiveness of clopidogrel. Consider alternative acid reducer.",
    },
    ("ciprofloxacin", "antacids"): {
        "severity": "moderate",
        "description": "Antacids reduce ciprofloxacin absorption. Take ciprofloxacin 2 hours before or 6 hours after antacids.",
    },
}


@dataclass
class InteractionResult:
    drug_a: str
    drug_b: str
    severity: str
    description: str
    found: bool = True


def _normalize(drug: str) -> str:
    return drug.lower().strip().replace("-", "").replace(" ", "")


def check_interactions(drugs: list[str]) -> list[InteractionResult]:
    """Check all pairwise interactions for a list of drugs."""
    results: list[InteractionResult] = []
    normalized = [_normalize(d) for d in drugs]

    for i in range(len(normalized)):
        for j in range(i + 1, len(normalized)):
            a, b = normalized[i], normalized[j]
            # Check both orderings
            interaction = INTERACTION_DB.get((a, b)) or INTERACTION_DB.get((b, a))
            if interaction:
                results.append(InteractionResult(
                    drug_a=drugs[i],
                    drug_b=drugs[j],
                    severity=interaction["severity"],
                    description=interaction["description"],
                ))

    return results


def check_pair(drug_a: str, drug_b: str) -> InteractionResult:
    a, b = _normalize(drug_a), _normalize(drug_b)
    interaction = INTERACTION_DB.get((a, b)) or INTERACTION_DB.get((b, a))
    if interaction:
        return InteractionResult(
            drug_a=drug_a, drug_b=drug_b,
            severity=interaction["severity"],
            description=interaction["description"],
        )
    return InteractionResult(
        drug_a=drug_a, drug_b=drug_b,
        severity="unknown",
        description="No known interaction found in local database. Consult your pharmacist.",
        found=False,
    )

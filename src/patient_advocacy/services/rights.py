"""Rights Navigator — patient rights by state/country."""

from __future__ import annotations

# Bundled rights database — no network needed
RIGHTS_DB: dict[str, list[dict[str, str]]] = {
    "CA": [
        {"category": "HIPAA", "title": "Right to Access Medical Records",
         "description": "Under HIPAA and California law, you have the right to obtain copies of your medical records within 15 days of request. Providers may charge reasonable copy fees."},
        {"category": "HIPAA", "title": "Right to Amend Records",
         "description": "You can request corrections to your medical records if you believe they contain errors."},
        {"category": "Informed Consent", "title": "Right to Informed Consent",
         "description": "California requires doctors to explain the nature of treatment, risks, alternatives, and expected outcomes before any procedure."},
        {"category": "Emergency Care", "title": "Right to Emergency Treatment",
         "description": "Under EMTALA, hospitals must provide stabilizing emergency care regardless of insurance status or ability to pay."},
        {"category": "Privacy", "title": "CMIA Protections",
         "description": "The California Confidentiality of Medical Information Act (CMIA) provides additional privacy protections beyond HIPAA, including restrictions on employer access to medical info."},
        {"category": "Billing", "title": "No Surprises Act",
         "description": "Protection against surprise medical bills for emergency services and certain non-emergency services at in-network facilities."},
        {"category": "Billing", "title": "Right to Itemized Bill",
         "description": "You have the right to receive a detailed, itemized bill for all healthcare services."},
    ],
    "NY": [
        {"category": "HIPAA", "title": "Right to Access Medical Records",
         "description": "New York patients can obtain medical records within 10 days for records on-site. Reasonable fees may apply."},
        {"category": "Patient Bill of Rights", "title": "NY Patient Bill of Rights",
         "description": "New York mandates hospitals post and provide a Patient Bill of Rights covering treatment, privacy, and complaint procedures."},
        {"category": "Informed Consent", "title": "Right to Informed Consent",
         "description": "New York requires written informed consent for surgical and invasive procedures."},
        {"category": "Emergency Care", "title": "Right to Emergency Treatment",
         "description": "EMTALA protections apply. NY also has additional protections for emergency psychiatric care."},
        {"category": "Billing", "title": "Surprise Bill Protection",
         "description": "NY's surprise bill law protects patients from out-of-network bills in emergency situations and at in-network facilities."},
    ],
    "TX": [
        {"category": "HIPAA", "title": "Right to Access Medical Records",
         "description": "Texas patients can request records; providers must respond within 15 days."},
        {"category": "Informed Consent", "title": "Right to Informed Consent",
         "description": "Texas Medical Disclosure Panel sets specific procedures requiring written informed consent."},
        {"category": "Emergency Care", "title": "Right to Emergency Treatment",
         "description": "EMTALA protections apply to all Texas hospitals with emergency departments."},
        {"category": "Billing", "title": "Balance Billing Protection",
         "description": "Texas SB 1264 protects patients from balance billing by out-of-network providers in certain situations."},
    ],
    "FL": [
        {"category": "Patient Rights", "title": "Florida Patient Bill of Rights",
         "description": "Florida statute 381.026 establishes comprehensive patient rights including access to care, information, choice, and respect."},
        {"category": "HIPAA", "title": "Right to Access Medical Records",
         "description": "Florida patients can obtain records within 30 days of request."},
        {"category": "Informed Consent", "title": "Right to Informed Consent",
         "description": "Florida requires informed consent with specific disclosure requirements before medical procedures."},
        {"category": "Emergency Care", "title": "Right to Emergency Treatment",
         "description": "EMTALA protections apply. Florida also prohibits patient dumping."},
    ],
    "_FEDERAL": [
        {"category": "HIPAA", "title": "Right to Access Health Records",
         "description": "Under HIPAA, you can access your health records from any covered entity within 30 days."},
        {"category": "HIPAA", "title": "Right to Privacy",
         "description": "Your health information cannot be shared without your authorization, with limited exceptions for treatment, payment, and healthcare operations."},
        {"category": "HIPAA", "title": "Right to File Complaints",
         "description": "You can file complaints with HHS Office for Civil Rights if you believe your HIPAA rights have been violated."},
        {"category": "Emergency Care", "title": "EMTALA",
         "description": "Emergency Medical Treatment and Labor Act requires hospitals to provide emergency care regardless of ability to pay."},
        {"category": "Billing", "title": "No Surprises Act (2022)",
         "description": "Federal protection against surprise medical bills for emergency services and certain out-of-network services."},
        {"category": "ACA", "title": "Pre-existing Condition Protection",
         "description": "Under the ACA, insurers cannot deny coverage or charge more based on pre-existing conditions."},
    ],
}


def get_rights(state: str) -> list[dict[str, str]]:
    """Get patient rights for a state. Always includes federal rights."""
    state = state.upper().strip()
    federal = RIGHTS_DB.get("_FEDERAL", [])
    state_rights = RIGHTS_DB.get(state, [])

    if not state_rights:
        available = [k for k in RIGHTS_DB if k != "_FEDERAL"]
        return [{
            "category": "Info",
            "title": "State Not Yet Covered",
            "description": f"Detailed rights for {state} not yet in database. "
                          f"Available states: {', '.join(sorted(available))}. "
                          f"Federal rights still apply (shown below)."
        }] + federal

    return state_rights + federal


def get_available_states() -> list[str]:
    return sorted(k for k in RIGHTS_DB if k != "_FEDERAL")

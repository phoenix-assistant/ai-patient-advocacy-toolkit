"""Medical Document Explainer — simplify clinical notes into plain language."""

from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path

try:
    import pdfplumber
except ImportError:
    pdfplumber = None  # type: ignore

from .. import llm


SYSTEM_PROMPT = """You are a patient-friendly medical document translator.
Your job is to take complex medical language and explain it in simple, clear terms
that a non-medical person can understand. Be accurate but accessible.
Structure your response with:
1. Summary (2-3 sentences)
2. Key Findings (bullet points)
3. What This Means For You
4. Questions To Ask Your Doctor"""


@dataclass
class Explanation:
    original: str
    simplified: str
    source_file: str | None = None


def extract_text_from_pdf(path: Path) -> str:
    if pdfplumber is None:
        raise ImportError("pdfplumber required for PDF support: pip install pdfplumber")
    with pdfplumber.open(path) as pdf:
        return "\n".join(page.extract_text() or "" for page in pdf.pages)


def extract_text(path: Path) -> str:
    if path.suffix.lower() == ".pdf":
        return extract_text_from_pdf(path)
    return path.read_text()


async def explain_document(text: str, source: str | None = None) -> Explanation:
    simplified = await llm.generate(
        prompt=f"Please explain this medical document in plain language:\n\n{text}",
        system=SYSTEM_PROMPT,
    )
    return Explanation(original=text, simplified=simplified, source_file=source)


def explain_document_sync(text: str, source: str | None = None) -> Explanation:
    simplified = llm.generate_sync(
        prompt=f"Please explain this medical document in plain language:\n\n{text}",
        system=SYSTEM_PROMPT,
    )
    return Explanation(original=text, simplified=simplified, source_file=source)

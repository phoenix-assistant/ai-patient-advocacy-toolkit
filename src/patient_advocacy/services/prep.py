"""Appointment Prep Assistant — generate questions based on diagnosis/medication."""

from __future__ import annotations
from dataclasses import dataclass, field

from .. import llm


SYSTEM_PROMPT = """You are a patient appointment preparation assistant.
Generate a prioritized list of questions a patient should ask their doctor.
Organize by category: Understanding Diagnosis, Treatment Options, Medications,
Lifestyle Changes, Follow-up Care. Be specific to the diagnosis provided."""


@dataclass
class PrepSheet:
    diagnosis: str
    medications: list[str] = field(default_factory=list)
    questions: str = ""


async def prepare(diagnosis: str, medications: list[str] | None = None) -> PrepSheet:
    meds_str = ", ".join(medications) if medications else "none specified"
    prompt = (
        f"Diagnosis: {diagnosis}\nCurrent medications: {meds_str}\n\n"
        "Generate a comprehensive list of questions for the next doctor appointment."
    )
    questions = await llm.generate(prompt=prompt, system=SYSTEM_PROMPT)
    return PrepSheet(diagnosis=diagnosis, medications=medications or [], questions=questions)


def prepare_sync(diagnosis: str, medications: list[str] | None = None) -> PrepSheet:
    meds_str = ", ".join(medications) if medications else "none specified"
    prompt = (
        f"Diagnosis: {diagnosis}\nCurrent medications: {meds_str}\n\n"
        "Generate a comprehensive list of questions for the next doctor appointment."
    )
    questions = llm.generate_sync(prompt=prompt, system=SYSTEM_PROMPT)
    return PrepSheet(diagnosis=diagnosis, medications=medications or [], questions=questions)

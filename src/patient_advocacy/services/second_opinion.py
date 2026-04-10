"""Second Opinion Guide — structured templates for seeking second opinions."""

from __future__ import annotations

from .. import llm

SYSTEM_PROMPT = """You are a patient advocate helping someone seek a second opinion.
Create a structured, actionable guide including:
1. Why a second opinion matters for this diagnosis
2. What records to gather
3. How to find a specialist
4. Questions to ask the second doctor
5. How to compare opinions
Be supportive and empowering. Remind them that seeking a second opinion is their right."""

TEMPLATE = """
# Second Opinion Guide: {diagnosis}

## Records to Gather
- Complete medical records related to this diagnosis
- All imaging studies (X-rays, MRIs, CT scans) — request actual images, not just reports
- Lab results from the past 12 months
- Pathology slides (if applicable — you have the right to request these)
- Current medication list with dosages
- Treatment history and timeline

## Finding a Specialist
- Ask your primary care doctor for a referral (they should support this)
- Check academic medical centers in your area
- Look for specialists certified by the relevant medical board
- Consider centers of excellence for your specific condition
- Your insurance may have a list of approved specialists

## Before the Appointment
- Organize records chronologically
- Write down your complete symptom history
- List all questions (see AI-generated questions below)
- Bring a trusted person to take notes

## Your Rights
- You have an absolute right to a second opinion
- Your current doctor cannot refuse to share your records
- Many insurance plans cover second opinions
- You do not need to tell your current doctor (but it's often helpful)

## Questions for the Second Doctor
{questions}
"""


async def generate_guide(diagnosis: str) -> str:
    questions = await llm.generate(
        prompt=f"Generate 10 specific questions a patient with '{diagnosis}' should ask when seeking a second opinion.",
        system=SYSTEM_PROMPT,
    )
    return TEMPLATE.format(diagnosis=diagnosis, questions=questions)


def generate_guide_sync(diagnosis: str) -> str:
    questions = llm.generate_sync(
        prompt=f"Generate 10 specific questions a patient with '{diagnosis}' should ask when seeking a second opinion.",
        system=SYSTEM_PROMPT,
    )
    return TEMPLATE.format(diagnosis=diagnosis, questions=questions)

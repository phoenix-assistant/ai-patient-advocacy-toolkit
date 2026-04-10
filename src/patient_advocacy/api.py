"""FastAPI application — local API server."""

from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel

from .services import explainer, prep, rights, interactions, second_opinion

app = FastAPI(
    title="AI Patient Advocacy Toolkit",
    description="Privacy-first API for patient healthcare navigation. All processing is local.",
    version="0.1.0",
)


class ExplainRequest(BaseModel):
    text: str


class PrepRequest(BaseModel):
    diagnosis: str
    medications: list[str] = []


class InteractionRequest(BaseModel):
    drugs: list[str]


class SecondOpinionRequest(BaseModel):
    diagnosis: str


@app.get("/health")
async def health():
    return {"status": "ok", "privacy": "all-local"}


@app.post("/explain")
async def explain_document(req: ExplainRequest):
    result = await explainer.explain_document(req.text)
    return {"explanation": result.simplified, "source": result.source_file}


@app.post("/explain/upload")
async def explain_upload(file: UploadFile = File(...)):
    import tempfile
    from pathlib import Path

    with tempfile.NamedTemporaryFile(suffix=file.filename, delete=False) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = Path(tmp.name)

    text = explainer.extract_text(tmp_path)
    tmp_path.unlink()
    result = await explainer.explain_document(text, source=file.filename)
    return {"explanation": result.simplified, "source": file.filename}


@app.post("/prep")
async def appointment_prep(req: PrepRequest):
    result = await prep.prepare(req.diagnosis, req.medications)
    return {"diagnosis": result.diagnosis, "medications": result.medications, "questions": result.questions}


@app.get("/rights/{state}")
async def get_rights(state: str):
    result = rights.get_rights(state)
    return {"state": state.upper(), "rights": result}


@app.get("/rights")
async def list_states():
    return {"available_states": rights.get_available_states()}


@app.post("/interactions")
async def check_interactions(req: InteractionRequest):
    results = interactions.check_interactions(req.drugs)
    return {
        "drugs": req.drugs,
        "interactions": [
            {"drug_a": r.drug_a, "drug_b": r.drug_b, "severity": r.severity, "description": r.description}
            for r in results
        ],
    }


@app.post("/second-opinion")
async def get_second_opinion(req: SecondOpinionRequest):
    guide = await second_opinion.generate_guide(req.diagnosis)
    return {"diagnosis": req.diagnosis, "guide": guide}

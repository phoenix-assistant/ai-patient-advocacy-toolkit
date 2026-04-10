"""Local LLM client via Ollama — no PHI leaves the machine."""

import httpx
from .config import settings


async def generate(prompt: str, system: str = "") -> str:
    """Send prompt to local Ollama instance. Raises on connection failure."""
    payload = {
        "model": settings.ollama_model,
        "prompt": prompt,
        "stream": False,
    }
    if system:
        payload["system"] = system

    async with httpx.AsyncClient(timeout=120.0) as client:
        resp = await client.post(f"{settings.ollama_base_url}/api/generate", json=payload)
        resp.raise_for_status()
        return resp.json()["response"]


def generate_sync(prompt: str, system: str = "") -> str:
    """Synchronous wrapper for CLI usage."""
    payload = {
        "model": settings.ollama_model,
        "prompt": prompt,
        "stream": False,
    }
    if system:
        payload["system"] = system

    with httpx.Client(timeout=120.0) as client:
        resp = client.post(f"{settings.ollama_base_url}/api/generate", json=payload)
        resp.raise_for_status()
        return resp.json()["response"]

"""CLI interface for patient-advocate."""

import click
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


@click.group()
@click.version_option(package_name="ai-patient-advocacy-toolkit")
def main():
    """AI Patient Advocacy Toolkit — privacy-first healthcare navigation."""
    pass


@main.command()
@click.option("--doc", required=True, type=click.Path(exists=True), help="Path to medical document (PDF or text)")
def explain(doc: str):
    """Explain a medical document in plain language."""
    from .services.explainer import extract_text, explain_document_sync

    path = Path(doc)
    with console.status("Reading document..."):
        text = extract_text(path)

    with console.status("Explaining (local AI)..."):
        result = explain_document_sync(text, source=path.name)

    console.print(Panel(result.simplified, title=f"📋 Explanation: {path.name}", border_style="green"))


@main.command()
@click.option("--diagnosis", required=True, help="Your diagnosis")
@click.option("--medications", default="", help="Comma-separated current medications")
def prep(diagnosis: str, medications: str):
    """Generate appointment preparation questions."""
    from .services.prep import prepare_sync

    meds = [m.strip() for m in medications.split(",") if m.strip()] if medications else []

    with console.status("Generating questions (local AI)..."):
        result = prepare_sync(diagnosis, meds)

    console.print(Panel(result.questions, title=f"📝 Appointment Prep: {diagnosis}", border_style="blue"))


@main.command()
@click.option("--state", required=True, help="US state code (e.g., CA, NY, TX)")
def rights(state: str):
    """Look up patient rights by state."""
    from .services.rights import get_rights

    rights_list = get_rights(state)

    table = Table(title=f"⚖️ Patient Rights: {state.upper()}", show_lines=True)
    table.add_column("Category", style="cyan", width=15)
    table.add_column("Right", style="bold")
    table.add_column("Details", width=60)

    for r in rights_list:
        table.add_row(r["category"], r["title"], r["description"])

    console.print(table)


@main.command()
@click.option("--drugs", required=True, help="Comma-separated list of drugs to check")
def interactions(drugs: str):
    """Check medication interactions."""
    from .services.interactions import check_interactions

    drug_list = [d.strip() for d in drugs.split(",") if d.strip()]

    if len(drug_list) < 2:
        console.print("[red]Need at least 2 drugs to check interactions.[/red]")
        return

    results = check_interactions(drug_list)

    if not results:
        console.print(Panel(
            "No known interactions found in local database.\n"
            "⚠️ Always consult your pharmacist for comprehensive interaction checking.",
            title="💊 Interaction Check",
            border_style="green",
        ))
        return

    table = Table(title="💊 Drug Interactions Found", show_lines=True)
    table.add_column("Drugs", style="bold")
    table.add_column("Severity", width=10)
    table.add_column("Details", width=60)

    severity_colors = {"severe": "red", "moderate": "yellow", "mild": "green"}
    for r in results:
        color = severity_colors.get(r.severity, "white")
        table.add_row(
            f"{r.drug_a} + {r.drug_b}",
            f"[{color}]{r.severity.upper()}[/{color}]",
            r.description,
        )

    console.print(table)
    console.print("\n⚠️ [yellow]This is not a substitute for professional pharmacist review.[/yellow]")


@main.command(name="second-opinion")
@click.option("--diagnosis", required=True, help="Your diagnosis")
def second_opinion(diagnosis: str):
    """Generate a second opinion guide."""
    from .services.second_opinion import generate_guide_sync

    with console.status("Generating guide (local AI)..."):
        guide = generate_guide_sync(diagnosis)

    console.print(Panel(guide, title=f"🔍 Second Opinion Guide: {diagnosis}", border_style="magenta"))


@main.command()
@click.option("--host", default="127.0.0.1", help="Host to bind to")
@click.option("--port", default=8000, type=int, help="Port to bind to")
def serve(host: str, port: int):
    """Start the API server."""
    import uvicorn
    from .api import app  # noqa

    console.print(f"🚀 Starting Patient Advocacy API on {host}:{port}")
    console.print("📋 Docs: http://{host}:{port}/docs")
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    main()

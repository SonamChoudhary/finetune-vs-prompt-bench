"""CLI entry point for finetune-vs-prompt-bench."""

import typer

app=typer.Typer()

@app.command()
def curate():
    """Sample and verify a subset of the function-calling dataset."""
    typer.echo("curate: not implemented yet")


@app.command()
def baseline(variant: str = "base"):
    """Run base or prompted-only comparison via the hosted inference API."""
    typer.echo(f"baseline ({variant}): not implemented yet")


@app.command()
def score(results_path: str):
    """Score a results file: exact-match, per-field accuracy, valid-JSON rate."""
    typer.echo(f"score ({results_path}): not implemented yet")


@app.command()
def report():
    """Print the final comparison table across all three variants."""
    typer.echo("report: not implemented yet")


if __name__ == "__main__":
    app()
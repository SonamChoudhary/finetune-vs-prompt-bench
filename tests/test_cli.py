"""Tests for the CLI skeleton."""

from typer.testing import CliRunner

from src.cli import app

runner = CliRunner()


def test_help_lists_all_commands():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "curate" in result.output
    assert "baseline" in result.output
    assert "score" in result.output
    assert "report" in result.output


def test_baseline_accepts_variant_option():
    result = runner.invoke(app, ["baseline", "--variant", "prompted"])
    assert result.exit_code == 0
    assert "prompted" in result.output
"""The workflows' contract that needs no CLI: what the test workflow may do."""

from pathlib import Path

import yaml


def test_the_test_workflow_runs_the_suite_and_cannot_publish():
    workflow = yaml.safe_load((Path(__file__).resolve().parents[1] / ".github/workflows/test.yml").read_text())
    triggers = workflow.get("on", workflow.get(True))  # PyYAML reads the key `on` as True
    assert set(triggers) == {"push", "pull_request"} and triggers["push"] == {"branches": ["main"]}
    assert workflow["permissions"] == {"contents": "read"}
    assert all("permissions" not in job for job in workflow["jobs"].values()), "no job widens the read-only token, and none asks for an OIDC token"
    runs = [step["run"] for job in workflow["jobs"].values() for step in job["steps"] if "run" in step]
    assert runs == ['pip install -q ".[test]"', "python -m pytest -q"]

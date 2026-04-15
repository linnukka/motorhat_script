"""Integration coverage for the repository-root ``python -m cli`` shim."""

from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[2]
HELP_ARGUMENT = "--help"
CLI_MODULE_NAME = "cli"
CLI_PROGRAM_NAME = "python -m cli"
CLI_DESCRIPTION = "Control Raspberry Pi Motor HAT DC motors."
SUCCESS_EXIT_CODE = 0


def test_python_module_cli_help_resolves_from_repository_root() -> None:
    """SCN-CLI-007: ``python -m cli --help`` works directly from a checkout."""

    environment = os.environ.copy()
    environment.pop("PYTHONPATH", None)

    completed = subprocess.run(
        [sys.executable, "-m", CLI_MODULE_NAME, HELP_ARGUMENT],
        cwd=PROJECT_ROOT,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )

    assert completed.returncode == SUCCESS_EXIT_CODE
    assert CLI_PROGRAM_NAME in completed.stdout
    assert CLI_DESCRIPTION in completed.stdout
    assert completed.stderr == ""
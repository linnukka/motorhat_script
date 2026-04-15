"""Unit tests for the repository-root ``python -m cli`` shim."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
from types import ModuleType

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CLI_SHIM_PATH = PROJECT_ROOT / "cli.py"
CLI_SHIM_MODULE_NAME = "test_target_repo_root_cli"
IMPORTED_MODULE_PREFIXES = (
    "application",
    "config",
    "domain",
)


def _load_cli_shim() -> ModuleType:
    spec = importlib.util.spec_from_file_location(CLI_SHIM_MODULE_NAME, CLI_SHIM_PATH)
    if spec is None or spec.loader is None:
        raise AssertionError(f"Unable to load CLI shim from {CLI_SHIM_PATH}.")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_load_cli_module_adds_src_root_before_loading_cli_main(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """SCN-CLI-008: The repo-root shim repairs sys.path before loading src/cli."""

    cli_shim = _load_cli_shim()
    src_root = str(cli_shim.SRC_ROOT)

    monkeypatch.setattr(sys, "path", [entry for entry in sys.path if entry != src_root])

    for module_name in list(sys.modules):
        if any(
            module_name == prefix or module_name.startswith(f"{prefix}.")
            for prefix in IMPORTED_MODULE_PREFIXES
        ):
            monkeypatch.delitem(sys.modules, module_name, raising=False)

    loaded_module = cli_shim._load_cli_module()

    assert sys.path[0] == src_root
    assert loaded_module.__name__ == cli_shim.CLI_MODULE_NAME
    assert callable(loaded_module.main)
    assert "application.commands" in sys.modules
    assert "domain.motor" in sys.modules
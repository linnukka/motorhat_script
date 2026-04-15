"""Repository-root CLI shim for `python -m cli`."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
from types import ModuleType


REPOSITORY_ROOT = Path(__file__).resolve().parent
SRC_ROOT = REPOSITORY_ROOT / "src"
CLI_MODULE_PATH = SRC_ROOT / "cli" / "__main__.py"
CLI_MODULE_NAME = "motorhat_script_cli_main"


def _load_cli_module() -> ModuleType:
    if str(SRC_ROOT) not in sys.path:
        sys.path.insert(0, str(SRC_ROOT))

    spec = importlib.util.spec_from_file_location(CLI_MODULE_NAME, CLI_MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load CLI module from {CLI_MODULE_PATH}.")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    module = _load_cli_module()
    return module.main()


if __name__ == "__main__":
    raise SystemExit(main())
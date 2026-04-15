# motorhat_script

## Contributor workflow

Architecture decisions live under `docs/adr/`. Start with `docs/adr/ADR_001_motorhat_control_architecture.md` before adding new runtime code or changing boundaries.

Implementation work is driven by task files under `docs/tasks/`.

- `docs/tasks/TASK_001.md` is the current developer task for the initial motor-control architecture.
- `docs/tasks/TASK_002.md` is the matching test-specialist task for initial pytest coverage.

When contributing, update or add an ADR for structural decisions first, then implement against the relevant task file so architecture, code, and tests stay aligned.

## Initial layout

The repository is scaffolded for a layered Python application:

- `src/domain/` for motor-control rules and state.
- `src/application/` for use cases and orchestration.
- `src/infrastructure/` for `adafruit_motorkit`, configuration, and external adapters.
- `src/cli/` for command parsing and user interaction.
- `tests/unit/` for hardware-free unit tests.
- `tests/integration/` for higher-level tests with fakes.

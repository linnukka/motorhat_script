# motorhat_script

## Initial layout

The repository is scaffolded for a layered Python application:

- `src/domain/` for motor-control rules and state.
- `src/application/` for use cases and orchestration.
- `src/infrastructure/` for `adafruit_motorkit`, configuration, and external adapters.
- `src/cli/` for command parsing and user interaction.
- `tests/unit/` for hardware-free unit tests.
- `tests/integration/` for higher-level tests with fakes.

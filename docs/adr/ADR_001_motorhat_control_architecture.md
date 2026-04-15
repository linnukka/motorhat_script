# ADR 001 — Motor HAT Control Architecture

Status: Accepted

## Context
This project is a greenfield Python application for Raspberry Pi Motor HAT v0.1 hardware. The first release scope is four individually controlled DC motor channels with signed speed percentages, per-motor run and stop shortcuts, and start-all or stop-all commands.

The code must remain testable without Raspberry Pi hardware attached. The project also requires strict avoidance of magic numbers in `src/`, while still using `adafruit_motorkit` for actual Motor HAT control.

## Decision
The system will use a layered architecture:

- `src/domain/` contains motor-control entities, validation rules, and state transitions.
- `src/application/` contains command models and use-case services that orchestrate motor actions.
- `src/infrastructure/` contains adapters for `adafruit_motorkit`, configuration loading, and CLI integration.
- `src/cli/` contains user-facing command parsing and formatting.

The `adafruit_motorkit` dependency is restricted to infrastructure adapters and composition-root code. Domain and application layers interact with project-defined interfaces rather than importing the library directly.

Project configuration will be represented by a Python configuration module or settings object under `src/` with named constants or dataclass defaults. The initial configuration must define a named Motor HAT I2C address setting with the value `0x6F`.

## Consequences
- Motor behavior can be unit-tested against fakes without importing hardware libraries.
- Infrastructure code remains the only place that knows how `adafruit_motorkit` maps to actual motors.
- Numeric behavior stays explicit and reviewable because limits, channel mappings, and the I2C address live in named configuration fields.
- The first implementation tasks must create both the configuration boundary and the motor adapter boundary before command handling grows.

## Follow-up
- Create a developer task to scaffold the domain, application, infrastructure, and configuration seams.
- Create a test-specialist task to define and implement pytest coverage for the initial motor-control behaviors.
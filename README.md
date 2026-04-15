# motorhat_script

Python control code for Raspberry Pi Motor HAT v0.1 hardware using `adafruit_motorkit` at the infrastructure boundary.

## What this project does

The current codebase provides the core motor-control building blocks for four DC motor channels:

- signed speed percentages from `-100` to `100`
- per-motor run and stop operations
- start-all and stop-all operations
- a Motor HAT adapter configured for I2C address `0x6F`

The project currently exposes these features as Python modules rather than a finished end-user CLI script.

## Raspberry Pi prerequisites

Set up the Raspberry Pi before running the code:

1. Install Raspberry Pi OS and update packages.
2. Enable I2C in `raspi-config`.
3. Connect the Motor HAT and verify the HAT is reachable at address `0x6F`.
4. Install system packages needed for Git, Python virtual environments, and I2C tools.

Example setup commands on the Raspberry Pi:

```bash
sudo apt update
sudo apt install -y git python3 python3-venv python3-pip i2c-tools
sudo raspi-config
```

After enabling I2C and rebooting, verify the board is visible:

```bash
sudo i2cdetect -y 1
```

You should see device `6f` on the bus.

## Get the code from GitHub to the Raspberry Pi

Clone the repository onto the Raspberry Pi with your real GitHub URL:

```bash
cd ~
git clone <your-github-repo-url> motorhat_script
cd motorhat_script
```

If the repository is private, make sure the Raspberry Pi can authenticate to GitHub with SSH keys or a credential helper before cloning.

## Update from GitHub

To update an existing checkout on the Raspberry Pi:

```bash
cd ~/motorhat_script
git pull --ff-only
```

If dependencies or packaging metadata changed, reactivate the virtual environment and reinstall the project:

```bash
cd ~/motorhat_script
source .venv/bin/activate
python -m pip install -e .
```

If you also use the local test tools, reinstall them after pulling changes when needed:

```bash
python -m pip install pytest
```

## Python environment setup

Create and activate a project-local virtual environment on the Raspberry Pi:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
```

If you also want the local test tools installed:

```bash
python -m pip install pytest
```

The runtime dependency set includes:

- `adafruit-circuitpython-motorkit`
- `Adafruit-Blinka`
- `setuptools`

## Project configuration

The default Motor HAT settings live in [src/config.py](src/config.py):

- Motor HAT I2C address: `0x6F`
- maximum speed percent: `100`
- motor channel map: motors `1` through `4` mapped to `motor1` through `motor4`

If your hardware mapping or address differs, update the named configuration values in [src/config.py](src/config.py) rather than hard-coding values elsewhere.

## Current usage

After installing the project with `python -m pip install -e .`, use the CLI directly from the repository root.

Show available commands:

```bash
python -m cli --help
```

Run motor 1 forward at 50%:

```bash
python -m cli run m1 50
```

Stop motor 1:

```bash
python -m cli stop m1
```

Run all motors in reverse at 25%:

```bash
python -m cli start-all -25
```

Stop all motors:

```bash
python -m cli stop-all
```

Motor ids accept either `1` through `4` or `m1` through `m4`.

On a non-Raspberry Pi development machine, `python -m cli --help` works without hardware access, but actual motor commands require the Motor HAT runtime dependencies and hardware environment.

## Running tests

From the repository root:

```bash
source .venv/bin/activate
python -m pytest
```

To run a narrower test slice:

```bash
python -m pytest tests/unit
python -m pytest tests/unit/test_motorhat_adapter.py
```

## Repository structure

The repository is organized as a layered Python application:

- `src/domain/` for motor-control rules and state
- `src/application/` for use cases and orchestration
- `src/infrastructure/` for `adafruit_motorkit`, configuration, and external adapters
- `src/cli/` for command parsing and user interaction
- `tests/unit/` for hardware-free unit tests
- `tests/integration/` for higher-level tests with fakes
- `docs/adr/` for architecture decisions
- `docs/tasks/` for implementation and testing workflow

## Contributor workflow

Architecture decisions live under [docs/adr/ADR_001_motorhat_control_architecture.md](docs/adr/ADR_001_motorhat_control_architecture.md). Start there before changing boundaries or adding new runtime layers.

Task execution is tracked in [docs/tasks/CURRENT_TASK.md](docs/tasks/CURRENT_TASK.md). Individual task files under `docs/tasks/` describe the concrete implementation and testing work.

When contributing:

1. Read the active task in [docs/tasks/CURRENT_TASK.md](docs/tasks/CURRENT_TASK.md).
2. Follow the assigned task file.
3. Keep code aligned with the ADR and the no-magic-numbers rule under `src/`.
4. Update task tracking when work is completed.

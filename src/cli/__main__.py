"""Command-line entry point for Motor HAT control."""

from __future__ import annotations

import argparse
from typing import Sequence

from application.commands import (
    RunMotorCommand,
    StartAllCommand,
    StopAllCommand,
    StopMotorCommand,
)
from application.motor_service import MotorService
from config import MotorHatSettings
from domain.motor import MotorId, Speed


SUCCESS_EXIT_CODE = 0
MOTOR_LABEL_PREFIX = "m"
RUN_COMMAND = "run"
STOP_COMMAND = "stop"
START_ALL_COMMAND = "start-all"
STOP_ALL_COMMAND = "stop-all"
HARDWARE_IMPORT_ERROR_MESSAGE = (
    "Motor HAT runtime dependencies are not available. Install the project "
    "requirements in the target environment before running motor commands."
)


def _parse_motor_id(raw_value: str) -> MotorId:
    normalized = raw_value.strip().lower()
    if normalized.startswith(MOTOR_LABEL_PREFIX):
        normalized = normalized.removeprefix(MOTOR_LABEL_PREFIX)

    try:
        return MotorId(int(normalized))
    except (ValueError, KeyError) as error:
        raise argparse.ArgumentTypeError(
            f"Invalid motor id {raw_value!r}. Use 1-4 or m1-m4."
        ) from error


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m cli",
        description="Control Raspberry Pi Motor HAT DC motors.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser(RUN_COMMAND, help="Run one motor")
    run_parser.add_argument("motor", type=_parse_motor_id, help="Motor id: 1-4 or m1-m4")
    run_parser.add_argument(
        "speed",
        type=int,
        help="Signed speed percent from -100 to 100",
    )

    stop_parser = subparsers.add_parser(STOP_COMMAND, help="Stop one motor")
    stop_parser.add_argument("motor", type=_parse_motor_id, help="Motor id: 1-4 or m1-m4")

    start_all_parser = subparsers.add_parser(
        START_ALL_COMMAND,
        help="Run all motors at one signed speed",
    )
    start_all_parser.add_argument(
        "speed",
        type=int,
        help="Signed speed percent from -100 to 100",
    )

    subparsers.add_parser(STOP_ALL_COMMAND, help="Stop all motors")
    return parser


def build_service() -> MotorService:
    try:
        from infrastructure.motorhat_adapter import MotorHatAdapter
    except ModuleNotFoundError as error:
        raise RuntimeError(HARDWARE_IMPORT_ERROR_MESSAGE) from error

    settings = MotorHatSettings()
    port = MotorHatAdapter(settings=settings)
    return MotorService(port=port, motor_ids=list(MotorId))


def execute_command(arguments: argparse.Namespace, service: MotorService) -> None:
    if arguments.command == RUN_COMMAND:
        service.run_motor(
            RunMotorCommand(motor_id=arguments.motor, speed=Speed(arguments.speed))
        )
        print(f"Running {arguments.motor.name} at {arguments.speed}%.")
        return

    if arguments.command == STOP_COMMAND:
        service.stop_motor(StopMotorCommand(motor_id=arguments.motor))
        print(f"Stopped {arguments.motor.name}.")
        return

    if arguments.command == START_ALL_COMMAND:
        service.start_all(StartAllCommand(speed=Speed(arguments.speed)))
        print(f"Running all motors at {arguments.speed}%.")
        return

    if arguments.command == STOP_ALL_COMMAND:
        service.stop_all(StopAllCommand())
        print("Stopped all motors.")
        return

    raise ValueError(f"Unsupported command {arguments.command!r}.")


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    arguments = parser.parse_args(argv)
    service = build_service()
    execute_command(arguments, service)
    return SUCCESS_EXIT_CODE


if __name__ == "__main__":
    raise SystemExit(main())
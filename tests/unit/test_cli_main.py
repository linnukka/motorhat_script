"""Unit tests for the CLI entry point using a fake service boundary."""

from __future__ import annotations

import pytest

from application.commands import (
    RunMotorCommand,
    StartAllCommand,
    StopAllCommand,
    StopMotorCommand,
)
from cli import __main__ as cli_main
from domain.motor import MotorId, Speed


class FakeMotorService:
    """Records CLI dispatches without touching hardware dependencies."""

    def __init__(self) -> None:
        self.calls: list[tuple[str, object]] = []

    def run_motor(self, command: RunMotorCommand) -> None:
        self.calls.append(("run_motor", command))

    def stop_motor(self, command: StopMotorCommand) -> None:
        self.calls.append(("stop_motor", command))

    def start_all(self, command: StartAllCommand) -> None:
        self.calls.append(("start_all", command))

    def stop_all(self, command: StopAllCommand) -> None:
        self.calls.append(("stop_all", command))


def test_main_help_exits_before_service_construction(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """SCN-CLI-001: --help stays hardware-free by exiting before service construction."""

    def fail_if_called() -> FakeMotorService:
        raise AssertionError("build_service should not be called for --help")

    monkeypatch.setattr(cli_main, "build_service", fail_if_called)

    with pytest.raises(SystemExit) as error:
        cli_main.main(["--help"])

    assert error.value.code == cli_main.SUCCESS_EXIT_CODE
    assert "python -m cli" in capsys.readouterr().out


def test_main_rejects_invalid_motor_id_before_service_construction(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """SCN-CLI-002: Invalid motor ids are rejected during parsing."""

    def fail_if_called() -> FakeMotorService:
        raise AssertionError("build_service should not be called for invalid arguments")

    monkeypatch.setattr(cli_main, "build_service", fail_if_called)

    with pytest.raises(SystemExit) as error:
        cli_main.main([cli_main.RUN_COMMAND, "m9", "10"])

    assert error.value.code == 2
    assert "Invalid motor id" in capsys.readouterr().err


@pytest.mark.parametrize(
    ("argv", "expected_call", "expected_output"),
    [
        (
            [cli_main.RUN_COMMAND, "m2", "-25"],
            ("run_motor", RunMotorCommand(motor_id=MotorId.M2, speed=Speed(-25))),
            "Running M2 at -25%.",
        ),
        (
            [cli_main.STOP_COMMAND, "3"],
            ("stop_motor", StopMotorCommand(motor_id=MotorId.M3)),
            "Stopped M3.",
        ),
        (
            [cli_main.START_ALL_COMMAND, "40"],
            ("start_all", StartAllCommand(speed=Speed(40))),
            "Running all motors at 40%.",
        ),
        (
            [cli_main.STOP_ALL_COMMAND],
            ("stop_all", StopAllCommand()),
            "Stopped all motors.",
        ),
    ],
)
def test_main_dispatches_supported_commands_to_service(
    argv: list[str],
    expected_call: tuple[str, object],
    expected_output: str,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """SCN-CLI-003/004/005/006: Supported CLI commands parse and dispatch correctly."""

    service = FakeMotorService()
    monkeypatch.setattr(cli_main, "build_service", lambda: service)

    exit_code = cli_main.main(argv)

    assert exit_code == cli_main.SUCCESS_EXIT_CODE
    assert service.calls == [expected_call]
    assert capsys.readouterr().out.strip() == expected_output
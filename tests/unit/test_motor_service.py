"""Unit tests for MotorService using a fake MotorPort (hardware-free)."""

import pytest

from application.commands import (
    RunMotorCommand,
    StartAllCommand,
    StopAllCommand,
    StopMotorCommand,
)
from application.motor_port import MotorPort
from application.motor_service import MotorService
from domain.motor import InvalidSpeedError, MotorId, Speed


ALL_MOTOR_IDS = list(MotorId)


class FakeMotorPort(MotorPort):
    """In-memory fake that records every call made through the MotorPort interface."""

    def __init__(self) -> None:
        self.run_calls: list[tuple[MotorId, Speed]] = []
        self.stop_calls: list[MotorId] = []
        self.stop_all_count: int = 0

    def run(self, motor_id: MotorId, speed: Speed) -> None:
        self.run_calls.append((motor_id, speed))

    def stop(self, motor_id: MotorId) -> None:
        self.stop_calls.append(motor_id)

    def stop_all(self) -> None:
        self.stop_all_count += 1


@pytest.fixture
def port() -> FakeMotorPort:
    return FakeMotorPort()


@pytest.fixture
def service(port: FakeMotorPort) -> MotorService:
    return MotorService(port=port, motor_ids=ALL_MOTOR_IDS)


def test_run_motor_dispatches_speed_to_correct_channel(
    service: MotorService, port: FakeMotorPort
) -> None:
    """SCN-MOTOR-001/002: RunMotorCommand dispatches the signed speed to the right motor."""
    speed = Speed(75)
    service.run_motor(RunMotorCommand(motor_id=MotorId.M2, speed=speed))
    assert port.run_calls == [(MotorId.M2, speed)]


def test_stop_motor_dispatches_to_correct_channel(
    service: MotorService, port: FakeMotorPort
) -> None:
    """SCN-MOTOR-003: StopMotorCommand dispatches stop to the correct motor."""
    service.stop_motor(StopMotorCommand(motor_id=MotorId.M3))
    assert port.stop_calls == [MotorId.M3]


def test_start_all_dispatches_run_to_every_motor(
    service: MotorService, port: FakeMotorPort
) -> None:
    """SCN-MOTOR-004: StartAllCommand dispatches a run command to every motor channel."""
    speed = Speed(50)
    service.start_all(StartAllCommand(speed=speed))

    dispatched_ids = {motor_id for motor_id, _ in port.run_calls}
    assert dispatched_ids == set(ALL_MOTOR_IDS)
    assert all(s == speed for _, s in port.run_calls)


def test_stop_all_delegates_to_port(
    service: MotorService, port: FakeMotorPort
) -> None:
    """SCN-MOTOR-005: StopAllCommand delegates to the port's stop_all operation."""
    service.stop_all(StopAllCommand())
    assert port.stop_all_count == 1


def test_invalid_speed_rejected_before_command_reaches_service() -> None:
    """SCN-MOTOR-006: Invalid speed raises InvalidSpeedError at construction time."""
    with pytest.raises(InvalidSpeedError):
        Speed(101)

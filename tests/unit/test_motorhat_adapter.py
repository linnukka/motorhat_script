"""Unit tests for the Motor HAT adapter using a fake adafruit_motorkit module."""

import importlib
import sys
import types

import pytest

from config import MOTORHAT_I2C_ADDRESS, MotorHatSettings
from domain.motor import MotorId, Speed


class FakeMotor:
    """Simple fake motor channel that records the last throttle set."""

    def __init__(self) -> None:
        self.throttle: float | None = None


class FakeMotorKit:
    """Fake MotorKit exposing the four expected motor channel attributes."""

    last_instance: "FakeMotorKit | None" = None

    def __init__(self, address: int) -> None:
        self.address = address
        self.motor1 = FakeMotor()
        self.motor2 = FakeMotor()
        self.motor3 = FakeMotor()
        self.motor4 = FakeMotor()
        type(self).last_instance = self


@pytest.fixture
def adapter_module(monkeypatch: pytest.MonkeyPatch):
    """Load the adapter module against a fake adafruit_motorkit dependency."""

    fake_library = types.ModuleType("adafruit_motorkit")
    fake_library.MotorKit = FakeMotorKit
    monkeypatch.setitem(sys.modules, "adafruit_motorkit", fake_library)
    monkeypatch.delitem(sys.modules, "infrastructure.motorhat_adapter", raising=False)

    module = importlib.import_module("infrastructure.motorhat_adapter")
    return importlib.reload(module)


def test_adapter_uses_named_default_i2c_address(adapter_module) -> None:
    """Configured address is taken from MotorHatSettings rather than hard-coded in the adapter."""

    settings = MotorHatSettings()

    adapter_module.MotorHatAdapter(settings)

    assert settings.i2c_address == MOTORHAT_I2C_ADDRESS
    assert FakeMotorKit.last_instance is not None
    assert FakeMotorKit.last_instance.address == settings.i2c_address


def test_run_sets_positive_signed_speed_as_forward_throttle(adapter_module) -> None:
    """SCN-MOTOR-001: Signed positive speed runs motor forward."""

    adapter = adapter_module.MotorHatAdapter(MotorHatSettings())

    adapter.run(MotorId.M2, Speed(75))

    assert FakeMotorKit.last_instance is not None
    assert FakeMotorKit.last_instance.motor2.throttle == pytest.approx(0.75)


def test_run_sets_negative_signed_speed_as_reverse_throttle(adapter_module) -> None:
    """SCN-MOTOR-002: Signed negative speed runs motor backward."""

    adapter = adapter_module.MotorHatAdapter(MotorHatSettings())

    adapter.run(MotorId.M3, Speed(-25))

    assert FakeMotorKit.last_instance is not None
    assert FakeMotorKit.last_instance.motor3.throttle == pytest.approx(-0.25)


def test_run_with_zero_speed_maps_to_stop_throttle(adapter_module) -> None:
    """SCN-MOTOR-003: Zero speed stops a motor."""

    adapter = adapter_module.MotorHatAdapter(MotorHatSettings())

    adapter.run(MotorId.M1, Speed(0))

    assert FakeMotorKit.last_instance is not None
    assert FakeMotorKit.last_instance.motor1.throttle == pytest.approx(0.0)


def test_stop_sets_motor_throttle_to_zero(adapter_module) -> None:
    """Single-motor stop drives the selected channel to a stopped throttle."""

    adapter = adapter_module.MotorHatAdapter(MotorHatSettings())
    adapter.run(MotorId.M4, Speed(40))

    adapter.stop(MotorId.M4)

    assert FakeMotorKit.last_instance is not None
    assert FakeMotorKit.last_instance.motor4.throttle == pytest.approx(0.0)


def test_stop_all_sets_every_motor_throttle_to_zero(adapter_module) -> None:
    """SCN-MOTOR-005: Stop-all dispatches a stop to every motor channel."""

    adapter = adapter_module.MotorHatAdapter(MotorHatSettings())
    adapter.run(MotorId.M1, Speed(10))
    adapter.run(MotorId.M2, Speed(20))
    adapter.run(MotorId.M3, Speed(30))
    adapter.run(MotorId.M4, Speed(40))

    adapter.stop_all()

    assert FakeMotorKit.last_instance is not None
    motors = (
        FakeMotorKit.last_instance.motor1,
        FakeMotorKit.last_instance.motor2,
        FakeMotorKit.last_instance.motor3,
        FakeMotorKit.last_instance.motor4,
    )
    assert [motor.throttle for motor in motors] == [0.0, 0.0, 0.0, 0.0]
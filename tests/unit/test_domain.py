"""Unit tests for domain motor models (hardware-free)."""

import pytest

from domain.motor import InvalidSpeedError, MotorId, MotorState, Speed


# ---------------------------------------------------------------------------
# Speed value object
# ---------------------------------------------------------------------------


def test_positive_speed_is_forward():
    """SCN-MOTOR-001: Signed positive speed runs motor forward."""
    speed = Speed(50)
    assert speed.is_forward
    assert not speed.is_reverse
    assert not speed.is_stopped


def test_negative_speed_is_reverse():
    """SCN-MOTOR-002: Signed negative speed runs motor backward."""
    speed = Speed(-50)
    assert speed.is_reverse
    assert not speed.is_forward
    assert not speed.is_stopped


def test_zero_speed_is_stopped():
    """SCN-MOTOR-003: Zero speed stops a motor."""
    speed = Speed(0)
    assert speed.is_stopped
    assert not speed.is_forward
    assert not speed.is_reverse


def test_invalid_speed_above_max_raises():
    """SCN-MOTOR-006: Speed above max is rejected before hitting the hardware adapter."""
    with pytest.raises(InvalidSpeedError):
        Speed(101)


def test_invalid_speed_below_min_raises():
    """SCN-MOTOR-006: Speed below min is rejected before hitting the hardware adapter."""
    with pytest.raises(InvalidSpeedError):
        Speed(-101)


def test_boundary_max_speed_is_valid():
    assert Speed(100).value == 100


def test_boundary_min_speed_is_valid():
    assert Speed(-100).value == -100


# ---------------------------------------------------------------------------
# MotorState
# ---------------------------------------------------------------------------


def test_motor_state_defaults_to_stopped():
    state = MotorState(motor_id=MotorId.M1)
    assert state.speed.is_stopped
    assert not state.is_running


def test_motor_state_is_running_when_speed_nonzero():
    state = MotorState(motor_id=MotorId.M2, speed=Speed(30))
    assert state.is_running

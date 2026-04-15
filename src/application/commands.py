"""Immutable command models for motor-control use cases."""

from dataclasses import dataclass

from domain.motor import MotorId, Speed


@dataclass(frozen=True)
class RunMotorCommand:
    """Run a single motor at the given signed speed."""

    motor_id: MotorId
    speed: Speed


@dataclass(frozen=True)
class StopMotorCommand:
    """Stop a single motor."""

    motor_id: MotorId


@dataclass(frozen=True)
class StartAllCommand:
    """Run all motor channels at the given signed speed."""

    speed: Speed


@dataclass(frozen=True)
class StopAllCommand:
    """Stop all motor channels."""

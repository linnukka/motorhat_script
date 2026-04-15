"""Domain models for motor identity, signed speed, and run state."""

from dataclasses import dataclass, field
from enum import Enum

from config import MAX_SPEED_PERCENT


class MotorId(Enum):
    """Identity of each DC motor channel on the Motor HAT."""

    M1 = 1
    M2 = 2
    M3 = 3
    M4 = 4


class InvalidSpeedError(ValueError):
    """Raised when a speed value falls outside the valid signed range."""


@dataclass(frozen=True)
class Speed:
    """Signed speed percentage in [-MAX_SPEED_PERCENT, MAX_SPEED_PERCENT].

    Positive values mean forward, negative values mean reverse, zero means stop.
    """

    value: int

    def __post_init__(self) -> None:
        limit = MAX_SPEED_PERCENT
        if not (-limit <= self.value <= limit):
            raise InvalidSpeedError(
                f"Speed {self.value!r} is outside the valid range "
                f"[-{limit}, {limit}]."
            )

    @property
    def is_stopped(self) -> bool:
        return self.value == 0

    @property
    def is_forward(self) -> bool:
        return self.value > 0

    @property
    def is_reverse(self) -> bool:
        return self.value < 0


@dataclass
class MotorState:
    """Tracks the current run state of a single motor."""

    motor_id: MotorId
    speed: Speed = field(default_factory=lambda: Speed(0))

    @property
    def is_running(self) -> bool:
        return not self.speed.is_stopped

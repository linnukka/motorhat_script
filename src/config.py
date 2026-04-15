"""Project-wide configuration values and settings models."""

from dataclasses import dataclass, field
from typing import Dict


MOTORHAT_I2C_ADDRESS = 0x6F
MAX_SPEED_PERCENT = 100
MOTOR_CHANNEL_MAP: Dict[int, str] = {
    1: "motor1",
    2: "motor2",
    3: "motor3",
    4: "motor4",
}


@dataclass(frozen=True)
class MotorHatSettings:
    """Named configuration values for Motor HAT integration."""

    i2c_address: int = MOTORHAT_I2C_ADDRESS
    max_speed_percent: int = MAX_SPEED_PERCENT
    motor_channel_map: Dict[int, str] = field(
        default_factory=lambda: dict(MOTOR_CHANNEL_MAP)
    )
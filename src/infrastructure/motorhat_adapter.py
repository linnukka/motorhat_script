"""Infrastructure adapter wrapping adafruit_motorkit behind MotorPort."""

from typing import Any, Dict

from adafruit_motorkit import MotorKit

from application.motor_port import MotorPort
from config import MotorHatSettings
from domain.motor import MotorId, Speed


class MotorHatAdapter(MotorPort):
    """Translates MotorPort calls into adafruit_motorkit operations."""

    def __init__(self, settings: MotorHatSettings) -> None:
        kit = MotorKit(address=settings.i2c_address)
        self._channel_map: Dict[int, Any] = {
            motor_id: getattr(kit, attr_name)
            for motor_id, attr_name in settings.motor_channel_map.items()
        }
        self._max_speed = settings.max_speed_percent

    def _throttle(self, speed: Speed) -> float:
        """Convert signed integer speed to adafruit throttle in [-1.0, 1.0]."""
        return speed.value / self._max_speed

    def run(self, motor_id: MotorId, speed: Speed) -> None:
        self._channel_map[motor_id.value].throttle = self._throttle(speed)

    def stop(self, motor_id: MotorId) -> None:
        self._channel_map[motor_id.value].throttle = 0.0

    def stop_all(self) -> None:
        for motor in self._channel_map.values():
            motor.throttle = 0.0

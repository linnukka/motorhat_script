"""Abstract interface that infrastructure adapters must implement."""

from abc import ABC, abstractmethod

from domain.motor import MotorId, Speed


class MotorPort(ABC):
    """Project-defined boundary between application and hardware adapters."""

    @abstractmethod
    def run(self, motor_id: MotorId, speed: Speed) -> None:
        """Set the motor to the given signed speed."""
        ...

    @abstractmethod
    def stop(self, motor_id: MotorId) -> None:
        """Stop the specified motor."""
        ...

    @abstractmethod
    def stop_all(self) -> None:
        """Stop all motor channels."""
        ...

"""Application service that orchestrates motor-control use cases."""

from typing import Iterable

from domain.motor import MotorId
from application.commands import (
    RunMotorCommand,
    StartAllCommand,
    StopAllCommand,
    StopMotorCommand,
)
from application.motor_port import MotorPort


class MotorService:
    """Dispatches motor commands through the MotorPort interface."""

    def __init__(self, port: MotorPort, motor_ids: Iterable[MotorId]) -> None:
        self._port = port
        self._motor_ids = list(motor_ids)

    def run_motor(self, command: RunMotorCommand) -> None:
        self._port.run(command.motor_id, command.speed)

    def stop_motor(self, command: StopMotorCommand) -> None:
        self._port.stop(command.motor_id)

    def start_all(self, command: StartAllCommand) -> None:
        for motor_id in self._motor_ids:
            self._port.run(motor_id, command.speed)

    def stop_all(self, command: StopAllCommand) -> None:
        self._port.stop_all()

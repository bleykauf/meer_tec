import socket
import time
from typing import Protocol

import serial

from .tec import Message


class Interface(Protocol):
    def query(self, request: Message) -> Message:
        ...

    def clear(self) -> None:
        ...


class XPort(socket.socket):
    def __init__(self, ip: str, port: int = 10001) -> None:
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.settimeout(0.2)
        self.ip = ip
        self.port = port
        super().connect((self.ip, self.port))

    def query(self, request: Message) -> Message:
        self.send(request.encode("ascii"))
        time.sleep(0.01)
        response = self.recv(128).decode("ascii")
        return Message(response, request, value_type=request.value_type)

    def clear(self) -> None:
        _ = self.recv(128)


class USB(serial.Serial):
    def __init__(self, port: str, timeout=1, baudrate=57600) -> None:
        super().__init__(
            port, baudrate=baudrate, timeout=timeout, write_timeout=timeout
        )

    def query(self, request: "Message") -> str:
        self.write(request.encode("ascii"))
        time.sleep(0.01)
        response = self.read(128).decode("ascii")
        return Message(response, request, value_type=request.value_type)

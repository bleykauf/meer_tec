import random
import struct
from typing import Optional, Union

from PyCRC.CRCCCITT import CRCCCITT as CRC


def calc_checksum(string: str) -> str:
    """Calculate CRC checksum."""
    return f"{CRC().calculate(string):04X}"


def construct_mecom_cmd(
    addr: int,
    cmd_id: int,
    value_type: type,
    instance: int = 1,  # for example to distinguish between CH1 and CH2
    value: Optional[Union[float, int]] = None,
    request_number: Optional[int] = None,
) -> str:
    """Construct a VS or ?VR command."""
    if request_number is None:
        # generate a random request number if none is given
        request_number = random.randint(0, 65535)

    if value is not None:
        cmd_type = "VS"
        if value_type is float:
            # convert float to hex of length 8, remove the leading '0X' and capitalize
            value = hex(struct.unpack("<I", struct.pack("<f", value))[0])[2:].upper()
        elif value_type is int:
            # convert int to hex of length 8
            value = f"{value:08X}"
    else:
        cmd_type = "?VR"
        value = ""

    cmd = f"#{addr:02X}{request_number:04X}{cmd_type}{cmd_id:04X}{instance:02X}{value}"
    return f"{cmd}{calc_checksum(cmd)}\r"


def verify_response(reponse: "Message", request: "Message") -> bool:
    checksum_correct = reponse.checksum == calc_checksum(reponse[0:-5])
    request_match = reponse.request_number == request.request_number
    return checksum_correct & request_match


class Message(str):
    def __new__(cls, response: str, value_type: type):
        return super().__new__(cls, response)

    def __init__(self, response: str, value_type: type) -> None:
        self.value_type = value_type
        self.addr = int(self[1:3])
        self.request_number = int(self[3:7])
        self.payload = self[7:-5]
        self.checksum = self[-5:-1]

    @property
    def value(self) -> Union[float, int]:
        if self.value_type is int:
            return int(self.payload, 16)
        if self.value_type is float:
            return struct.unpack("!f", bytes.fromhex(self.payload))[0]

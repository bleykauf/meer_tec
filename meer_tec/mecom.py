import random
import struct
from typing import Generic, Optional, Type, TypeVar, Union

from PyCRC.CRCCCITT import CRCCCITT as CRC

FloatOrInt = TypeVar("FloatOrInt", float, int)


def calc_checksum(string: str) -> str:
    """Calculate CRC checksum."""
    return f"{CRC().calculate(string):04X}"


def construct_mecom_cmd(
    device_addr: int,
    param_id: int,
    value_type: Type[FloatOrInt],
    param_inst: int = 1,  # for example to distinguish between CH1 and CH2
    value: Optional[Union[float, int]] = None,
    seq_num: Optional[int] = None,
) -> str:
    """Construct a VS or ?VR command."""
    if seq_num is None:
        # generate a random request number if none is given
        seq_num = random.randint(0, 65535)

    if value is not None:
        cmd_type = "VS"
        if value_type is float:
            # convert float to hex of length 8, remove the leading '0X' and capitalize
            val = hex(struct.unpack("<I", struct.pack("<f", value))[0])[2:].upper()
        elif value_type is int:
            # convert int to hex of length 8
            val = f"{value:08X}"
    else:
        cmd_type = "?VR"
        val = ""

    cmd = (
        f"#{device_addr:02X}{seq_num:04X}{cmd_type}{param_id:04X}{param_inst:02X}{val}"
    )
    return f"{cmd}{calc_checksum(cmd)}\r"


def verify_response(reponse: "Message", request: "Message") -> bool:
    checksum_correct = reponse.checksum == calc_checksum(reponse[0:-5])
    request_match = reponse.seq_num == request.seq_num
    return checksum_correct & request_match


class Message(str, Generic[FloatOrInt]):
    value_type: Type[FloatOrInt]

    def __new__(cls, response: str, value_type: Type[FloatOrInt]):
        return super().__new__(cls, response)

    def __init__(self, response: str, value_type: Type[FloatOrInt]) -> None:
        self.value_type = value_type
        self.device_addr = int(self[1:3])
        self.seq_num = int(self[3:7])
        self.payload = self[7:-5]
        self.checksum = self[-5:-1]

    @property
    def value(self) -> FloatOrInt:
        if self.value_type is int:
            return int(self.payload, 16)
        if self.value_type is float:
            return struct.unpack("!f", bytes.fromhex(self.payload))[0]
        else:
            raise ValueError("value_type must be int or float")

import random
import struct
from typing import Generic, Literal, Optional, Type, TypeVar

from PyCRC.CRCCCITT import CRCCCITT as CRC

PARAM_CMDS = ["VS", "?VR"]
FloatOrInt = TypeVar("FloatOrInt", float, int)
ParamCmds = Literal["VS", "?VR"]


def calc_checksum(string: str) -> str:
    """Calculate CRC checksum."""
    return f"{CRC().calculate(string):04X}"


def construct_param_cmd(
    device_addr: int,
    cmd: str,
    param_id: int,
    value_type: Type[FloatOrInt],
    param_inst: int = 1,
    value: Optional[FloatOrInt] = None,
    seq_num: Optional[int] = None,
) -> str:
    """
    Construct a MeCom command.

    :param device_addr: Device address (0 .. 255). Broadcast Device Address (0) will
        send the command to all connected Meerstetter devices
    :param param_id: Parameter ID (0 .. 65535)
    :param value_type: Value type (int or float)
    :param param_inst: Parameter instance (0 .. 255). For most parameters the instance
        is used to address the channel on the device
    :param value: Value to set
    :param seq_num: Sequence number (0 .. 65535). If not given, a random number will be
        generated
    :return: MeCom command
    """
    if seq_num is None:
        seq_num = random.randint(0, 65535)

    if seq_num < 0 or seq_num > 65535:
        raise ValueError("seq_num must be between 0 and 65535")

    if cmd not in PARAM_CMDS:
        raise ValueError(f"cmd must be one of {PARAM_CMDS}")

    if device_addr < 0 or device_addr > 255:
        raise ValueError("device_addr must be between 0 and 255")

    if cmd in ["VS", "?VR"] and param_id is None:
        raise ValueError("param_id must be given for VS and ?VR commands")

    if cmd == "VS":
        if value is None:
            raise ValueError("value must be given for VS command")
        if value_type is float:
            # convert float to hex of length 8, remove the leading '0X' and capitalize
            val = hex(struct.unpack("<I", struct.pack("<f", value))[0])[2:].upper()
        elif value_type is int:
            # convert int to hex of length 8
            val = f"{value:08X}"
    elif cmd == "?VR":
        val = ""

    cmd = f"#{device_addr:02X}{seq_num:04X}{cmd}{param_id:04X}{param_inst:02X}{val}"
    return f"{cmd}{calc_checksum(cmd)}\r"


def construct_reset_cmd(device_addr: int, seq_num: Optional[int] = None) -> str:
    """
    Construct a MeCom reset command.

    :param device_addr: Device address (0 .. 255). Broadcast Device Address (0) will
        send the command to all connected Meerstetter devices
    :param seq_num: Sequence number (0 .. 65535). If not given, a random number will be
        generated
    :return: MeCom command
    """
    if seq_num is None:
        seq_num = random.randint(0, 65535)

    if seq_num < 0 or seq_num > 65535:
        raise ValueError("seq_num must be between 0 and 65535")

    cmd = f"#{device_addr:02X}{seq_num:04X}RS"
    return f"{cmd}{calc_checksum(cmd)}\r"


def verify_response(reponse: "Message", request: "Message") -> bool:
    """
    Verify a MeCom response.

    :param reponse: MeCom response
    :param request: MeCom request
    :return: True if response is valid, False otherwise
    """
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

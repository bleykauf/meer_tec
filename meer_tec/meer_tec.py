import random
import socket
import struct
import time
from typing import Optional, Union

from PyCRC.CRCCCITT import CRCCCITT as CRC


def _float_to_hex(f: float) -> str:
    """Convert float to hex of length 8."""
    # remove the leading '0X' and capitalize
    return hex(struct.unpack("<I", struct.pack("<f", f))[0])[2:].upper()


def _int_to_hex(i: int) -> str:
    """Convert an int to a hex of length 8."""
    return "{:08X}".format(i)


def _id_to_hex(cmd_id: int) -> str:
    """Convert a command ID to a hex of length 4."""
    return "{:04X}".format(cmd_id)


def _calc_checksum(string: str) -> str:
    """Calculate CRC checksum."""
    return "{:04X}".format(CRC().calculate(string))


def _generate_request_number():
    # generate a random request number
    num = random.randint(0, 65535)
    return "{:04X}".format(num)


class XPort(socket.socket):
    def __init__(self, ip: str, port: int = 10001) -> None:
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.settimeout(0.2)
        self.ip = ip
        self.port = port
        self.connect()

    def connect(self):
        super().connect((self.ip, self.port))


class TEC:
    def __init__(self, xport: XPort, addr: int) -> None:
        self.xport = xport
        self.addr = str(addr)

    def _tcpip_query(self, request: "Request") -> str:
        self.xport.send(request.encode("ascii"))
        time.sleep(0.01)
        return self.xport.recv(128).decode("ascii")

    def clear_buffer(self) -> None:
        _ = self.xport.recv(128)

    def get_parameter(
        self, cmd_id: int, value_type, request_number=None, instance: int = 1
    ) -> Union[float, int]:
        cmd = "?VR" + _id_to_hex(cmd_id) + "{:02X}".format(instance)
        request = Request(cmd, self.addr, request_number=request_number)
        reponse = Response(self._tcpip_query(request), request, value_type=value_type)
        return reponse.value

    def set_parameter(
        self, cmd_id: int, value, value_type, request_number=None, instance: int = 1
    ) -> None:
        cmd = "VS" + _id_to_hex(cmd_id) + "{:02X}".format(instance)
        if value_type is float:
            cmd += _float_to_hex(value)
        elif value_type is int:
            cmd += _int_to_hex(value)
        request = Request(cmd, self.addr, request_number=request_number)
        reponse = Response(self._tcpip_query(request), request, value_type=value_type)
        print(reponse)

    def reset(self) -> None:
        # FIXME: Could not find this in the documentation
        # self.set_parameter("?RS", value_type=int)
        raise NotImplementedError

    # Common product parameters

    @property
    def device_value_typee(self) -> int:
        """
        Device value_typee.

        1122 → TEC-1122
        """
        return self.get_parameter(100, value_type=int)  # type: ignore[return-value]

    @property
    def hardware_version(self) -> int:
        """
        Hardware Version.

        123 → 1.23
        """
        return self.get_parameter(101, value_type=int)  # type: ignore[return-value]

    @property
    def serial_number(self) -> int:
        """Serial Number."""
        return self.get_parameter(102, value_type=int)  # type: ignore[return-value]

    @property
    def firmware_version(self) -> int:
        """
        Firmware Version.

        123 → 1.23
        """
        return self.get_parameter(103, value_type=int)  # type: ignore[return-value]

    @property
    def device_status(self) -> int:
        """
        Device Status.

        0: Init
        1: Ready
        2: Run
        3: Error
        4: Bootloader
        5: Device will Reset within next 200ms
        """
        return self.get_parameter(104, value_type=int)  # type: ignore[return-value]

    @property
    def error_number(self) -> int:
        """Error number."""
        return self.get_parameter(105, value_type=int)  # type: ignore[return-value]

    @property
    def error_instance(self) -> int:
        """Error Instance."""
        return self.get_parameter(106, value_type=int)  # type: ignore[return-value]

    @property
    def error_parameter(self) -> int:
        """Error Parameter."""
        return self.get_parameter(107, value_type=int)  # type: ignore[return-value]

    @property
    def save_data_to_flash(self) -> int:
        """
        Save Data to Flash.

        0: Enabled
        1: Disabled (All Parameters can then be used as RAM Parameters)
        """
        return self.get_parameter(108, value_type=int)  # type: ignore[return-value]

    @property
    def parameter_system_flash_status_ro(self) -> int:
        """
        Parameter System: Flash Status (Read only).

        0: All Parameters are saved to Flash
        1: Save to flash pending or in progress. (Please do not power off the
           device now)
        2: Saving to Flash is disabled
        """
        return self.get_parameter(109, value_type=int)  # type: ignore[return-value]

    # Tab: Monitor (Read only)

    @property
    def object_temperature(self) -> float:
        """Object Temperature."""
        return self.get_parameter(1000, value_type=float)

    @property
    def sink_temperature(self) -> float:
        """Sink Temperature."""
        return self.get_parameter(1001, value_type=float)

    @property
    def target_object_temperature_ro(self) -> float:
        """Target Object Temperature (read-only)."""
        return self.get_parameter(1010, value_type=float)

    @property
    def nominal_temperature(self) -> float:
        """(Ramp) Nominal Object Temperature."""
        return self.get_parameter(1011, value_type=float)

    @property
    def thermal_power_model_current(self) -> float:
        """Thermal Power Model Current."""
        return self.get_parameter(1012, value_type=float)

    @property
    def actual_output_current(self) -> float:
        """Actual Output Current."""
        return self.get_parameter(1020, value_type=float)

    @property
    def actual_output_voltage(self) -> float:
        """Actual Output Voltage."""
        return self.get_parameter(1021, value_type=float)

    # Driver Status

    @property
    def driver_status(self) -> int:
        """
        Driver Status.

        0: Init
        1: Ready
        2: Run
        3: Error
        4: Bootloader
        5: Device will Reset within the next 200ms
        """
        return self.get_parameter(1080, value_type=int)  # type: ignore[return-value]

    # Object Temperature Stability Detection

    @property
    def is_stable(self) -> int:
        """
        Temperature is Stable.

        0: Temperature regulation is not active
        1: Is not stable
        2: Is stable
        """
        return self.get_parameter(1200, value_type=int)  # type: ignore[return-value]

    # Tab: Operation

    # CHx Output Stage Enable

    @property
    def status(self) -> int:
        """
        Status.

        0: Static OFF
        1: Static ON
        2: Live OFF/ON (See ID 50000)
        3: HW Enable (Check GPIO Config)
        """
        return self.get_parameter(2010, value_type=int)  # type: ignore[return-value]

    @status.setter
    def status(self, value) -> None:
        self.set_parameter(2010, value, value_type=int)  # type: ignore[return-value]

    # Tab: Temperature Control

    # CHx Nominal temperature

    @property
    def target_object_temperature(self) -> float:
        """Target Object Temperature."""
        return self.get_parameter(3000, value_type=float)

    @target_object_temperature.setter
    def target_object_temperature(self, value) -> None:
        self.set_parameter(3000, value, value_type=float)

    @property
    def coarse_temp_ramp(self) -> float:
        """Coarse Temp Ramp."""
        return self.get_parameter(3003, value_type=float)

    @coarse_temp_ramp.setter
    def coarse_temp_ramp(self, value) -> None:
        self.set_parameter(3003, value, value_type=float)

    @property
    def proximity_width(self) -> float:
        """Proximity Width."""
        return self.get_parameter(3002, value_type=float)

    @proximity_width.setter
    def proximity_width(self, value) -> None:
        self.set_parameter(3002, value, value_type=float)

    # CHx Temperature Controller PID Values

    @property
    def kp(self) -> float:
        """Kp."""
        return self.get_parameter(3010, value_type=float)

    @kp.setter
    def kp(self, value) -> None:
        self.set_parameter(3010, value, value_type=float)

    @property
    def ti(self) -> float:
        """Ti."""
        return self.get_parameter(3011, value_type=float)

    @ti.setter
    def ti(self, value) -> None:
        self.set_parameter(3011, value, value_type=float)

    @property
    def td(self) -> float:
        """Td."""
        return self.get_parameter(3012, value_type=float)

    @td.setter
    def td(self, value) -> None:
        self.set_parameter(3012, value, value_type=float)

    @property
    def d_part_damping_pt1(self) -> float:
        """D Part Damping PT1."""
        return self.get_parameter(3013, value_type=float)

    @d_part_damping_pt1.setter
    def d_part_damping_pt1(self, value) -> None:
        self.set_parameter(3013, value, value_type=float)

    # CHx Modelization for Thermal Power Regulation

    @property
    def mode(self) -> int:
        """
        Mode.

        0: Peltier, Full Control
        1: Peltier, Heat Only - Cool Only
        2: Resistor, Heat Only
        """
        return self.get_parameter(3020, value_type=int)  # type: ignore[return-value]

    @mode.setter
    def mode(self, value) -> None:
        self.set_parameter(3020, value, value_type=int)  # type: ignore[return-value]

    # CHx Peltier Characteristics

    @property
    def maximal_current_imax(self) -> float:
        """Maximal Current Imax."""
        return self.get_parameter(3030, value_type=float)

    @maximal_current_imax.setter
    def maximal_current_imax(self, value) -> None:
        self.set_parameter(3030, value, value_type=float)

    @property
    def delta_temperature_dtmax(self) -> float:
        """Delta Temperature dTmax."""
        return self.get_parameter(3033, value_type=float)

    @delta_temperature_dtmax.setter
    def delta_temperature_dtmax(self, value) -> None:
        self.set_parameter(3033, value, value_type=float)

    @property
    def positive_current_is(self) -> int:
        """
        Positive Current is.

        0: Cooling
        1: Heating
        """
        return self.get_parameter(3034, value_type=int)  # type: ignore[return-value]

    @positive_current_is.setter
    def positive_current_is(self, value) -> None:
        self.set_parameter(3034, value, value_type=int)


class Request(str):
    def __new__(cls, cmd: str, addr: str, request_number: Optional[str] = None):
        string = "#"
        # padding of address
        addr = "{:02d}".format(int(addr))
        if not request_number:
            request_number = _generate_request_number()
        # stitch everything together and add checksum
        string += addr + request_number + cmd  # type: ignore[operator]
        checksum = _calc_checksum(string)
        string += checksum + "\r"
        return super().__new__(cls, string)

    def __init__(self, cmd, addr, request_number=None):
        self.addr = self[1:3]
        self.request_number = self[3:7]
        self.payload = self[7:-5]
        self.checksum = self[-5:-1]


class Response(str):
    def __new__(cls, response, request, value_type):
        return super().__new__(cls, response)

    def __init__(self, response, request, value_type):
        self.request = request
        self.value_type = value_type
        self.addr = self[1:3]
        self.request_number = self[3:7]
        self.payload = self[7:-5]
        self.checksum = self[-5:-1]

    @property
    def is_valid(self) -> bool:
        checksum_correct = self.checksum == _calc_checksum(self[0:-5])
        request_match = self.request_number == self.request.request_number
        return checksum_correct & request_match

    @property
    def value(self) -> Union[float, int]:
        if self.is_valid:
            if self.value_type is int:
                return int(self.payload, 16)
            if self.value_type is float:
                return struct.unpack("!f", bytes.fromhex(self.payload))[0]
            else:
                print("Invalid response: {}".format(self))
                return float("nan")
        else:
            return float("nan")

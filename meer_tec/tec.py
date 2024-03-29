from typing import Optional, Type

from .interfaces import Interface, Message
from .mecom import FloatOrInt, construct_param_cmd, construct_reset_cmd, verify_response


class TEC:
    def __init__(self, interface: Interface, device_addr: int) -> None:
        self.interface = interface
        self.device_addr = device_addr

    def clear(self) -> None:
        self.interface.clear()

    def get_parameter(
        self,
        param_id: int,
        value_type: Type[FloatOrInt],
        seq_num: Optional[int] = None,
        param_inst: int = 1,
    ) -> FloatOrInt:
        cmd = construct_param_cmd(
            device_addr=self.device_addr,
            cmd="?VR",
            param_id=param_id,
            value_type=value_type,
            param_inst=param_inst,
            value=None,
            seq_num=seq_num,
        )
        request = Message(cmd, value_type)

        reponse = Message(self.interface.query(request), value_type=value_type)
        return reponse.value

    def set_parameter(
        self,
        param_id: int,
        value: FloatOrInt,
        value_type: Type[FloatOrInt],
        seq_num: Optional[int] = None,
        param_inst: int = 1,
    ) -> None:
        cmd = construct_param_cmd(
            device_addr=self.device_addr,
            cmd="VS",
            param_id=param_id,
            value_type=value_type,
            param_inst=param_inst,
            value=value,
            seq_num=seq_num,
        )
        request = Message(cmd, value_type)
        reponse = Message(self.interface.query(request), value_type=value_type)
        if not verify_response(reponse, request):
            raise ValueError("Response does not match request")
        print(reponse)

    def reset(self) -> None:
        cmd = construct_reset_cmd(device_addr=self.device_addr)
        request = Message(cmd, value_type=int)
        reponse = Message(self.interface.query(request), value_type=int)
        if not verify_response(reponse, request):
            raise ValueError("Response does not match request")

    # Common product parameters

    @property
    def device_type(self) -> int:
        """
        Device type.

        1122 → TEC-1122
        """
        return self.get_parameter(100, value_type=int)

    @property
    def hardware_version(self) -> int:
        """
        Hardware Version.

        123 → 1.23
        """
        return self.get_parameter(101, value_type=int)

    @property
    def serial_number(self) -> int:
        """Serial Number."""
        return self.get_parameter(102, value_type=int)

    @property
    def firmware_version(self) -> int:
        """
        Firmware Version.

        123 → 1.23
        """
        return self.get_parameter(103, value_type=int)

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
        return self.get_parameter(104, value_type=int)

    @property
    def error_number(self) -> int:
        """Error number."""
        return self.get_parameter(105, value_type=int)

    @property
    def error_instance(self) -> int:
        """Error param_inst."""
        return self.get_parameter(106, value_type=int)

    @property
    def error_parameter(self) -> int:
        """Error Parameter."""
        return self.get_parameter(107, value_type=int)

    @property
    def save_data_to_flash(self) -> int:
        """
        Save Data to Flash.

        0: Enabled
        1: Disabled (All Parameters can then be used as RAM Parameters)
        """
        return self.get_parameter(108, value_type=int)

    @property
    def parameter_system_flash_status_ro(self) -> int:
        """
        Parameter System: Flash Status (Read only).

        0: All Parameters are saved to Flash
        1: Save to flash pending or in progress. (Please do not power off the
           device now)
        2: Saving to Flash is disabled
        """
        return self.get_parameter(109, value_type=int)

    # Tab: Monitor (Read only)

    @property
    def object_temperature(self) -> float:
        """Object Temperature."""
        return self.get_parameter(1000, value_type=float)

    @property
    def object_temperature_ch1(self) -> float:
        """Object Temperature CH1."""
        return self.get_parameter(1000, value_type=float, param_inst=1)

    @property
    def object_temperature_ch2(self) -> float:
        """Object Temperature CH2."""
        return self.get_parameter(1000, value_type=float, param_inst=2)

    @property
    def sink_temperature(self) -> float:
        """Sink Temperature."""
        return self.get_parameter(1001, value_type=float)

    @property
    def sink_temperature_ch1(self) -> float:
        """Sink Temperature CH1."""
        return self.get_parameter(1001, value_type=float, param_inst=1)

    @property
    def sink_temperature_ch2(self) -> float:
        """Sink Temperature CH2."""
        return self.get_parameter(1001, value_type=float, param_inst=2)

    @property
    def target_object_temperature_ro(self) -> float:
        """Target Object Temperature (read-only)."""
        return self.get_parameter(1010, value_type=float)

    @property
    def nominal_temperature(self) -> float:
        """(Ramp) Nominal Object Temperature."""
        return self.get_parameter(1011, value_type=float)

    @property
    def nominal_temperature_ch1(self) -> float:
        """(Ramp) Nominal Object Temperature CH1."""
        return self.get_parameter(1011, value_type=float, param_inst=1)

    @property
    def nominal_temperature_ch2(self) -> float:
        """(Ramp) Nominal Object Temperature CH2."""
        return self.get_parameter(1011, value_type=float, param_inst=2)

    @property
    def thermal_power_model_current(self) -> float:
        """Thermal Power Model Current."""
        return self.get_parameter(1012, value_type=float)

    @property
    def actual_output_current(self) -> float:
        """Actual Output Current."""
        return self.get_parameter(1020, value_type=float)

    @property
    def actual_output_current_ch1(self) -> float:
        """Actual Output Current CH1."""
        return self.get_parameter(1020, value_type=float, param_inst=1)

    @property
    def actual_output_current_ch2(self) -> float:
        """Actual Output Current CH2."""
        return self.get_parameter(1020, value_type=float, param_inst=2)

    @property
    def actual_output_voltage(self) -> float:
        """Actual Output Voltage."""
        return self.get_parameter(1021, value_type=float)

    @property
    def actual_output_voltage_ch1(self) -> float:
        """Actual Output Voltage CH1."""
        return self.get_parameter(1021, value_type=float, param_inst=1)

    @property
    def actual_output_voltage_ch2(self) -> float:
        """Actual Output Voltage CH2."""
        return self.get_parameter(1021, value_type=float, param_inst=2)

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
        return self.get_parameter(1080, value_type=int)

    # Object Temperature Stability Detection

    @property
    def is_stable(self) -> int:
        """
        Temperature is Stable.

        0: Temperature regulation is not active
        1: Is not stable
        2: Is stable
        """
        return self.get_parameter(1200, value_type=int)

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
        return self.get_parameter(2010, value_type=int)

    @status.setter
    def status(self, value: int) -> None:
        self.set_parameter(2010, value, value_type=int)

    # Tab: Temperature Control

    # CHx Nominal temperature

    @property
    def status_ch1(self) -> int:
        """
        Status CH1.

        0: Static OFF
        1: Static ON
        2: Live OFF/ON (See ID 50000)
        3: HW Enable (Check GPIO Config)
        """
        return self.get_parameter(2010, value_type=int, param_inst=1)

    @status_ch1.setter
    def status_ch1(self, value: int) -> None:
        self.set_parameter(2010, value, value_type=int, param_inst=1)

    @property
    def status_ch2(self) -> int:
        """
        Status CH2.

        0: Static OFF
        1: Static ON
        2: Live OFF/ON (See ID 50000)
        3: HW Enable (Check GPIO Config)
        """
        return self.get_parameter(2010, value_type=int, param_inst=2)

    @status_ch2.setter
    def status_ch2(self, value: int) -> None:
        self.set_parameter(2010, value, value_type=int, param_inst=2)

    @property
    def target_object_temperature(self) -> float:
        """Target Object Temperature."""
        return self.get_parameter(3000, value_type=float)

    @target_object_temperature.setter
    def target_object_temperature(self, value: float) -> None:
        self.set_parameter(3000, value, value_type=float)

    @property
    def coarse_temp_ramp(self) -> float:
        """Coarse Temp Ramp."""
        return self.get_parameter(3003, value_type=float)

    @coarse_temp_ramp.setter
    def coarse_temp_ramp(self, value: float) -> None:
        self.set_parameter(3003, value, value_type=float)

    @property
    def coarse_temp_ramp_ch1(self) -> float:
        """Coarse Temp Ramp CH1."""
        return self.get_parameter(3003, value_type=float, param_inst=1)

    @coarse_temp_ramp_ch1.setter
    def coarse_temp_ramp_ch1(self, value: float) -> None:
        self.set_parameter(3003, value, value_type=float, param_inst=1)

    @property
    def coarse_temp_ramp_ch2(self) -> float:
        """Coarse Temp Ramp CH2."""
        return self.get_parameter(3003, value_type=float, param_inst=2)

    @coarse_temp_ramp_ch2.setter
    def coarse_temp_ramp_ch2(self, value: float) -> None:
        self.set_parameter(3003, value, value_type=float, param_inst=2)

    @property
    def proximity_width(self) -> float:
        """Proximity Width."""
        return self.get_parameter(3002, value_type=float)

    @proximity_width.setter
    def proximity_width(self, value: float) -> None:
        self.set_parameter(3002, value, value_type=float)

    @property
    def proximity_width_ch1(self) -> float:
        """Proximity Width CH1."""
        return self.get_parameter(3002, value_type=float, param_inst=1)

    @proximity_width_ch1.setter
    def proximity_width_ch1(self, value: float) -> None:
        self.set_parameter(3002, value, value_type=float, param_inst=1)

    @property
    def proximity_width_ch2(self) -> float:
        """Proximity Width CH2."""
        return self.get_parameter(3002, value_type=float, param_inst=2)

    @proximity_width_ch2.setter
    def proximity_width_ch2(self, value: float) -> None:
        self.set_parameter(3002, value, value_type=float, param_inst=2)

    # CHx Temperature Controller PID Values

    @property
    def kp(self) -> float:
        """Kp."""
        return self.get_parameter(3010, value_type=float)

    @kp.setter
    def kp(self, value: float) -> None:
        self.set_parameter(3010, value, value_type=float)

    @property
    def kp_ch1(self) -> float:
        """Kp CH1."""
        return self.get_parameter(3010, value_type=float, param_inst=1)

    @kp_ch1.setter
    def kp_ch1(self, value: float) -> None:
        self.set_parameter(3010, value, value_type=float, param_inst=1)

    @property
    def kp_ch2(self) -> float:
        """Kp CH2."""
        return self.get_parameter(3010, value_type=float, param_inst=2)

    @kp_ch2.setter
    def kp_ch2(self, value: float) -> None:
        self.set_parameter(3010, value, value_type=float, param_inst=2)

    @property
    def ti(self) -> float:
        """Ti."""
        return self.get_parameter(3011, value_type=float)

    @ti.setter
    def ti(self, value: float) -> None:
        self.set_parameter(3011, value, value_type=float)

    @property
    def ti_ch1(self) -> float:
        """Ti CH1."""
        return self.get_parameter(3011, value_type=float, param_inst=1)

    @ti_ch1.setter
    def ti_ch1(self, value: float) -> None:
        self.set_parameter(3011, value, value_type=float, param_inst=1)

    @property
    def td(self) -> float:
        """Td."""
        return self.get_parameter(3012, value_type=float)

    @td.setter
    def td(self, value: float) -> None:
        self.set_parameter(3012, value, value_type=float)

    @property
    def td_ch1(self) -> float:
        """Td CH1."""
        return self.get_parameter(3012, value_type=float, param_inst=1)

    @td_ch1.setter
    def td_ch1(self, value: float) -> None:
        self.set_parameter(3012, value, value_type=float, param_inst=1)

    @property
    def d_part_damping_pt1(self) -> float:
        """D Part Damping PT1."""
        return self.get_parameter(3013, value_type=float)

    @d_part_damping_pt1.setter
    def d_part_damping_pt1(self, value: float) -> None:
        self.set_parameter(3013, value, value_type=float)

    @property
    def d_part_damping_pt1_ch1(self) -> float:
        """D Part Damping PT1 CH1."""
        return self.get_parameter(3013, value_type=float, param_inst=1)

    @d_part_damping_pt1_ch1.setter
    def d_part_damping_pt1_ch1(self, value: float) -> None:
        self.set_parameter(3013, value, value_type=float, param_inst=1)

    @property
    def d_part_damping_pt1_ch2(self) -> float:
        """D Part Damping PT1 CH2."""
        return self.get_parameter(3013, value_type=float, param_inst=2)

    @d_part_damping_pt1_ch2.setter
    def d_part_damping_pt1_ch2(self, value: float) -> None:
        self.set_parameter(3013, value, value_type=float, param_inst=2)

    # CHx Modelization for Thermal Power Regulation

    @property
    def mode(self) -> int:
        """
        Mode.

        0: Peltier, Full Control
        1: Peltier, Heat Only - Cool Only
        2: Resistor, Heat Only
        """
        return self.get_parameter(3020, value_type=int)

    @mode.setter
    def mode(self, value: int) -> None:
        self.set_parameter(3020, value, value_type=int)

    @property
    def mode_ch1(self) -> int:
        """
        Mode CH1.

        0: Peltier, Full Control
        1: Peltier, Heat Only - Cool Only
        2: Resistor, Heat Only
        """
        return self.get_parameter(3020, value_type=int, param_inst=1)

    @mode_ch1.setter
    def mode_ch1(self, value: int) -> None:
        self.set_parameter(3020, value, value_type=int, param_inst=1)

    @property
    def mode_ch2(self) -> int:
        """
        Mode CH2.

        0: Peltier, Full Control
        1: Peltier, Heat Only - Cool Only
        2: Resistor, Heat Only
        """
        return self.get_parameter(3020, value_type=int, param_inst=2)

    @mode_ch2.setter
    def mode_ch2(self, value: int) -> None:
        self.set_parameter(3020, value, value_type=int, param_inst=2)

    # CHx Peltier Characteristics

    @property
    def maximal_current_imax(self) -> float:
        """Maximal Current Imax."""
        return self.get_parameter(3030, value_type=float)

    @maximal_current_imax.setter
    def maximal_current_imax(self, value: float) -> None:
        self.set_parameter(3030, value, value_type=float)

    @property
    def maximal_current_imax_ch1(self) -> float:
        """Maximal Current Imax CH1."""
        return self.get_parameter(3030, value_type=float, param_inst=1)

    @maximal_current_imax_ch1.setter
    def maximal_current_imax_ch1(self, value: float) -> None:
        self.set_parameter(3030, value, value_type=float, param_inst=1)

    @property
    def maximal_current_imax_ch2(self) -> float:
        """Maximal Current Imax CH2."""
        return self.get_parameter(3030, value_type=float, param_inst=2)

    @maximal_current_imax_ch2.setter
    def maximal_current_imax_ch2(self, value: float) -> None:
        self.set_parameter(3030, value, value_type=float, param_inst=2)

    @property
    def delta_temperature_dtmax(self) -> float:
        """Delta Temperature dTmax."""
        return self.get_parameter(3033, value_type=float)

    @delta_temperature_dtmax.setter
    def delta_temperature_dtmax(self, value: float) -> None:
        self.set_parameter(3033, value, value_type=float)

    @property
    def delta_temperature_dtmax_ch1(self) -> float:
        """Delta Temperature dTmax CH1."""
        return self.get_parameter(3033, value_type=float, param_inst=1)

    @delta_temperature_dtmax_ch1.setter
    def delta_temperature_dtmax_ch1(self, value: float) -> None:
        self.set_parameter(3033, value, value_type=float, param_inst=1)

    @property
    def delta_temperature_dtmax_ch2(self) -> float:
        """Delta Temperature dTmax CH2."""
        return self.get_parameter(3033, value_type=float, param_inst=2)

    @delta_temperature_dtmax_ch2.setter
    def delta_temperature_dtmax_ch2(self, value: float) -> None:
        self.set_parameter(3033, value, value_type=float, param_inst=2)

    @property
    def positive_current_is(self) -> int:
        """
        Positive Current is.

        0: Cooling
        1: Heating
        """
        return self.get_parameter(3034, value_type=int)

    @positive_current_is.setter
    def positive_current_is(self, value: int) -> None:
        self.set_parameter(3034, value, value_type=int)

    @property
    def positive_current_is_ch1(self) -> int:
        """
        Positive Current is CH1.

        0: Cooling
        1: Heating
        """
        return self.get_parameter(3034, value_type=int, param_inst=1)

    @positive_current_is_ch1.setter
    def positive_current_is_ch1(self, value: int) -> None:
        self.set_parameter(3034, value, value_type=int, param_inst=1)

    @property
    def positive_current_is_ch2(self) -> int:
        """
        Positive Current is CH2.

        0: Cooling
        1: Heating
        """
        return self.get_parameter(3034, value_type=int, param_inst=2)

    @positive_current_is_ch2.setter
    def positive_current_is_ch2(self, value: int) -> None:
        self.set_parameter(3034, value, value_type=int, param_inst=2)

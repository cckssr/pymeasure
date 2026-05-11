from pymeasure.instruments import Instrument, SCPIMixin


class ThorlabsPM400(SCPIMixin, Instrument):
    # IEEE 488.2
    self_test: bool

    # SYSTem
    beeper_state: bool
    error: list
    scpi_version: float
    date: list  # getter: [year, month, day]; setter: 'year,month,day' string
    time: list  # getter: [hour, min, sec]; setter: 'hour,min,sec' string
    line_frequency: float
    sensor_info: list

    # STATus — MEASurement
    status_measurement_event: int
    status_measurement_condition: int
    status_measurement_positive_transition: int
    status_measurement_negative_transition: int
    status_measurement_enable: int

    # STATus — AUXiliary
    status_auxiliary_event: int
    status_auxiliary_condition: int
    status_auxiliary_positive_transition: int
    status_auxiliary_negative_transition: int
    status_auxiliary_enable: int

    # STATus — OPERation
    status_operation_event: int
    status_operation_condition: int
    status_operation_positive_transition: int
    status_operation_negative_transition: int
    status_operation_enable: int

    # STATus — QUEStionable
    status_questionable_event: int
    status_questionable_condition: int
    status_questionable_positive_transition: int
    status_questionable_negative_transition: int
    status_questionable_enable: int

    # DISPlay
    display_brightness: float
    display_contrast: float

    # CALibration
    calibration_string: str

    # SENSe — averaging / correction
    averaging_count: int
    attenuation: float
    zero_state: int
    zero_magnitude: float
    beam_diameter: float
    wavelength: float
    photodiode_response: float
    thermopile_response: float
    pyro_response: float

    # SENSe — current
    current_autorange: bool
    current_range: float
    current_reference: float
    current_delta_mode: bool

    # SENSe — energy
    energy_range: float
    energy_reference: float
    energy_delta_mode: bool

    # SENSe — frequency (read-only)
    frequency_range_upper: float
    frequency_range_lower: float

    # SENSe — power
    power_autorange: bool
    power_range: float
    power_reference: float
    power_delta_mode: bool
    power_unit: str

    # SENSe — voltage
    voltage_autorange: bool
    voltage_range: float
    voltage_reference: float
    voltage_delta_mode: bool

    # SENSe — peak
    peak_threshold: float

    # INPut
    photodiode_filter: bool
    thermopile_accelerator: bool
    thermopile_accelerator_auto: bool
    thermopile_tau: float
    adapter_type: str

    # Measurement
    configure: str
    power: float
    current: float
    voltage: float
    energy: float
    frequency: float
    power_density: float
    energy_density: float
    resistance: float
    temperature: float
    fetch: float
    read_measurement: float

    def __init__(self, adapter: str, name: str = ..., **kwargs) -> None: ...
    def beep(self) -> None: ...
    def status_preset(self) -> None: ...
    def zero(self) -> None: ...
    def abort_zero(self) -> None: ...
    def initiate(self) -> None: ...
    def abort(self) -> None: ...

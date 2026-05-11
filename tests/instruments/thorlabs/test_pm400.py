#
# This file is part of the PyMeasure package.
#
# Copyright (c) 2013-2026 PyMeasure Developers
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

from pymeasure.test import expected_protocol
from pymeasure.instruments.thorlabs.pm400 import ThorlabsPM400


def test_self_test_passes():
    with expected_protocol(ThorlabsPM400, [("*TST?", "0")]) as inst:
        assert inst.self_test is True


def test_self_test_fails():
    with expected_protocol(ThorlabsPM400, [("*TST?", "1")]) as inst:
        assert inst.self_test is False


def test_beeper_state_get_true():
    with expected_protocol(ThorlabsPM400, [("SYST:BEEP:STAT?", "1")]) as inst:
        assert inst.beeper_state is True


def test_beeper_state_get_false():
    with expected_protocol(ThorlabsPM400, [("SYST:BEEP:STAT?", "0")]) as inst:
        assert inst.beeper_state is False


def test_beeper_state_set_true():
    with expected_protocol(ThorlabsPM400, [("SYST:BEEP:STAT 1", None)]) as inst:
        inst.beeper_state = True


def test_beeper_state_set_false():
    with expected_protocol(ThorlabsPM400, [("SYST:BEEP:STAT 0", None)]) as inst:
        inst.beeper_state = False


def test_error_no_error():
    with expected_protocol(ThorlabsPM400, [("SYST:ERR?", '0,"No error"')]) as inst:
        err = inst.error
        assert err[0] == 0


def test_scpi_version():
    with expected_protocol(ThorlabsPM400, [("SYST:VERS?", "1999.0")]) as inst:
        assert inst.scpi_version == 1999.0


def test_date_get():
    with expected_protocol(ThorlabsPM400, [("SYST:DATE?", "2026,1,15")]) as inst:
        assert inst.date == [2026.0, 1.0, 15.0]


def test_date_set():
    with expected_protocol(ThorlabsPM400, [("SYST:DATE 2026,1,15", None)]) as inst:
        inst.date = "2026,1,15"


def test_time_get():
    with expected_protocol(ThorlabsPM400, [("SYST:TIME?", "12,30,0")]) as inst:
        assert inst.time == [12.0, 30.0, 0.0]


def test_time_set():
    with expected_protocol(ThorlabsPM400, [("SYST:TIME 12,30,0", None)]) as inst:
        inst.time = "12,30,0"


def test_sensor_info():
    response = '"S120C","P0006006","cal","1","1","17"'
    with expected_protocol(ThorlabsPM400, [("SYST:SENS:IDN?", response)]) as inst:
        info = inst.sensor_info
        assert isinstance(info, list)
        assert len(info) == 6


def test_calibration_string():
    with expected_protocol(ThorlabsPM400, [("CAL:STR?", '"Factory 2024-01-01"')]) as inst:
        assert isinstance(inst.calibration_string, str)


def test_averaging_count_get():
    with expected_protocol(ThorlabsPM400, [("SENS:AVER:COUN?", "100")]) as inst:
        assert inst.averaging_count == 100


def test_averaging_count_set():
    with expected_protocol(ThorlabsPM400, [("SENS:AVER:COUN 10", None)]) as inst:
        inst.averaging_count = 10


def test_averaging_count_truncation():
    with expected_protocol(ThorlabsPM400, [("SENS:AVER:COUN 1", None)]) as inst:
        inst.averaging_count = 0  # truncated to 1


def test_wavelength_get():
    with expected_protocol(ThorlabsPM400, [("SENS:CORR:WAV?", "1064.0")]) as inst:
        assert inst.wavelength == 1064.0


def test_wavelength_set():
    with expected_protocol(ThorlabsPM400, [("SENS:CORR:WAV 532", None)]) as inst:
        inst.wavelength = 532


def test_attenuation_get():
    with expected_protocol(ThorlabsPM400, [("SENS:CORR:LOSS:INP:MAGN?", "0.0")]) as inst:
        assert inst.attenuation == 0.0


def test_attenuation_set():
    with expected_protocol(ThorlabsPM400, [("SENS:CORR:LOSS:INP:MAGN 3", None)]) as inst:
        inst.attenuation = 3.0


def test_beam_diameter_get():
    with expected_protocol(ThorlabsPM400, [("SENS:CORR:BEAM?", "3.0")]) as inst:
        assert inst.beam_diameter == 3.0


def test_beam_diameter_set():
    with expected_protocol(ThorlabsPM400, [("SENS:CORR:BEAM 5", None)]) as inst:
        inst.beam_diameter = 5.0


def test_zero_state():
    with expected_protocol(ThorlabsPM400, [("SENS:CORR:COLL:ZERO:STAT?", "0")]) as inst:
        assert inst.zero_state == 0


def test_zero_magnitude():
    with expected_protocol(ThorlabsPM400, [("SENS:CORR:COLL:ZERO:MAGN?", "1.5e-9")]) as inst:
        assert isinstance(inst.zero_magnitude, float)


def test_power_autorange_get_true():
    with expected_protocol(ThorlabsPM400, [("SENS:POW:RANG:AUTO?", "1")]) as inst:
        assert inst.power_autorange is True


def test_power_autorange_get_false():
    with expected_protocol(ThorlabsPM400, [("SENS:POW:RANG:AUTO?", "0")]) as inst:
        assert inst.power_autorange is False


def test_power_autorange_set():
    with expected_protocol(ThorlabsPM400, [("SENS:POW:RANG:AUTO 1", None)]) as inst:
        inst.power_autorange = True


def test_power_range_get():
    with expected_protocol(ThorlabsPM400, [("SENS:POW:RANG:UPP?", "2e-3")]) as inst:
        assert inst.power_range == 2e-3


def test_power_range_set():
    with expected_protocol(ThorlabsPM400, [("SENS:POW:RANG:UPP 0.01", None)]) as inst:
        inst.power_range = 0.01


def test_power_reference_get():
    with expected_protocol(ThorlabsPM400, [("SENS:POW:REF?", "1e-3")]) as inst:
        assert inst.power_reference == 1e-3


def test_power_reference_set():
    with expected_protocol(ThorlabsPM400, [("SENS:POW:REF 0.001", None)]) as inst:
        inst.power_reference = 0.001


def test_power_unit_get_watts():
    with expected_protocol(ThorlabsPM400, [("SENS:POW:UNIT?", "W")]) as inst:
        assert inst.power_unit == "W"


def test_power_unit_get_dbm():
    with expected_protocol(ThorlabsPM400, [("SENS:POW:UNIT?", "DBM")]) as inst:
        assert inst.power_unit == "DBM"


def test_power_unit_set():
    with expected_protocol(ThorlabsPM400, [("SENS:POW:UNIT DBM", None)]) as inst:
        inst.power_unit = "DBM"


def test_display_brightness_get():
    with expected_protocol(ThorlabsPM400, [("DISP:BRIG?", "0.5")]) as inst:
        assert inst.display_brightness == 0.5


def test_display_brightness_set():
    with expected_protocol(ThorlabsPM400, [("DISP:BRIG 0.8", None)]) as inst:
        inst.display_brightness = 0.8


def test_photodiode_filter_set_true():
    with expected_protocol(ThorlabsPM400, [("INP:PDI:FILT:LPAS:STAT 1", None)]) as inst:
        inst.photodiode_filter = True


def test_photodiode_filter_set_false():
    with expected_protocol(ThorlabsPM400, [("INP:PDI:FILT:LPAS:STAT 0", None)]) as inst:
        inst.photodiode_filter = False


def test_thermopile_tau_get():
    with expected_protocol(ThorlabsPM400, [("INP:THER:ACC:TAU?", "5.0")]) as inst:
        assert inst.thermopile_tau == 5.0


def test_thermopile_tau_set():
    with expected_protocol(ThorlabsPM400, [("INP:THER:ACC:TAU 10", None)]) as inst:
        inst.thermopile_tau = 10.0


def test_adapter_type_get():
    with expected_protocol(ThorlabsPM400, [("INP:ADP:TYPE?", "THER")]) as inst:
        assert inst.adapter_type == "THER"


def test_adapter_type_set():
    with expected_protocol(ThorlabsPM400, [("INP:ADP:TYPE PHOT", None)]) as inst:
        inst.adapter_type = "PHOT"


def test_configure_get():
    with expected_protocol(ThorlabsPM400, [("CONF?", "POW")]) as inst:
        assert inst.configure == "POW"


def test_configure_set():
    with expected_protocol(ThorlabsPM400, [("CONF:FREQ", None)]) as inst:
        inst.configure = "FREQ"


def test_power_measurement():
    with expected_protocol(ThorlabsPM400, [("MEAS:POW?", "1.234e-3")]) as inst:
        assert inst.power == 1.234e-3


def test_current_measurement():
    with expected_protocol(ThorlabsPM400, [("MEAS:CURR?", "5.0e-6")]) as inst:
        assert inst.current == 5.0e-6


def test_voltage_measurement():
    with expected_protocol(ThorlabsPM400, [("MEAS:VOLT?", "3.14")]) as inst:
        assert inst.voltage == 3.14


def test_energy_measurement():
    with expected_protocol(ThorlabsPM400, [("MEAS:ENER?", "2.5e-9")]) as inst:
        assert inst.energy == 2.5e-9


def test_frequency_measurement():
    with expected_protocol(ThorlabsPM400, [("MEAS:FREQ?", "1000.0")]) as inst:
        assert inst.frequency == 1000.0


def test_temperature_measurement():
    with expected_protocol(ThorlabsPM400, [("MEAS:TEMP?", "25.3")]) as inst:
        assert inst.temperature == 25.3


def test_fetch():
    with expected_protocol(ThorlabsPM400, [("FETC?", "0.00123")]) as inst:
        assert inst.fetch == 0.00123


def test_read_measurement():
    with expected_protocol(ThorlabsPM400, [("READ?", "0.00456")]) as inst:
        assert inst.read_measurement == 0.00456


def test_beep():
    with expected_protocol(ThorlabsPM400, [("SYST:BEEP:IMM", None)]) as inst:
        inst.beep()


def test_status_preset():
    with expected_protocol(ThorlabsPM400, [("STAT:PRES", None)]) as inst:
        inst.status_preset()


def test_zero():
    with expected_protocol(ThorlabsPM400, [("SENS:CORR:COLL:ZERO:INIT", None)]) as inst:
        inst.zero()


def test_abort_zero():
    with expected_protocol(ThorlabsPM400, [("SENS:CORR:COLL:ZERO:ABOR", None)]) as inst:
        inst.abort_zero()


def test_initiate():
    with expected_protocol(ThorlabsPM400, [("INIT", None)]) as inst:
        inst.initiate()


def test_abort():
    with expected_protocol(ThorlabsPM400, [("ABOR", None)]) as inst:
        inst.abort()


def test_peak_threshold_get():
    with expected_protocol(ThorlabsPM400, [("SENS:PEAK:THR?", "50.0")]) as inst:
        assert inst.peak_threshold == 50.0


def test_peak_threshold_set():
    with expected_protocol(ThorlabsPM400, [("SENS:PEAK:THR 75", None)]) as inst:
        inst.peak_threshold = 75.0


def test_frequency_range_upper():
    with expected_protocol(ThorlabsPM400, [("SENS:FREQ:RANG:UPP?", "1000.0")]) as inst:
        assert inst.frequency_range_upper == 1000.0


def test_frequency_range_lower():
    with expected_protocol(ThorlabsPM400, [("SENS:FREQ:RANG:LOW?", "0.1")]) as inst:
        assert inst.frequency_range_lower == 0.1


def test_current_autorange_set():
    with expected_protocol(ThorlabsPM400, [("SENS:CURR:RANG:AUTO 1", None)]) as inst:
        inst.current_autorange = True


def test_energy_delta_mode_set():
    with expected_protocol(ThorlabsPM400, [("SENS:ENER:STAT 0", None)]) as inst:
        inst.energy_delta_mode = False


def test_thermopile_accelerator_set():
    with expected_protocol(ThorlabsPM400, [("INP:THER:ACC:STAT 1", None)]) as inst:
        inst.thermopile_accelerator = True


def test_thermopile_accelerator_auto_set():
    with expected_protocol(ThorlabsPM400, [("INP:THER:ACC:AUTO 0", None)]) as inst:
        inst.thermopile_accelerator_auto = False

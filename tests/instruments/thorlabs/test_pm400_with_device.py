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

"""Hardware tests for ThorlabsPM400.

Run against the physical instrument with:
    pytest tests/instruments/thorlabs/test_pm400_with_device.py \
        --device-address "USB0::0x1313::0x8075::P5006006::0::INSTR" -v

Tested with: Thorlabs PM400 + S120C thermal power sensor.

Notes on skipped tests:
- SYST:LFREQ? is not answered by the PM400 (no response / timeout).
- STAT:MEAS/AUX/OPER/QUES queries are not implemented in PM400 firmware.
- DISP:CONT? and INP:ADP:TYPE? cause timeouts on this firmware.
- SENS:POW:STAT? (power delta mode query) is not supported on this unit.
- INP:PDI:FILT:LPAS:STAT? requires a photodiode sensor (S120C is thermal).
"""

import math
import pytest

from pymeasure.instruments.thorlabs.pm400 import ThorlabsPM400


@pytest.fixture(scope="module")
def pm(connected_device_address):
    instr = ThorlabsPM400(connected_device_address)
    instr.clear()  # clear any accumulated errors from prior runs
    yield instr
    # Restore safe defaults on teardown
    instr.power_autorange = True
    instr.wavelength = 532
    instr.averaging_count = 1


class TestIdentification:
    def test_id_is_string(self, pm):
        assert isinstance(pm.id, str)
        assert len(pm.id) > 0

    def test_id_contains_thorlabs(self, pm):
        assert "THORLABS" in pm.id.upper()

    def test_self_test_passes(self, pm):
        assert pm.self_test is True


class TestSystem:
    def test_scpi_version(self, pm):
        # Returns a float such as 1999.0
        assert pm.scpi_version >= 1999.0

    def test_error_queue_empty(self, pm):
        pm.clear()  # flush any prior errors
        err = pm.error
        # values() splits comma-separated response → [code, "message"]
        code = err[0] if isinstance(err, list) else float(err)
        assert code == 0

    def test_sensor_info(self, pm):
        # SYST:SENS:IDN? returns comma-separated: name, sn, cal_msg, type, subtype, flags
        info = pm.sensor_info
        assert isinstance(info, list)
        assert len(info) >= 1

    def test_sensor_name_is_string(self, pm):
        info = pm.sensor_info
        # Sensor name is the first field, returned as quoted string e.g. '"S120C"'
        assert isinstance(info[0], str)

    def test_date_roundtrip(self, pm):
        original = pm.date
        pm.date = original
        assert pm.date == original

    def test_time_roundtrip(self, pm):
        original = pm.time
        pm.time = original
        assert pm.time == original

    @pytest.mark.skip(reason="SYST:LFREQ? causes timeout on PM400 (no response from firmware)")
    def test_line_frequency(self, pm):
        freq = pm.line_frequency
        assert freq in (50.0, 60.0)

    def test_beeper_state_roundtrip(self, pm):
        original = pm.beeper_state
        pm.beeper_state = False
        assert pm.beeper_state is False
        pm.beeper_state = True
        assert pm.beeper_state is True
        pm.beeper_state = original

    def test_beep_method(self, pm):
        pm.beep()  # must not raise


class TestCalibration:
    def test_calibration_string(self, pm):
        cal = pm.calibration_string
        assert isinstance(cal, str)
        assert len(cal) > 0


class TestSenseAveraging:
    def test_averaging_count_roundtrip(self, pm):
        original = pm.averaging_count
        pm.averaging_count = 10
        assert pm.averaging_count == 10
        pm.averaging_count = 1
        assert pm.averaging_count == 1
        pm.averaging_count = original

    def test_averaging_count_min(self, pm):
        pm.averaging_count = 1
        assert pm.averaging_count >= 1

    def test_averaging_count_is_int(self, pm):
        assert isinstance(pm.averaging_count, int)


class TestSenseCorrection:
    def test_wavelength_roundtrip(self, pm):
        original = pm.wavelength
        pm.wavelength = 1064
        assert abs(pm.wavelength - 1064) < 1
        pm.wavelength = original

    def test_wavelength_is_float(self, pm):
        assert isinstance(pm.wavelength, float)

    def test_beam_diameter_roundtrip(self, pm):
        original = pm.beam_diameter
        pm.beam_diameter = 3.0
        assert abs(pm.beam_diameter - 3.0) < 0.01
        pm.beam_diameter = original

    def test_attenuation_roundtrip(self, pm):
        original = pm.attenuation
        pm.attenuation = 0.0
        assert abs(pm.attenuation - 0.0) < 0.01
        pm.attenuation = original

    def test_zero_state_is_int(self, pm):
        assert isinstance(pm.zero_state, int)

    def test_zero_magnitude_is_float(self, pm):
        assert isinstance(pm.zero_magnitude, float)


class TestPowerRanging:
    def test_power_autorange_roundtrip(self, pm):
        original = pm.power_autorange
        pm.power_autorange = True
        assert pm.power_autorange is True
        pm.power_autorange = original

    def test_power_range_is_float(self, pm):
        pm.power_autorange = False
        assert isinstance(pm.power_range, float)
        pm.power_autorange = True

    def test_power_unit_roundtrip(self, pm):
        original = pm.power_unit
        pm.power_unit = "W"
        assert pm.power_unit == "W"
        pm.power_unit = "DBM"
        assert pm.power_unit == "DBM"
        pm.power_unit = original

    @pytest.mark.skip(reason="SENS:POW:STAT? causes timeout on PM400 (no response from firmware)")
    def test_power_delta_mode_roundtrip(self, pm):
        original = pm.power_delta_mode
        pm.power_delta_mode = False
        assert pm.power_delta_mode is False
        pm.power_delta_mode = original

    def test_power_reference_roundtrip(self, pm):
        original = pm.power_reference
        pm.power_reference = 0.001
        assert isinstance(pm.power_reference, float)
        pm.power_reference = original


class TestDisplay:
    def test_display_brightness_roundtrip(self, pm):
        original = pm.display_brightness
        pm.display_brightness = original
        assert isinstance(pm.display_brightness, float)

    @pytest.mark.skip(reason="DISP:CONT? causes timeout on PM400 (not implemented in firmware)")
    def test_display_contrast_roundtrip(self, pm):
        original = pm.display_contrast
        pm.display_contrast = original
        assert isinstance(pm.display_contrast, float)


class TestInputSubsystem:
    @pytest.mark.skip(
        reason="INP:PDI:FILT:LPAS:STAT? requires a photodiode sensor; S120C is thermal"
    )
    def test_photodiode_filter_roundtrip(self, pm):
        original = pm.photodiode_filter
        pm.photodiode_filter = False
        assert pm.photodiode_filter is False
        pm.photodiode_filter = True
        assert pm.photodiode_filter is True
        pm.photodiode_filter = original

    @pytest.mark.skip(reason="INP:ADP:TYPE? causes timeout on PM400 (not implemented in firmware)")
    def test_adapter_type_roundtrip(self, pm):
        original = pm.adapter_type
        pm.adapter_type = original
        assert pm.adapter_type in ["PHOT", "THER", "PYRO"]


class TestMeasurement:
    def test_configure_power(self, pm):
        pm.configure = "POW"
        assert "POW" in pm.configure.upper()

    def test_configure_roundtrip(self, pm):
        for mode in ["POW", "FREQ"]:
            pm.configure = mode
            assert mode in pm.configure.upper()
        pm.configure = "POW"

    def test_power_is_float(self, pm):
        pm.configure = "POW"
        assert isinstance(pm.power, float)

    def test_power_is_finite(self, pm):
        pm.configure = "POW"
        assert math.isfinite(pm.power)

    def test_fetch_is_float(self, pm):
        pm.configure = "POW"
        _ = pm.power  # trigger a measurement first
        assert isinstance(pm.fetch, float)

    def test_read_measurement_is_float(self, pm):
        pm.configure = "POW"
        assert isinstance(pm.read_measurement, float)

    def test_frequency_is_float(self, pm):
        pm.configure = "FREQ"
        assert isinstance(pm.frequency, float)

    def test_temperature_is_float(self, pm):
        pm.configure = "TEMP"
        assert isinstance(pm.temperature, float)

    def test_initiate_abort(self, pm):
        pm.initiate()
        pm.abort()  # must not raise


@pytest.mark.skip(reason="STAT:MEAS/AUX/OPER/QUES queries are not implemented in PM400 firmware")
class TestStatusRegisters:
    def test_measurement_event_is_int(self, pm):
        assert isinstance(pm.status_measurement_event, int)

    def test_measurement_condition_is_int(self, pm):
        assert isinstance(pm.status_measurement_condition, int)

    def test_operation_event_is_int(self, pm):
        assert isinstance(pm.status_operation_event, int)

    def test_operation_condition_is_int(self, pm):
        assert isinstance(pm.status_operation_condition, int)

    def test_questionable_event_is_int(self, pm):
        assert isinstance(pm.status_questionable_event, int)

    def test_measurement_enable_roundtrip(self, pm):
        original = pm.status_measurement_enable
        pm.status_measurement_enable = 0
        assert pm.status_measurement_enable == 0
        pm.status_measurement_enable = original

    def test_status_preset(self, pm):
        pm.status_preset()  # must not raise

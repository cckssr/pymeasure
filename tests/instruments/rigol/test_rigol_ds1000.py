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

# Real-device test file for the Rigol DS1000Z series oscilloscope.
# Connects to a physical device and exercises all properties/methods.
#
# Usage:
#   pytest tests/instruments/rigol/test_rigol_ds1000.py \
#       --device-address "USB0::0x1AB1::0x04CE::DS1ZA123456::INSTR"
#
# Notes:
#   - Connect the probe compensation output to channel 1 for waveform tests
#     (1 kHz square wave, ~3 V).
#   - MSO-specific tests are marked with @pytest.mark.mso_only.
#     Skip them on DS-only models: pytest -m 'not mso_only'
#   - Optional hardware tests (waveform record, source generator) are marked
#     with @pytest.mark.optional. Skip them: pytest -m 'not optional'

from time import sleep

import pytest

from pymeasure.generator import Generator
from pymeasure.instruments.rigol.rigol_ds1000 import RigolDS1000ZSeries


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def generator():
    return Generator()


@pytest.fixture(scope="module")
def rigol_ds1000(connected_device_address, generator) -> RigolDS1000ZSeries:
    instr = generator.instantiate(
        RigolDS1000ZSeries,
        connected_device_address,
        "Rigol DS1000Z Series",
        adapter_kwargs={},
    )
    return instr


# ---------------------------------------------------------------------------
# Common test functions
# ---------------------------------------------------------------------------


def _ensure_channel_enabled(device, channel_nr):
    getattr(device, "ch" + str(channel_nr)).is_enabled = True  # Ensure source channel is enabled


# ---------------------------------------------------------------------------
# Basic operations
# ---------------------------------------------------------------------------


def test_id(rigol_ds1000):
    assert rigol_ds1000.id is not None


def test_autoscale(rigol_ds1000):
    rigol_ds1000.autoscale()
    sleep(5)  # Wait for autoscale to complete


def test_stop(rigol_ds1000):
    rigol_ds1000.stop()
    sleep(0.5)


def test_run(rigol_ds1000):
    rigol_ds1000.run()
    sleep(0.5)


def test_force_trigger(rigol_ds1000):
    rigol_ds1000.force_trigger()
    sleep(0.5)


# ---------------------------------------------------------------------------
# Acquire Subsystem
# ---------------------------------------------------------------------------
class TestAcquireSubsystem:
    """Test every command and property in the Acquire subsystem."""

    @pytest.mark.parametrize(
        "mode_key, mode_value",
        {"NORMAL": "NORM", "AVERAGES": "AVER", "PEAK": "PEAK", "HRESOLUTION": "HRES"}.items(),
    )
    def test_mode(self, rigol_ds1000, mode_key, mode_value):
        rigol_ds1000.acq_mode = mode_key
        assert rigol_ds1000.acq_mode == mode_value

    @pytest.mark.parametrize("averages", [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024])
    def test_averages(self, rigol_ds1000, averages):
        rigol_ds1000.acq_mode = "AVERAGES"  # Must be in AVERAGES mode to set this property
        rigol_ds1000.acq_averages = averages
        assert rigol_ds1000.acq_averages == averages

    def test_sample_rate(self, rigol_ds1000):
        rate = rigol_ds1000.acq_sample_rate
        assert isinstance(rate, (int, float))

    # TODO: Fix the memory depth tests - the device seems to reject some valid values, and the error handling is not working correctly (see check_device_errors fixture)
    @pytest.mark.parametrize(
        "mdepth",
        [
            "AUTO",
            3_000,
            6_000,
            12_000,
            30_000,
            60_000,
            120_000,
            300_000,
            600_000,
            1_200_000,
            3_000_000,
            6_000_000,
            12_000_000,
            24_000_000,
        ],
    )
    def fix_test_memory_depth(self, rigol_ds1000, mdepth):
        rigol_ds1000.acq_memory_depth = mdepth
        assert rigol_ds1000.acq_memory_depth == mdepth


# ---------------------------------------------------------------------------
# Channel Subsystem
# ---------------------------------------------------------------------------
class TestChannelSubsystem:
    """Test every command and property in the Channel subsystem.

    All channels are tested with their respective ch1/ch2/ch3/ch4 accessors.
    A known good scale (1 V/div) and DC coupling are set before offset tests
    to ensure the ±20 V range is valid.
    """

    @pytest.mark.parametrize("channel_attr", ["ch1", "ch2", "ch3", "ch4"])
    def test_channel_enable_disable(self, rigol_ds1000, channel_attr):
        ch = getattr(rigol_ds1000, channel_attr)
        ch.is_enabled = True
        assert ch.is_enabled is True
        ch.is_enabled = False
        assert ch.is_enabled is False
        ch.is_enabled = True  # Leave enabled for subsequent tests

    @pytest.mark.parametrize("bandwidth", ["OFF", "20M"])
    def test_ch1_bandwidth(self, rigol_ds1000, bandwidth):
        rigol_ds1000.ch1.is_enabled = True
        rigol_ds1000.ch1.bandwidth = bandwidth
        assert rigol_ds1000.ch1.bandwidth == bandwidth

    @pytest.mark.parametrize("coupling", ["AC", "DC", "GND"])
    def test_ch1_coupling(self, rigol_ds1000, coupling):
        rigol_ds1000.ch1.is_enabled = True
        rigol_ds1000.ch1.coupling = coupling
        assert rigol_ds1000.ch1.coupling == coupling
        rigol_ds1000.ch1.coupling = "DC"  # Reset to DC

    @pytest.mark.parametrize("scale", [0.01, 0.1, 1.0, 5.0, 10.0])
    def test_ch1_scale(self, rigol_ds1000, scale):
        rigol_ds1000.ch1.is_enabled = True
        rigol_ds1000.ch1.probe_ratio = 1
        rigol_ds1000.ch1.scale = scale
        assert rigol_ds1000.ch1.scale == scale

    def test_ch1_offset(self, rigol_ds1000):
        rigol_ds1000.ch1.is_enabled = True
        rigol_ds1000.ch1.probe_ratio = 1
        rigol_ds1000.ch1.scale = 1.0  # < 5 V/div => offset range ±20 V
        rigol_ds1000.ch1.offset = 2.0
        assert rigol_ds1000.ch1.offset == pytest.approx(2.0, rel=0.01)
        rigol_ds1000.ch1.offset = 0.0  # Reset

    def test_ch1_range(self, rigol_ds1000):
        rigol_ds1000.ch1.is_enabled = True
        rigol_ds1000.ch1.probe_ratio = 1
        rigol_ds1000.ch1.range = 8.0  # 8 V total, = 1 V/div
        assert rigol_ds1000.ch1.range == pytest.approx(8.0, rel=0.01)

    @pytest.mark.parametrize("probe", [1, 10, 100])
    def test_ch1_probe_ratio(self, rigol_ds1000, probe):
        rigol_ds1000.ch1.probe_ratio = probe
        assert rigol_ds1000.ch1.probe_ratio == probe
        rigol_ds1000.ch1.probe_ratio = 10  # Reset to 10X default

    @pytest.mark.parametrize("units", ["VOLT", "AMP"])
    def test_ch1_units(self, rigol_ds1000, units):
        rigol_ds1000.ch1.units = units
        assert rigol_ds1000.ch1.units == units
        rigol_ds1000.ch1.units = "VOLT"  # Reset

    def test_ch1_invert(self, rigol_ds1000):
        rigol_ds1000.ch1.is_inverted = True
        assert rigol_ds1000.ch1.is_inverted is True
        rigol_ds1000.ch1.is_inverted = False
        assert rigol_ds1000.ch1.is_inverted is False

    def test_ch1_vernier(self, rigol_ds1000):
        rigol_ds1000.ch1.vernier_enabled = True
        assert rigol_ds1000.ch1.vernier_enabled is True
        rigol_ds1000.ch1.vernier_enabled = False
        assert rigol_ds1000.ch1.vernier_enabled is False

    def test_ch1_delay_calibration(self, rigol_ds1000):
        rigol_ds1000.ch1.delay_calibration = 0.0
        assert rigol_ds1000.ch1.delay_calibration == pytest.approx(0.0, abs=1e-10)


# ---------------------------------------------------------------------------
# Timebase Subsystem
# ---------------------------------------------------------------------------
class TestTimebaseSubsystem:
    """Test every command and property in the Timebase subsystem."""

    @pytest.mark.parametrize("scale", [5e-9, 1e-6, 100e-6, 5e-3, 50.0])
    def test_timebase_scale(self, rigol_ds1000, scale):
        rigol_ds1000.timebase_delay_enabled = (
            False  # Delay scale must be disabled to set main scale to low values
        )
        rigol_ds1000.timebase_mode = "MAIN"
        rigol_ds1000.timebase_scale = scale
        assert rigol_ds1000.timebase_scale == scale

    def test_timebase_offset(self, rigol_ds1000):
        rigol_ds1000.timebase_mode = "MAIN"
        rigol_ds1000.timebase_scale = 1e-3
        rigol_ds1000.timebase_offset = 0.0
        assert rigol_ds1000.timebase_offset == pytest.approx(0.0, abs=1e-6)

    @pytest.mark.parametrize("mode", ["MAIN", "XY", "ROLL"])
    def test_timebase_mode(self, rigol_ds1000, mode):
        rigol_ds1000.timebase_mode = mode
        sleep(3)  # Wait for mode change to take effect
        assert rigol_ds1000.timebase_mode == mode
        rigol_ds1000.timebase_mode = "MAIN"  # Reset
        sleep(1)

    def test_timebase_delay_enabled(self, rigol_ds1000):
        rigol_ds1000.timebase_mode = "MAIN"
        rigol_ds1000.timebase_delay_enabled = True
        assert rigol_ds1000.timebase_delay_enabled is True
        rigol_ds1000.timebase_delay_enabled = False
        assert rigol_ds1000.timebase_delay_enabled is False

    @pytest.mark.parametrize("scale", [5e-9, 1e-7, 5e-7, 1e-6])
    def test_timebase_delay_scale(self, rigol_ds1000, scale):
        rigol_ds1000.timebase_mode = "MAIN"
        rigol_ds1000.timebase_scale = 1e-6  # Main must be >= delay scale
        rigol_ds1000.timebase_delay_enabled = True
        rigol_ds1000.timebase_delay_scale = scale
        assert rigol_ds1000.timebase_delay_scale == scale
        rigol_ds1000.timebase_delay_enabled = False  # Reset


# ---------------------------------------------------------------------------
# Trigger Subsystem – Common
# ---------------------------------------------------------------------------
class TestTriggerCommon:
    """Test common trigger settings (mode-independent)."""

    @pytest.mark.parametrize(
        "mode",
        [
            "EDGE",
            "PULS",
            "RUNT",
            "WIND",
            "NEDG",
            "SLOP",
            "VID",
            "PATT",
            "DEL",
            "TIM",
            "DUR",
            "SHOL",
            "RS232",
            "IIC",
            "SPI",
        ],
    )
    def test_trigger_mode(self, rigol_ds1000, mode):
        rigol_ds1000.trigger_mode = mode
        assert rigol_ds1000.trigger_mode == mode
        rigol_ds1000.trigger_mode = "EDGE"  # Reset

    @pytest.mark.parametrize("coupling", ["AC", "DC", "LFR", "HFR"])
    def test_trigger_coupling(self, rigol_ds1000, coupling):
        rigol_ds1000.trigger_mode = "EDGE"
        rigol_ds1000.trigger_coupling = coupling
        assert rigol_ds1000.trigger_coupling == coupling

    def test_trigger_status(self, rigol_ds1000):
        status = rigol_ds1000.trigger_status
        assert status in ["TD", "WAIT", "RUN", "AUTO", "STOP"]

    @pytest.mark.parametrize("sweep", ["AUTO", "NORM", "SING"])
    def test_trigger_sweep(self, rigol_ds1000, sweep):
        rigol_ds1000.trigger_sweep = sweep
        assert rigol_ds1000.trigger_sweep == sweep
        rigol_ds1000.trigger_sweep = "AUTO"  # Reset

    def test_trigger_holdoff(self, rigol_ds1000):
        rigol_ds1000.trigger_holdoff = 1e-6
        assert rigol_ds1000.trigger_holdoff == pytest.approx(1e-6, rel=0.01)
        rigol_ds1000.trigger_holdoff = 500e-9  # Reset to minimum

    def test_trigger_noise_reject(self, rigol_ds1000):
        rigol_ds1000.trigger_noise_reject = True
        assert rigol_ds1000.trigger_noise_reject is True
        rigol_ds1000.trigger_noise_reject = False
        assert rigol_ds1000.trigger_noise_reject is False


# ---------------------------------------------------------------------------
# Trigger Subsystem – Edge
# ---------------------------------------------------------------------------
class TestTriggerEdge:
    """Test edge trigger settings."""

    @pytest.mark.parametrize("source", ["CHAN1", "CHAN2", "CHAN3", "CHAN4"])
    def test_trigger_edge_source(self, rigol_ds1000, source):
        _ensure_channel_enabled(rigol_ds1000, source[-1])
        rigol_ds1000.trigger_mode = "EDGE"
        rigol_ds1000.trigger_edge_source = source
        assert rigol_ds1000.trigger_edge_source == source

    @pytest.mark.parametrize("slope", ["POS", "NEG", "RFAL"])
    def test_trigger_edge_slope(self, rigol_ds1000, slope):
        rigol_ds1000.trigger_mode = "EDGE"
        rigol_ds1000.trigger_edge_slope = slope
        assert rigol_ds1000.trigger_edge_slope == slope

    def test_trigger_edge_level(self, rigol_ds1000):
        _ensure_channel_enabled(rigol_ds1000, 1)
        rigol_ds1000.trigger_mode = "EDGE"
        rigol_ds1000.trigger_edge_source = "CHAN1"
        rigol_ds1000.trigger_edge_level = 1.0
        assert rigol_ds1000.trigger_edge_level == pytest.approx(1.0, rel=0.01)
        rigol_ds1000.trigger_edge_level = 0.0  # Reset


# ---------------------------------------------------------------------------
# Trigger Subsystem – Pulse Width
# ---------------------------------------------------------------------------
class TestTriggerPulse:
    """Test pulse width trigger settings.

    The trigger mode is set to PULSE before each test.
    """

    @pytest.mark.parametrize("source", ["CHAN1", "CHAN2"])
    def test_trigger_pulse_source(self, rigol_ds1000, source):
        _ensure_channel_enabled(rigol_ds1000, source[-1])
        rigol_ds1000.trigger_mode = "PULS"
        rigol_ds1000.trigger_pulse_source = source
        assert rigol_ds1000.trigger_pulse_source == source

    @pytest.mark.parametrize("when", ["PGR", "PLES", "PGL"])
    def test_trigger_pulse_when(self, rigol_ds1000, when):
        rigol_ds1000.trigger_mode = "PULS"
        rigol_ds1000.trigger_pulse_when = when
        assert rigol_ds1000.trigger_pulse_when == when

    def test_trigger_pulse_width(self, rigol_ds1000):
        rigol_ds1000.trigger_mode = "PULS"
        rigol_ds1000.trigger_pulse_when = "PGR"
        rigol_ds1000.trigger_pulse_width = 1e-6
        assert rigol_ds1000.trigger_pulse_width == pytest.approx(1e-6, rel=0.01)

    def test_trigger_pulse_upper_lower_width(self, rigol_ds1000):
        rigol_ds1000.trigger_mode = "PULS"
        rigol_ds1000.trigger_pulse_when = "PGL"
        rigol_ds1000.trigger_pulse_lower_width = 1e-6
        assert rigol_ds1000.trigger_pulse_lower_width == pytest.approx(1e-6, rel=0.01)
        rigol_ds1000.trigger_pulse_upper_width = 5e-6
        assert rigol_ds1000.trigger_pulse_upper_width == pytest.approx(5e-6, rel=0.01)

    def test_trigger_pulse_level(self, rigol_ds1000):
        rigol_ds1000.trigger_mode = "PULS"
        rigol_ds1000.trigger_pulse_level = 0.5
        assert rigol_ds1000.trigger_pulse_level == pytest.approx(0.5, rel=0.01)


# ---------------------------------------------------------------------------
# Trigger Subsystem – Slope
# ---------------------------------------------------------------------------
class TestTriggerSlope:
    """Test slope trigger settings."""

    @pytest.mark.parametrize("source", ["CHAN1", "CHAN2"])
    def test_trigger_slope_source(self, rigol_ds1000, source):
        _ensure_channel_enabled(rigol_ds1000, source[-1])
        rigol_ds1000.trigger_mode = "SLOP"
        rigol_ds1000.trigger_slope_source = source
        assert rigol_ds1000.trigger_slope_source == source

    @pytest.mark.parametrize("when", ["PGR", "PLES", "NGR", "NLES"])
    def test_trigger_slope_when(self, rigol_ds1000, when):
        rigol_ds1000.trigger_mode = "SLOP"
        rigol_ds1000.trigger_slope_when = when
        assert rigol_ds1000.trigger_slope_when == when

    def test_trigger_slope_time(self, rigol_ds1000):
        rigol_ds1000.trigger_mode = "SLOP"
        rigol_ds1000.trigger_slope_when = "PGR"
        rigol_ds1000.trigger_slope_time = 1e-6
        assert rigol_ds1000.trigger_slope_time == pytest.approx(1e-6, rel=0.01)

    def test_trigger_slope_time_upper_lower(self, rigol_ds1000):
        rigol_ds1000.trigger_mode = "SLOP"
        rigol_ds1000.trigger_slope_when = "PGL"
        rigol_ds1000.trigger_slope_time_lower = 1e-6
        assert rigol_ds1000.trigger_slope_time_lower == pytest.approx(1e-6, rel=0.01)
        rigol_ds1000.trigger_slope_time_upper = 5e-6
        assert rigol_ds1000.trigger_slope_time_upper == pytest.approx(5e-6, rel=0.01)

    @pytest.mark.parametrize("window", ["TA", "TB", "TAB"])
    def test_trigger_slope_window(self, rigol_ds1000, window):
        rigol_ds1000.trigger_mode = "SLOP"
        rigol_ds1000.trigger_slope_window = window
        assert rigol_ds1000.trigger_slope_window == window

    def test_trigger_slope_levels(self, rigol_ds1000):
        rigol_ds1000.trigger_mode = "SLOP"
        rigol_ds1000.trigger_slope_level_a = 1.5
        assert rigol_ds1000.trigger_slope_level_a == pytest.approx(1.5, rel=0.01)
        rigol_ds1000.trigger_slope_level_b = 0.5
        assert rigol_ds1000.trigger_slope_level_b == pytest.approx(0.5, rel=0.01)


# ---------------------------------------------------------------------------
# Trigger Subsystem – Video
# ---------------------------------------------------------------------------
class TestTriggerVideo:
    """Test video trigger settings."""

    @pytest.mark.parametrize("source", ["CHAN1", "CHAN2"])
    def test_trigger_video_source(self, rigol_ds1000, source):
        _ensure_channel_enabled(rigol_ds1000, source[-1])
        rigol_ds1000.trigger_mode = "VID"
        rigol_ds1000.trigger_video_source = source
        assert rigol_ds1000.trigger_video_source == source

    @pytest.mark.parametrize("polarity", ["POS", "NEG"])
    def test_trigger_video_polarity(self, rigol_ds1000, polarity):
        rigol_ds1000.trigger_mode = "VID"
        rigol_ds1000.trigger_video_polarity = polarity
        assert rigol_ds1000.trigger_video_polarity == polarity

    @pytest.mark.parametrize("mode", ["ODDF", "EVEN", "ALIN"])
    def test_trigger_video_mode(self, rigol_ds1000, mode):
        rigol_ds1000.trigger_mode = "VID"
        rigol_ds1000.trigger_video_mode = mode
        assert rigol_ds1000.trigger_video_mode == mode

    @pytest.mark.parametrize("standard", ["PALS", "NTSC", "480P", "576P"])
    def test_trigger_video_standard(self, rigol_ds1000, standard):
        rigol_ds1000.trigger_mode = "VID"
        rigol_ds1000.trigger_video_standard = standard
        assert rigol_ds1000.trigger_video_standard == standard

    def test_trigger_video_line(self, rigol_ds1000):
        rigol_ds1000.trigger_mode = "VID"
        rigol_ds1000.trigger_video_mode = "LINE"
        rigol_ds1000.trigger_video_line = 100
        assert rigol_ds1000.trigger_video_line == 100

    def test_trigger_video_level(self, rigol_ds1000):
        rigol_ds1000.trigger_mode = "VID"
        rigol_ds1000.trigger_video_level = 0.5
        assert rigol_ds1000.trigger_video_level == pytest.approx(0.5, rel=0.01)


# ---------------------------------------------------------------------------
# Trigger Subsystem – Duration
# ---------------------------------------------------------------------------


# TODO: The d_type is not implemented correctly in the driver
class TestTriggerDuration:
    """Test duration trigger settings."""

    def test_trigger_duration_source(self, rigol_ds1000):
        _ensure_channel_enabled(rigol_ds1000, 1)
        rigol_ds1000.trigger_mode = "DUR"
        rigol_ds1000.trigger_duration_source = "CHAN1"
        assert rigol_ds1000.trigger_duration_source == "CHAN1"

    @pytest.mark.parametrize("d_type", ["PGR", "PLES", "NGR", "NLES"])
    def test_trigger_duration_type(self, rigol_ds1000, d_type):
        rigol_ds1000.trigger_mode = "DUR"
        rigol_ds1000.trigger_duration_type = d_type
        assert rigol_ds1000.trigger_duration_type == d_type

    def test_trigger_duration_time_upper_lower(self, rigol_ds1000):
        rigol_ds1000.trigger_mode = "DUR"
        rigol_ds1000.trigger_duration_type = "PGL"
        rigol_ds1000.trigger_duration_time_lower = 100e-9
        assert rigol_ds1000.trigger_duration_time_lower == pytest.approx(100e-9, rel=0.01)
        rigol_ds1000.trigger_duration_time_upper = 1e-6
        assert rigol_ds1000.trigger_duration_time_upper == pytest.approx(1e-6, rel=0.01)


# ---------------------------------------------------------------------------
# Trigger Subsystem – Timeout
# ---------------------------------------------------------------------------
class TestTriggerTimeout:
    """Test timeout trigger settings."""

    def test_trigger_timeout_source(self, rigol_ds1000):
        _ensure_channel_enabled(rigol_ds1000, 1)
        rigol_ds1000.trigger_mode = "TIM"
        rigol_ds1000.trigger_timeout_source = "CHAN1"
        assert rigol_ds1000.trigger_timeout_source == "CHAN1"

    @pytest.mark.parametrize("slope", ["POS", "NEG", "RFAL"])
    def test_trigger_timeout_slope(self, rigol_ds1000, slope):
        rigol_ds1000.trigger_mode = "TIM"
        rigol_ds1000.trigger_timeout_slope = slope
        assert rigol_ds1000.trigger_timeout_slope == slope

    def test_trigger_timeout_time(self, rigol_ds1000):
        rigol_ds1000.trigger_mode = "TIM"
        rigol_ds1000.trigger_timeout_time = 100e-6
        assert rigol_ds1000.trigger_timeout_time == pytest.approx(100e-6, rel=0.01)


# ---------------------------------------------------------------------------
# Trigger Subsystem – Runt
# ---------------------------------------------------------------------------


# TODO: Check FAILED tests/instruments/rigol/test_rigol_ds1000.py::TestTriggerRunt::test_trigger_runt_when[PGR] - AssertionError: assert 'NONE' == 'PGR'
class TestTriggerRunt:
    """Test runt pulse trigger settings."""

    @pytest.mark.parametrize("source", ["CHAN1", "CHAN2"])
    def test_trigger_runt_source(self, rigol_ds1000, source):
        _ensure_channel_enabled(rigol_ds1000, source[-1])
        rigol_ds1000.trigger_mode = "RUNT"
        rigol_ds1000.trigger_runt_source = source
        assert rigol_ds1000.trigger_runt_source == source

    @pytest.mark.parametrize("polarity", ["POS", "NEG"])
    def test_trigger_runt_polarity(self, rigol_ds1000, polarity):
        rigol_ds1000.trigger_mode = "RUNT"
        rigol_ds1000.trigger_runt_polarity = polarity
        assert rigol_ds1000.trigger_runt_polarity == polarity

    @pytest.mark.parametrize("when", ["NONE", "PGR", "PLES"])
    def test_trigger_runt_when(self, rigol_ds1000, when):
        rigol_ds1000.trigger_mode = "RUNT"
        rigol_ds1000.trigger_runt_when = when
        assert rigol_ds1000.trigger_runt_when == when

    def test_trigger_runt_width(self, rigol_ds1000):
        rigol_ds1000.trigger_mode = "RUNT"
        rigol_ds1000.trigger_runt_when = "PGR"
        rigol_ds1000.trigger_runt_width = 1e-6
        assert rigol_ds1000.trigger_runt_width == pytest.approx(1e-6, rel=0.01)

    def test_trigger_runt_upper_lower_width(self, rigol_ds1000):
        rigol_ds1000.trigger_mode = "RUNT"
        rigol_ds1000.trigger_runt_when = "PGL"
        rigol_ds1000.trigger_runt_lower_width = 1e-6
        assert rigol_ds1000.trigger_runt_lower_width == pytest.approx(1e-6, rel=0.01)
        rigol_ds1000.trigger_runt_upper_width = 5e-6
        assert rigol_ds1000.trigger_runt_upper_width == pytest.approx(5e-6, rel=0.01)

    def test_trigger_runt_levels(self, rigol_ds1000):
        rigol_ds1000.trigger_mode = "RUNT"
        rigol_ds1000.trigger_runt_level_upper = 1.0
        assert rigol_ds1000.trigger_runt_level_upper == pytest.approx(1.0, rel=0.01)
        rigol_ds1000.trigger_runt_level_lower = -1.0
        assert rigol_ds1000.trigger_runt_level_lower == pytest.approx(-1.0, rel=0.01)


# ---------------------------------------------------------------------------
# Trigger Subsystem – Windows
# ---------------------------------------------------------------------------
class TestTriggerWindows:
    """Test windows trigger settings."""

    @pytest.mark.parametrize("source", ["CHAN1", "CHAN2"])
    def test_trigger_windows_source(self, rigol_ds1000, source):
        _ensure_channel_enabled(rigol_ds1000, source[-1])
        rigol_ds1000.trigger_mode = "WIND"
        rigol_ds1000.trigger_windows_source = source
        assert rigol_ds1000.trigger_windows_source == source

    @pytest.mark.parametrize("slope", ["POS", "NEG", "RFAL"])
    def test_trigger_windows_slope(self, rigol_ds1000, slope):
        rigol_ds1000.trigger_mode = "WIND"
        rigol_ds1000.trigger_windows_slope = slope
        assert rigol_ds1000.trigger_windows_slope == slope

    @pytest.mark.parametrize("position", ["EXIT", "ENTER", "TIM"])
    def test_trigger_windows_position(self, rigol_ds1000, position):
        rigol_ds1000.trigger_mode = "WIND"
        rigol_ds1000.trigger_windows_position = position
        assert rigol_ds1000.trigger_windows_position == position

    def test_trigger_windows_time(self, rigol_ds1000):
        rigol_ds1000.trigger_mode = "WIND"
        rigol_ds1000.trigger_windows_position = "TIM"
        rigol_ds1000.trigger_windows_time = 1e-6
        assert rigol_ds1000.trigger_windows_time == pytest.approx(1e-6, rel=0.01)

    def test_trigger_windows_levels(self, rigol_ds1000):
        rigol_ds1000.trigger_mode = "WIND"
        rigol_ds1000.trigger_windows_level_upper = 1.0
        assert rigol_ds1000.trigger_windows_level_upper == pytest.approx(1.0, rel=0.01)
        rigol_ds1000.trigger_windows_level_lower = -1.0
        assert rigol_ds1000.trigger_windows_level_lower == pytest.approx(-1.0, rel=0.01)


# ---------------------------------------------------------------------------
# Trigger Subsystem – Delay
# ---------------------------------------------------------------------------
class TestTriggerDelay:
    """Test delay trigger settings.

    Requires signals on two channels. Use channels 1 and 2.
    """

    def test_trigger_delay_sources(self, rigol_ds1000):
        _ensure_channel_enabled(rigol_ds1000, 1)
        _ensure_channel_enabled(rigol_ds1000, 2)
        rigol_ds1000.trigger_mode = "DEL"
        rigol_ds1000.trigger_delay_source_a = "CHAN1"
        assert rigol_ds1000.trigger_delay_source_a == "CHAN1"
        rigol_ds1000.trigger_delay_source_b = "CHAN2"
        assert rigol_ds1000.trigger_delay_source_b == "CHAN2"

    @pytest.mark.parametrize("slope", ["POS", "NEG"])
    def test_trigger_delay_slope_a(self, rigol_ds1000, slope):
        rigol_ds1000.trigger_mode = "DEL"
        rigol_ds1000.trigger_delay_slope_a = slope
        assert rigol_ds1000.trigger_delay_slope_a == slope

    @pytest.mark.parametrize("slope", ["POS", "NEG"])
    def test_trigger_delay_slope_b(self, rigol_ds1000, slope):
        rigol_ds1000.trigger_mode = "DEL"
        rigol_ds1000.trigger_delay_slope_b = slope
        assert rigol_ds1000.trigger_delay_slope_b == slope

    @pytest.mark.parametrize("type_", ["GRE", "LESS"])
    def test_trigger_delay_type(self, rigol_ds1000, type_):
        rigol_ds1000.trigger_mode = "DEL"
        rigol_ds1000.trigger_delay_type = type_
        assert rigol_ds1000.trigger_delay_type == type_

    def test_trigger_delay_time_upper_lower(self, rigol_ds1000):
        rigol_ds1000.trigger_mode = "DEL"
        rigol_ds1000.trigger_delay_type = "GLES"
        rigol_ds1000.trigger_delay_time_lower = 1e-6
        assert rigol_ds1000.trigger_delay_time_lower == pytest.approx(1e-6, rel=0.01)
        rigol_ds1000.trigger_delay_time_upper = 5e-6
        assert rigol_ds1000.trigger_delay_time_upper == pytest.approx(5e-6, rel=0.01)


# ---------------------------------------------------------------------------
# Trigger Subsystem – Setup/Hold
# ---------------------------------------------------------------------------
class TestTriggerSHOL:
    """Test setup/hold trigger settings.

    Clock and data source must be different channels.
    """

    def test_trigger_shol_sources(self, rigol_ds1000):
        _ensure_channel_enabled(rigol_ds1000, 1)
        _ensure_channel_enabled(rigol_ds1000, 2)
        rigol_ds1000.trigger_mode = "SHOL"
        rigol_ds1000.trigger_shol_clock_source = "CHAN1"
        assert rigol_ds1000.trigger_shol_clock_source == "CHAN1"
        rigol_ds1000.trigger_shol_data_source = "CHAN2"
        assert rigol_ds1000.trigger_shol_data_source == "CHAN2"

    @pytest.mark.parametrize("slope", ["POS", "NEG"])
    def test_trigger_shol_slope(self, rigol_ds1000, slope):
        rigol_ds1000.trigger_mode = "SHOL"
        rigol_ds1000.trigger_shol_slope = slope
        assert rigol_ds1000.trigger_shol_slope == slope

    @pytest.mark.parametrize("pattern", ["H", "L"])
    def test_trigger_shol_pattern(self, rigol_ds1000, pattern):
        rigol_ds1000.trigger_mode = "SHOL"
        rigol_ds1000.trigger_shol_pattern = pattern
        assert rigol_ds1000.trigger_shol_pattern == pattern

    @pytest.mark.parametrize("type_", ["SET", "HOL", "SETHOL"])
    def test_trigger_shol_type(self, rigol_ds1000, type_):
        rigol_ds1000.trigger_mode = "SHOL"
        rigol_ds1000.trigger_shol_type = type_
        assert rigol_ds1000.trigger_shol_type == type_

    def test_trigger_shol_setup_time(self, rigol_ds1000):
        rigol_ds1000.trigger_mode = "SHOL"
        rigol_ds1000.trigger_shol_setup_time = 100e-9
        assert rigol_ds1000.trigger_shol_setup_time == pytest.approx(100e-9, rel=0.01)

    def test_trigger_shol_hold_time(self, rigol_ds1000):
        rigol_ds1000.trigger_mode = "SHOL"
        rigol_ds1000.trigger_shol_hold_time = 100e-9
        assert rigol_ds1000.trigger_shol_hold_time == pytest.approx(100e-9, rel=0.01)


# ---------------------------------------------------------------------------
# Trigger Subsystem – Nth Edge
# ---------------------------------------------------------------------------
class TestTriggerNthEdge:
    """Test Nth edge trigger settings."""

    @pytest.mark.parametrize("source", ["CHAN1", "CHAN2"])
    def test_trigger_nedge_source(self, rigol_ds1000, source):
        _ensure_channel_enabled(rigol_ds1000, source[-1])
        rigol_ds1000.trigger_mode = "NEDG"
        rigol_ds1000.trigger_nedge_source = source
        assert rigol_ds1000.trigger_nedge_source == source

    @pytest.mark.parametrize("slope", ["POS", "NEG"])
    def test_trigger_nedge_slope(self, rigol_ds1000, slope):
        rigol_ds1000.trigger_mode = "NEDG"
        rigol_ds1000.trigger_nedge_slope = slope
        assert rigol_ds1000.trigger_nedge_slope == slope

    def test_trigger_nedge_idle(self, rigol_ds1000):
        rigol_ds1000.trigger_mode = "NEDG"
        rigol_ds1000.trigger_nedge_idle = 1e-6
        assert rigol_ds1000.trigger_nedge_idle == pytest.approx(1e-6, rel=0.01)

    @pytest.mark.parametrize("n", [1, 2, 5, 10])
    def test_trigger_nedge_edge(self, rigol_ds1000, n):
        rigol_ds1000.trigger_mode = "NEDG"
        rigol_ds1000.trigger_nedge_edge = n
        assert rigol_ds1000.trigger_nedge_edge == n

    def test_trigger_nedge_level(self, rigol_ds1000):
        rigol_ds1000.trigger_mode = "NEDG"
        rigol_ds1000.trigger_nedge_level = 0.5
        assert rigol_ds1000.trigger_nedge_level == pytest.approx(0.5, rel=0.01)


# ---------------------------------------------------------------------------
# Trigger Subsystem – RS232/UART
# ---------------------------------------------------------------------------
class TestTriggerRS232:
    """Test RS232/UART trigger settings."""

    @pytest.mark.parametrize("source", ["CHAN1", "CHAN2"])
    def test_trigger_rs232_source(self, rigol_ds1000, source):
        _ensure_channel_enabled(rigol_ds1000, source[-1])
        rigol_ds1000.trigger_mode = "RS232"
        rigol_ds1000.trigger_rs232_source = source
        assert rigol_ds1000.trigger_rs232_source == source

    @pytest.mark.parametrize("when", ["STAR", "ERR", "PAR", "DATA"])
    def test_trigger_rs232_when(self, rigol_ds1000, when):
        rigol_ds1000.trigger_mode = "RS232"
        rigol_ds1000.trigger_rs232_when = when
        assert rigol_ds1000.trigger_rs232_when == when

    @pytest.mark.parametrize("baud", [9600, 19200, 115200, "USER"])
    def test_trigger_rs232_baud(self, rigol_ds1000, baud):
        rigol_ds1000.trigger_mode = "RS232"
        rigol_ds1000.trigger_rs232_baud = baud
        assert rigol_ds1000.trigger_rs232_baud == baud

    @pytest.mark.parametrize("userbaud", [111, 23456, 999_999])
    def test_trigger_rs232_user_baud(self, rigol_ds1000, userbaud):
        rigol_ds1000.trigger_mode = "RS232"
        rigol_ds1000.trigger_rs232_baud = "USER"
        rigol_ds1000.trigger_rs232_user_baud = userbaud
        assert rigol_ds1000.trigger_rs232_user_baud == userbaud

    @pytest.mark.parametrize("parity", ["NONE", "EVEN", "ODD"])
    def test_trigger_rs232_parity(self, rigol_ds1000, parity):
        rigol_ds1000.trigger_mode = "RS232"
        rigol_ds1000.trigger_rs232_parity = parity
        assert rigol_ds1000.trigger_rs232_parity == parity

    @pytest.mark.parametrize("stop", [1, 2])
    def test_trigger_rs232_stop_bits(self, rigol_ds1000, stop):
        rigol_ds1000.trigger_mode = "RS232"
        rigol_ds1000.trigger_rs232_stop_bits = stop
        assert rigol_ds1000.trigger_rs232_stop_bits == float(stop)

    @pytest.mark.parametrize("bits", [5, 6, 7, 8])
    def test_trigger_rs232_data_bits(self, rigol_ds1000, bits):
        rigol_ds1000.trigger_mode = "RS232"
        rigol_ds1000.trigger_rs232_data_bits = bits
        assert rigol_ds1000.trigger_rs232_data_bits == bits

    @pytest.mark.parametrize("datalen", [0, 31, 254])
    def test_trigger_rs232_data_width(self, rigol_ds1000, datalen):
        rigol_ds1000.trigger_mode = "RS232"
        rigol_ds1000.trigger_rs232_data_bits = 8
        rigol_ds1000.trigger_rs232_data_width = datalen
        assert rigol_ds1000.trigger_rs232_data_width == datalen

    def test_trigger_rs232_level(self, rigol_ds1000):
        rigol_ds1000.trigger_mode = "RS232"
        rigol_ds1000.trigger_rs232_level = 1.5
        assert rigol_ds1000.trigger_rs232_level == pytest.approx(1.5, rel=0.01)


# ---------------------------------------------------------------------------
# Trigger Subsystem – I2C
# ---------------------------------------------------------------------------
class TestTriggerI2C:
    """Test I2C trigger settings.

    The clock (SCL) and data (SDA) sources must be on different channels.
    """

    def test_trigger_i2c_sources(self, rigol_ds1000):
        _ensure_channel_enabled(rigol_ds1000, 1)
        _ensure_channel_enabled(rigol_ds1000, 2)
        rigol_ds1000.trigger_mode = "IIC"
        rigol_ds1000.trigger_i2c_clock_source = "CHAN1"
        assert rigol_ds1000.trigger_i2c_clock_source == "CHAN1"
        rigol_ds1000.trigger_i2c_data_source = "CHAN2"
        assert rigol_ds1000.trigger_i2c_data_source == "CHAN2"

    @pytest.mark.parametrize("when", ["STAR", "REST", "STOP", "NACK", "ADDR", "DATA", "ADAT"])
    def test_trigger_i2c_when(self, rigol_ds1000, when):
        rigol_ds1000.trigger_mode = "IIC"
        rigol_ds1000.trigger_i2c_when = when
        assert rigol_ds1000.trigger_i2c_when == when

    @pytest.mark.parametrize("bits", [7, 8, 10])
    def test_trigger_i2c_address_width(self, rigol_ds1000, bits):
        rigol_ds1000.trigger_mode = "IIC"
        rigol_ds1000.trigger_i2c_when = "ADDR"
        rigol_ds1000.trigger_i2c_awidth = bits
        assert rigol_ds1000.trigger_i2c_awidth == bits

    @pytest.mark.parametrize("address", [0, 255, 1012])
    def test_trigger_i2c_address(self, rigol_ds1000, address):
        rigol_ds1000.trigger_mode = "IIC"
        rigol_ds1000.trigger_i2c_when = "ADDR"
        rigol_ds1000.trigger_i2c_awidth = 10
        rigol_ds1000.trigger_i2c_address = address
        assert rigol_ds1000.trigger_i2c_address == address

    @pytest.mark.parametrize("direction", ["READ", "WRIT", "RWR"])
    def test_trigger_i2c_direction(self, rigol_ds1000, direction):
        rigol_ds1000.trigger_mode = "IIC"
        rigol_ds1000.trigger_i2c_direction = direction
        assert rigol_ds1000.trigger_i2c_direction == direction

    @pytest.mark.parametrize("data_bits", [0, 255, 4096, 2**32 - 1])
    def test_trigger_i2c_data(self, rigol_ds1000, data_bits):
        rigol_ds1000.trigger_mode = "IIC"
        rigol_ds1000.trigger_i2c_when = "DATA"
        rigol_ds1000.trigger_i2c_data_bits = data_bits
        assert rigol_ds1000.trigger_i2c_data_bits == data_bits

    def test_trigger_i2c_levels(self, rigol_ds1000):
        rigol_ds1000.trigger_mode = "IIC"
        rigol_ds1000.trigger_i2c_clock_level = 1.5
        assert rigol_ds1000.trigger_i2c_clock_level == pytest.approx(1.5, rel=0.01)
        rigol_ds1000.trigger_i2c_data_level = 1.5
        assert rigol_ds1000.trigger_i2c_data_level == pytest.approx(1.5, rel=0.01)


# ---------------------------------------------------------------------------
# Trigger Subsystem – SPI
# ---------------------------------------------------------------------------
class TestTriggerSPI:
    """Test SPI trigger settings."""

    def test_trigger_spi_sources(self, rigol_ds1000):
        _ensure_channel_enabled(rigol_ds1000, 1)
        _ensure_channel_enabled(rigol_ds1000, 2)
        rigol_ds1000.trigger_mode = "SPI"
        rigol_ds1000.trigger_spi_clock_source = "CHAN1"
        assert rigol_ds1000.trigger_spi_clock_source == "CHAN1"
        rigol_ds1000.trigger_spi_data_source = "CHAN2"
        assert rigol_ds1000.trigger_spi_data_source == "CHAN2"

    @pytest.mark.parametrize("when", ["CS", "TIM", "DATA"])
    def test_trigger_spi_when(self, rigol_ds1000, when):
        rigol_ds1000.trigger_mode = "SPI"
        rigol_ds1000.trigger_spi_when = when
        assert rigol_ds1000.trigger_spi_when == when

    @pytest.mark.parametrize("slope", ["POS", "NEG"])
    def test_trigger_spi_clock_slope(self, rigol_ds1000, slope):
        rigol_ds1000.trigger_mode = "SPI"
        rigol_ds1000.trigger_spi_clock_slope = slope
        assert rigol_ds1000.trigger_spi_clock_slope == slope

    def test_trigger_spi_width(self, rigol_ds1000):
        rigol_ds1000.trigger_mode = "SPI"
        rigol_ds1000.trigger_spi_width = 8
        assert rigol_ds1000.trigger_spi_width == 8

    def test_trigger_spi_levels(self, rigol_ds1000):
        rigol_ds1000.trigger_mode = "SPI"
        rigol_ds1000.trigger_spi_clock_level = 1.5
        assert rigol_ds1000.trigger_spi_clock_level == pytest.approx(1.5, rel=0.01)
        rigol_ds1000.trigger_spi_data_level = 1.5
        assert rigol_ds1000.trigger_spi_data_level == pytest.approx(1.5, rel=0.01)

    def test_trigger_spi_timeout(self, rigol_ds1000):
        rigol_ds1000.trigger_mode = "SPI"
        rigol_ds1000.trigger_spi_timeout = True
        assert rigol_ds1000.trigger_spi_timeout is True
        rigol_ds1000.trigger_spi_timeout = False

    @pytest.mark.parametrize("polarity", ["POS", "NEG"])
    def test_trigger_spi_cs_polarity(self, rigol_ds1000, polarity):
        rigol_ds1000.trigger_mode = "SPI"
        rigol_ds1000.trigger_spi_cs_polarity = polarity
        assert rigol_ds1000.trigger_spi_cs_polarity == polarity

    def test_trigger_reset_to_edge(self, rigol_ds1000):
        """Restore to edge trigger at the end of all trigger tests."""
        _ensure_channel_enabled(rigol_ds1000, 1)
        rigol_ds1000.trigger_mode = "EDGE"
        rigol_ds1000.trigger_edge_source = "CHAN1"
        rigol_ds1000.trigger_edge_slope = "POS"


# ---------------------------------------------------------------------------
# Waveform Subsystem
# ---------------------------------------------------------------------------
class TestWaveformSubsystem:
    """Test waveform data acquisition.

    Connect the probe compensation output (1 kHz, ~3 V square wave) to
    channel 1 so that waveform reads return meaningful data.
    The oscilloscope is stopped before reading to ensure stable data.
    """

    def test_waveform_source(self, rigol_ds1000):
        _ensure_channel_enabled(rigol_ds1000, 1)
        rigol_ds1000.waveform_source = "CHAN1"
        assert rigol_ds1000.waveform_source == "CHAN1"

    @pytest.mark.parametrize("mode", ["NORM", "MAX", "RAW"])
    def test_waveform_mode(self, rigol_ds1000, mode):
        rigol_ds1000.stop()
        sleep(0.3)
        rigol_ds1000.waveform_mode = mode
        assert rigol_ds1000.waveform_mode == mode

    @pytest.mark.parametrize("fmt", ["WORD", "BYTE", "ASC"])
    def test_waveform_format(self, rigol_ds1000, fmt):
        rigol_ds1000.waveform_format = fmt
        assert rigol_ds1000.waveform_format == fmt

    def test_waveform_start_stop(self, rigol_ds1000):
        rigol_ds1000.stop()
        sleep(0.3)
        rigol_ds1000.waveform_mode = "NORM"
        rigol_ds1000.waveform_start = 1
        assert rigol_ds1000.waveform_start == 1
        rigol_ds1000.waveform_stop = 1200
        assert rigol_ds1000.waveform_stop == 1200

    def test_waveform_preamble(self, rigol_ds1000):
        rigol_ds1000.stop()
        sleep(0.3)
        _ensure_channel_enabled(rigol_ds1000, 1)
        rigol_ds1000.waveform_source = "CHAN1"
        rigol_ds1000.waveform_mode = "NORM"
        preamble = rigol_ds1000.get_waveform_preamble()
        for key in (
            "format",
            "type",
            "points",
            "count",
            "xincrement",
            "xorigin",
            "xreference",
            "yincrement",
            "yorigin",
            "yreference",
        ):
            assert key in preamble
        assert isinstance(preamble["points"], int)
        assert preamble["points"] > 0
        assert isinstance(preamble["xincrement"], float)
        assert preamble["xincrement"] > 0

    def test_waveform_axis_parameters(self, rigol_ds1000):
        rigol_ds1000.stop()
        sleep(0.3)
        _ensure_channel_enabled(rigol_ds1000, 1)
        rigol_ds1000.waveform_source = "CHAN1"
        assert isinstance(rigol_ds1000.waveform_xincrement, float)
        assert isinstance(rigol_ds1000.waveform_xorigin, float)
        assert isinstance(rigol_ds1000.waveform_xreference, float)
        assert isinstance(rigol_ds1000.waveform_yincrement, float)
        assert isinstance(rigol_ds1000.waveform_yorigin, float)
        assert isinstance(rigol_ds1000.waveform_yreference, float)

    def test_waveform_data_byte(self, rigol_ds1000):
        """Read waveform in BYTE format and convert to voltages."""
        rigol_ds1000.stop()
        sleep(0.3)
        _ensure_channel_enabled(rigol_ds1000, 1)
        rigol_ds1000.waveform_source = "CHAN1"
        rigol_ds1000.waveform_mode = "NORM"
        rigol_ds1000.waveform_format = "BYTE"
        data = rigol_ds1000.get_waveform_data(raw=False)
        assert data is not None
        assert len(data) > 0

    def test_waveform_data_asc(self, rigol_ds1000):
        """Read waveform in ASCII format."""
        rigol_ds1000.stop()
        sleep(0.3)
        _ensure_channel_enabled(rigol_ds1000, 1)
        rigol_ds1000.waveform_source = "CHAN1"
        rigol_ds1000.waveform_mode = "NORM"
        rigol_ds1000.waveform_format = "ASC"
        data = rigol_ds1000.get_waveform_data(raw=False)
        assert data is not None
        assert len(data) > 0

    def test_waveform_resume(self, rigol_ds1000):
        """Resume oscilloscope after waveform tests."""
        rigol_ds1000.run()
        sleep(0.3)


# ---------------------------------------------------------------------------
# Display Subsystem
# ---------------------------------------------------------------------------
class TestDisplaySubsystem:
    """Test display settings."""

    def test_display_clear(self, rigol_ds1000):
        rigol_ds1000.display_clear()  # Just verify no exception is raised

    @pytest.mark.parametrize("type_", ["VECT", "DOTS"])
    def test_display_type(self, rigol_ds1000, type_):
        rigol_ds1000.display_type = type_
        assert rigol_ds1000.display_type == type_
        rigol_ds1000.display_type = "VECT"  # Reset

    def test_display_grading_time(self, rigol_ds1000):
        rigol_ds1000.display_grading_time = 1.0
        assert rigol_ds1000.display_grading_time == pytest.approx(1.0, rel=0.01)

    @pytest.mark.parametrize("brightness", [0, 50, 100])
    def test_display_waveform_brightness(self, rigol_ds1000, brightness):
        rigol_ds1000.display_waveform_brightness = brightness
        assert rigol_ds1000.display_waveform_brightness == brightness

    @pytest.mark.parametrize("grid", ["FULL", "HALF", "NONE"])
    def test_display_grid(self, rigol_ds1000, grid):
        rigol_ds1000.display_grid = grid
        assert rigol_ds1000.display_grid == grid
        rigol_ds1000.display_grid = "FULL"  # Reset

    @pytest.mark.parametrize("brightness", [0, 50, 100])
    def test_display_grid_brightness(self, rigol_ds1000, brightness):
        rigol_ds1000.display_grid_brightness = brightness
        assert rigol_ds1000.display_grid_brightness == brightness

    def test_get_display_data(self, rigol_ds1000):
        """Get a screenshot from the oscilloscope."""
        rigol_ds1000.storage_image_type = "PNG"
        data = rigol_ds1000.get_display_data()
        assert data is not None
        assert len(data) > 0


# ---------------------------------------------------------------------------
# Measurement Subsystem
# ---------------------------------------------------------------------------
class TestMeasurementSubsystem:
    """Test measurement settings and functions.

    Voltage and frequency measurements require a signal on channel 1.
    """

    @pytest.mark.parametrize("source", ["CHAN1", "CHAN2"])
    def test_measure_source(self, rigol_ds1000, source):
        _ensure_channel_enabled(rigol_ds1000, source[-1])
        rigol_ds1000.measure_source = source
        assert rigol_ds1000.measure_source == source

    def test_measure_all_display(self, rigol_ds1000):
        rigol_ds1000.measure_all_display = True
        assert rigol_ds1000.measure_all_display is True
        rigol_ds1000.measure_all_display = False
        assert rigol_ds1000.measure_all_display is False

    @pytest.mark.parametrize("source", ["CHAN1", "CHAN2"])
    def test_measure_all_source(self, rigol_ds1000, source):
        _ensure_channel_enabled(rigol_ds1000, source[-1])
        rigol_ds1000.measure_all_source = source
        assert rigol_ds1000.measure_all_source == source

    def test_measure_clear_recover(self, rigol_ds1000):
        rigol_ds1000.measure_clear()
        rigol_ds1000.measure_recover()

    def test_measure_setup_thresholds(self, rigol_ds1000):
        rigol_ds1000.measure_setup_max = 90
        assert rigol_ds1000.measure_setup_max == 90
        rigol_ds1000.measure_setup_mid = 50
        assert rigol_ds1000.measure_setup_mid == 50
        rigol_ds1000.measure_setup_min = 10
        assert rigol_ds1000.measure_setup_min == 10

    @pytest.mark.parametrize("source", ["CHAN1", "CHAN2", "CHAN3", "CHAN4"])
    def test_measure_phase_source_a(self, rigol_ds1000, source):
        _ensure_channel_enabled(rigol_ds1000, source[-1])
        rigol_ds1000.measure_phase_source_a = source
        assert rigol_ds1000.measure_phase_source_a == source

    @pytest.mark.parametrize("source", ["CHAN1", "CHAN2", "CHAN3", "CHAN4"])
    def test_measure_phase_source_b(self, rigol_ds1000, source):
        _ensure_channel_enabled(rigol_ds1000, source[-1])
        rigol_ds1000.measure_phase_source_b = source
        assert rigol_ds1000.measure_phase_source_b == source

    @pytest.mark.parametrize("source", ["CHAN1", "CHAN2", "CHAN3", "CHAN4"])
    def test_measure_delay_source_a(self, rigol_ds1000, source):
        _ensure_channel_enabled(rigol_ds1000, source[-1])
        rigol_ds1000.measure_delay_source_a = source
        assert rigol_ds1000.measure_delay_source_a == source

    @pytest.mark.parametrize("source", ["CHAN1", "CHAN2", "CHAN3", "CHAN4"])
    def test_measure_delay_source_b(self, rigol_ds1000, source):
        _ensure_channel_enabled(rigol_ds1000, source[-1])
        rigol_ds1000.measure_delay_source_b = source
        assert rigol_ds1000.measure_delay_source_b == source

    def test_measure_statistic_display(self, rigol_ds1000):
        rigol_ds1000.measure_statistic_display = True
        assert rigol_ds1000.measure_statistic_display is True
        rigol_ds1000.measure_statistic_display = False
        assert rigol_ds1000.measure_statistic_display is False

    @pytest.mark.parametrize("mode", ["DIFF", "EXTR"])
    def test_measure_statistic_mode(self, rigol_ds1000, mode):
        rigol_ds1000.measure_statistic_mode = mode
        assert rigol_ds1000.measure_statistic_mode == mode

    def test_measure_statistic_reset(self, rigol_ds1000):
        rigol_ds1000.measure_statistic_reset()

    def test_measure_item_vpp(self, rigol_ds1000):
        """Measure VPP – requires a signal on channel 1."""
        rigol_ds1000.run()
        sleep(0.5)
        _ensure_channel_enabled(rigol_ds1000, 1)
        rigol_ds1000.measure_source = "CHAN1"
        vpp = rigol_ds1000.measure_item("VPP")
        assert isinstance(vpp, float)

    def test_measure_item_freq(self, rigol_ds1000):
        """Measure frequency – requires a periodic signal on channel 1."""
        rigol_ds1000.run()
        sleep(0.5)
        _ensure_channel_enabled(rigol_ds1000, 1)
        rigol_ds1000.measure_source = "CHAN1"
        freq = rigol_ds1000.measure_item("FREQ")
        assert isinstance(freq, float)

    def test_measure_counter_source(self, rigol_ds1000):
        _ensure_channel_enabled(rigol_ds1000, 1)
        rigol_ds1000.measure_counter_source = "CHAN1"
        assert rigol_ds1000.measure_counter_source == "CHAN1"

    def test_measure_counter_value(self, rigol_ds1000):
        """Read frequency counter – requires a periodic signal on channel 1."""
        rigol_ds1000.run()
        sleep(0.5)
        _ensure_channel_enabled(rigol_ds1000, 1)
        rigol_ds1000.measure_counter_source = "CHAN1"
        value = rigol_ds1000.measure_counter_value
        assert isinstance(value, float)

    def test_measure_item_statistic(self, rigol_ds1000):
        """Test statistic measurement – requires a signal on channel 1."""
        rigol_ds1000.run()
        sleep(0.5)
        _ensure_channel_enabled(rigol_ds1000, 1)
        stats = rigol_ds1000.measure_item_statistic("VPP", source="CHAN1")
        for key in ("current", "average", "min", "max", "deviation"):
            assert key in stats
            assert isinstance(stats[key], float)


# ---------------------------------------------------------------------------
# Cursor Subsystem
# ---------------------------------------------------------------------------
class TestCursorSubsystem:
    """Test cursor modes and settings."""

    @pytest.mark.parametrize("mode", ["OFF", "MAN", "TRAC", "AUTO"])
    def test_cursor_mode(self, rigol_ds1000, mode):
        rigol_ds1000.cursor_mode = mode
        assert rigol_ds1000.cursor_mode == mode
        rigol_ds1000.cursor_mode = "OFF"  # Reset

    class TestManualCursor:
        """Test manual cursor mode."""

        @pytest.mark.parametrize("type_", ["X", "Y", "XY"])
        def test_cursor_manual_type(self, rigol_ds1000, type_):
            rigol_ds1000.cursor_mode = "MAN"
            rigol_ds1000.cursor_manual_type = type_
            assert rigol_ds1000.cursor_manual_type == type_

        @pytest.mark.parametrize("source", ["CHAN1", "CHAN2", "CHAN3", "CHAN4"])
        def test_cursor_manual_source(self, rigol_ds1000, source):
            _ensure_channel_enabled(rigol_ds1000, source[-1])
            rigol_ds1000.cursor_mode = "MAN"
            rigol_ds1000.cursor_manual_source = source
            assert rigol_ds1000.cursor_manual_source == source

        @pytest.mark.parametrize("unit", ["S", "HZ", "DEGR", "PERC"])
        def test_cursor_manual_time_unit(self, rigol_ds1000, unit):
            rigol_ds1000.cursor_mode = "MAN"
            rigol_ds1000.cursor_manual_time_unit = unit
            assert rigol_ds1000.cursor_manual_time_unit == unit

        @pytest.mark.parametrize("unit", ["VOLT", "AMP"])
        def test_cursor_manual_voltage_unit(self, rigol_ds1000, unit):
            rigol_ds1000.cursor_mode = "MAN"
            rigol_ds1000.cursor_manual_voltage_unit = unit
            assert rigol_ds1000.cursor_manual_voltage_unit == unit

        def test_cursor_manual_x_positions(self, rigol_ds1000):
            rigol_ds1000.cursor_mode = "MAN"
            rigol_ds1000.cursor_manual_type = "X"
            rigol_ds1000.cursor_manual_time_unit = "S"
            rigol_ds1000.timebase_scale = 1e-3
            rigol_ds1000.cursor_manual_ax = -1e-3
            rigol_ds1000.cursor_manual_bx = 1e-3
            xdelta = rigol_ds1000.cursor_manual_xdelta
            assert isinstance(xdelta, float)
            # Verify readbacks
            assert isinstance(rigol_ds1000.cursor_manual_axvalue, float)
            assert isinstance(rigol_ds1000.cursor_manual_bxvalue, float)
            assert isinstance(rigol_ds1000.cursor_manual_inverse_xdelta, float)

        def test_cursor_manual_y_positions(self, rigol_ds1000):
            rigol_ds1000.cursor_mode = "MAN"
            rigol_ds1000.cursor_manual_type = "Y"
            rigol_ds1000.cursor_manual_ay = 1.0
            rigol_ds1000.cursor_manual_by = -1.0
            ydelta = rigol_ds1000.cursor_manual_ydelta
            assert isinstance(ydelta, float)
            assert isinstance(rigol_ds1000.cursor_manual_ayvalue, float)
            assert isinstance(rigol_ds1000.cursor_manual_byvalue, float)

    class TestTrackCursor:
        """Test track cursor mode."""

        @pytest.mark.parametrize("source", ["CHAN1", "CHAN2"])
        def test_cursor_track_source_a(self, rigol_ds1000, source):
            _ensure_channel_enabled(rigol_ds1000, source[-1])
            rigol_ds1000.cursor_mode = "TRAC"
            rigol_ds1000.cursor_track_source_a = source
            assert rigol_ds1000.cursor_track_source_a == source

        @pytest.mark.parametrize("source", ["CHAN1", "CHAN2"])
        def test_cursor_track_source_b(self, rigol_ds1000, source):
            _ensure_channel_enabled(rigol_ds1000, source[-1])
            rigol_ds1000.cursor_mode = "TRAC"
            rigol_ds1000.cursor_track_source_b = source
            assert rigol_ds1000.cursor_track_source_b == source

        @pytest.mark.parametrize("unit", ["S", "HZ", "DEGR", "PERC"])
        def test_cursor_track_time_unit(self, rigol_ds1000, unit):
            rigol_ds1000.cursor_mode = "TRAC"
            rigol_ds1000.cursor_track_time_unit = unit
            assert rigol_ds1000.cursor_track_time_unit == unit

        @pytest.mark.parametrize("unit", ["VOLT", "AMP"])
        def test_cursor_track_voltage_unit_a(self, rigol_ds1000, unit):
            rigol_ds1000.cursor_mode = "TRAC"
            rigol_ds1000.cursor_track_voltage_unit_a = unit
            assert rigol_ds1000.cursor_track_voltage_unit_a == unit

        def test_cursor_track_ax(self, rigol_ds1000):
            _ensure_channel_enabled(rigol_ds1000, 1)
            rigol_ds1000.cursor_mode = "TRAC"
            rigol_ds1000.cursor_track_source_a = "CHAN1"
            rigol_ds1000.cursor_track_ax = 0.0
            assert isinstance(rigol_ds1000.cursor_track_axvalue, float)
            assert isinstance(rigol_ds1000.cursor_track_ayvalue, float)
            assert isinstance(rigol_ds1000.cursor_track_xdelta, float)
            assert isinstance(rigol_ds1000.cursor_track_ydelta, float)

    class TestAutoCursor:
        """Test auto cursor mode."""

        @pytest.mark.parametrize("source", ["CHAN1", "CHAN2"])
        def test_cursor_auto_source(self, rigol_ds1000, source):
            _ensure_channel_enabled(rigol_ds1000, source[-1])
            rigol_ds1000.cursor_mode = "AUTO"
            rigol_ds1000.cursor_auto_source = source
            assert rigol_ds1000.cursor_auto_source == source

        @pytest.mark.parametrize("unit", ["S", "HZ"])
        def test_cursor_auto_time_unit(self, rigol_ds1000, unit):
            rigol_ds1000.cursor_mode = "AUTO"
            rigol_ds1000.cursor_auto_time_unit = unit
            assert rigol_ds1000.cursor_auto_time_unit == unit

        def test_cursor_auto_readbacks(self, rigol_ds1000):
            rigol_ds1000.cursor_mode = "AUTO"
            assert isinstance(rigol_ds1000.cursor_auto_axvalue, float)
            assert isinstance(rigol_ds1000.cursor_auto_bxvalue, float)
            assert isinstance(rigol_ds1000.cursor_auto_ayvalue, float)
            assert isinstance(rigol_ds1000.cursor_auto_byvalue, float)
            assert isinstance(rigol_ds1000.cursor_auto_xdelta, float)


# ---------------------------------------------------------------------------
# Math Subsystem
# ---------------------------------------------------------------------------
class TestMathSubsystem:
    """Test math operation settings."""

    def test_math_display(self, rigol_ds1000):
        rigol_ds1000.math_display = True
        assert rigol_ds1000.math_display is True
        rigol_ds1000.math_display = False
        assert rigol_ds1000.math_display is False

    @pytest.mark.parametrize("operator", ["ADD", "SUBT", "MULT", "DIV"])
    def test_math_operator(self, rigol_ds1000, operator):
        rigol_ds1000.math_display = True
        rigol_ds1000.math_operator = operator
        assert rigol_ds1000.math_operator == operator

    @pytest.mark.parametrize("source", ["CHAN1", "CHAN2", "CHAN3", "CHAN4"])
    def test_math_source1(self, rigol_ds1000, source):
        _ensure_channel_enabled(rigol_ds1000, source[-1])
        rigol_ds1000.math_display = True
        rigol_ds1000.math_operator = "ADD"
        rigol_ds1000.math_source1 = source
        assert rigol_ds1000.math_source1 == source

    @pytest.mark.parametrize("source", ["CHAN1", "CHAN2", "CHAN3", "CHAN4"])
    def test_math_source2(self, rigol_ds1000, source):
        _ensure_channel_enabled(rigol_ds1000, source[-1])
        rigol_ds1000.math_display = True
        rigol_ds1000.math_operator = "ADD"
        rigol_ds1000.math_source2 = source
        assert rigol_ds1000.math_source2 == source

    def test_math_scale(self, rigol_ds1000):
        rigol_ds1000.math_display = True
        rigol_ds1000.math_operator = "ADD"
        rigol_ds1000.math_scale = 1.0
        assert rigol_ds1000.math_scale == pytest.approx(1.0, rel=0.01)

    def test_math_offset(self, rigol_ds1000):
        rigol_ds1000.math_display = True
        rigol_ds1000.math_offset = 0.0
        assert rigol_ds1000.math_offset == pytest.approx(0.0, abs=0.01)

    def test_math_invert(self, rigol_ds1000):
        rigol_ds1000.math_display = True
        rigol_ds1000.math_invert = True
        assert rigol_ds1000.math_invert is True
        rigol_ds1000.math_invert = False
        assert rigol_ds1000.math_invert is False

    def test_math_reset(self, rigol_ds1000):
        rigol_ds1000.math_display = True
        rigol_ds1000.math_reset()

    class TestFFT:
        """Test FFT math settings.

        The oscilloscope must be in MAIN timebase mode.
        """

        @pytest.mark.parametrize("source", ["CHAN1", "CHAN2"])
        def test_math_fft_source(self, rigol_ds1000, source):
            _ensure_channel_enabled(rigol_ds1000, source[-1])
            rigol_ds1000.timebase_mode = "MAIN"
            rigol_ds1000.math_display = True
            rigol_ds1000.math_operator = "FFT"
            rigol_ds1000.math_fft_source = source
            assert rigol_ds1000.math_fft_source == source

        @pytest.mark.parametrize("window", ["RECT", "BLAC", "HANN", "HAMM", "FLAT", "TRI"])
        def test_math_fft_window(self, rigol_ds1000, window):
            rigol_ds1000.math_display = True
            rigol_ds1000.math_operator = "FFT"
            rigol_ds1000.math_fft_window = window
            assert rigol_ds1000.math_fft_window == window

        @pytest.mark.parametrize("unit", ["DB", "VRMS"])
        def test_math_fft_unit(self, rigol_ds1000, unit):
            rigol_ds1000.math_display = True
            rigol_ds1000.math_operator = "FFT"
            rigol_ds1000.math_fft_unit = unit
            assert rigol_ds1000.math_fft_unit == unit

        def test_math_fft_split(self, rigol_ds1000):
            rigol_ds1000.math_display = True
            rigol_ds1000.math_operator = "FFT"
            rigol_ds1000.math_fft_split = True
            assert rigol_ds1000.math_fft_split is True
            rigol_ds1000.math_fft_split = False
            assert rigol_ds1000.math_fft_split is False

        @pytest.mark.parametrize("mode", ["AMPL", "PSD"])
        def test_math_fft_mode(self, rigol_ds1000, mode):
            rigol_ds1000.math_display = True
            rigol_ds1000.math_operator = "FFT"
            rigol_ds1000.math_fft_mode = mode
            assert rigol_ds1000.math_fft_mode == mode

    class TestFilter:
        """Test math filter settings."""

        @pytest.mark.parametrize("type_", ["LPAS", "HPAS", "BPAS", "BST"])
        def test_math_filter_type(self, rigol_ds1000, type_):
            rigol_ds1000.math_display = True
            rigol_ds1000.math_operator = "FILT"
            rigol_ds1000.math_filter_type = type_
            assert rigol_ds1000.math_filter_type == type_

        def test_math_filter_w1(self, rigol_ds1000):
            rigol_ds1000.math_display = True
            rigol_ds1000.math_operator = "FILT"
            rigol_ds1000.math_filter_w1 = 1e3
            assert rigol_ds1000.math_filter_w1 == pytest.approx(1e3, rel=0.01)

        def test_math_filter_w2(self, rigol_ds1000):
            rigol_ds1000.math_display = True
            rigol_ds1000.math_operator = "FILT"
            rigol_ds1000.math_filter_type = "BPAS"
            rigol_ds1000.math_filter_w1 = 1e3
            rigol_ds1000.math_filter_w2 = 10e3
            assert rigol_ds1000.math_filter_w2 == pytest.approx(10e3, rel=0.01)


# ---------------------------------------------------------------------------
# Math Options Subsystem
# ---------------------------------------------------------------------------
class TestMathOptions:
    """Test math options."""

    def test_math_option_start_end(self, rigol_ds1000):
        rigol_ds1000.math_display = True
        rigol_ds1000.math_option_start = 0
        assert rigol_ds1000.math_option_start == 0
        rigol_ds1000.math_option_end = 1199
        assert rigol_ds1000.math_option_end == 1199

    def test_math_option_invert(self, rigol_ds1000):
        rigol_ds1000.math_display = True
        rigol_ds1000.math_option_invert = True
        assert rigol_ds1000.math_option_invert is True
        rigol_ds1000.math_option_invert = False

    def test_math_option_auto_scale(self, rigol_ds1000):
        rigol_ds1000.math_display = True
        rigol_ds1000.math_option_auto_scale = True
        assert rigol_ds1000.math_option_auto_scale is True
        rigol_ds1000.math_option_auto_scale = False

    def test_math_option_thresholds(self, rigol_ds1000):
        rigol_ds1000.math_display = True
        rigol_ds1000.math_option_threshold1 = 0.5
        assert rigol_ds1000.math_option_threshold1 == pytest.approx(0.5, rel=0.01)
        rigol_ds1000.math_option_threshold2 = 1.0
        assert rigol_ds1000.math_option_threshold2 == pytest.approx(1.0, rel=0.01)


# ---------------------------------------------------------------------------
# Mask Testing Subsystem
# ---------------------------------------------------------------------------
class TestMaskSubsystem:
    """Test pass/fail mask testing.

    A signal on channel 1 is recommended so that pass/fail counts accumulate.
    """

    def test_mask_source(self, rigol_ds1000):
        _ensure_channel_enabled(rigol_ds1000, 1)
        rigol_ds1000.mask_source = "CHAN1"
        assert rigol_ds1000.mask_source == "CHAN1"

    def test_mask_enable_disable(self, rigol_ds1000):
        _ensure_channel_enabled(rigol_ds1000, 1)
        rigol_ds1000.mask_source = "CHAN1"
        rigol_ds1000.mask_enable = True
        assert rigol_ds1000.mask_enable is True
        rigol_ds1000.mask_enable = False
        assert rigol_ds1000.mask_enable is False

    def test_mask_message_display(self, rigol_ds1000):
        rigol_ds1000.mask_message_display = True
        assert rigol_ds1000.mask_message_display is True
        rigol_ds1000.mask_message_display = False

    def test_mask_sound_output(self, rigol_ds1000):
        rigol_ds1000.mask_sound_output = False
        assert rigol_ds1000.mask_sound_output is False

    def test_mask_stop_on_fail(self, rigol_ds1000):
        rigol_ds1000.mask_stop_on_fail = False
        assert rigol_ds1000.mask_stop_on_fail is False

    def test_mask_x_y(self, rigol_ds1000):
        rigol_ds1000.mask_x = 0.2
        assert rigol_ds1000.mask_x == pytest.approx(0.2, rel=0.01)
        rigol_ds1000.mask_y = 0.2
        assert rigol_ds1000.mask_y == pytest.approx(0.2, rel=0.01)

    def test_mask_operate(self, rigol_ds1000):
        rigol_ds1000.mask_operate = "STOP"
        assert rigol_ds1000.mask_operate == "STOP"

    def test_mask_create_and_statistics(self, rigol_ds1000):
        """Create a mask and verify statistics can be read."""
        _ensure_channel_enabled(rigol_ds1000, 1)
        rigol_ds1000.mask_source = "CHAN1"
        rigol_ds1000.mask_x = 0.2
        rigol_ds1000.mask_y = 0.2
        rigol_ds1000.mask_create()
        sleep(0.5)
        assert isinstance(rigol_ds1000.mask_passed, (int, float))
        assert isinstance(rigol_ds1000.mask_failed, (int, float))
        assert isinstance(rigol_ds1000.mask_total, (int, float))

    def test_mask_reset(self, rigol_ds1000):
        rigol_ds1000.mask_reset()


# ---------------------------------------------------------------------------
# Storage Subsystem
# ---------------------------------------------------------------------------
class TestStorageSubsystem:
    """Test storage and screenshot settings."""

    @pytest.mark.parametrize("type_", ["PNG", "BMP8", "BMP24", "JPEG", "TIFF"])
    def test_storage_image_type(self, rigol_ds1000, type_):
        rigol_ds1000.storage_image_type = type_
        assert rigol_ds1000.storage_image_type == type_

    def test_storage_image_invert(self, rigol_ds1000):
        rigol_ds1000.storage_image_invert = True
        assert rigol_ds1000.storage_image_invert is True
        rigol_ds1000.storage_image_invert = False
        assert rigol_ds1000.storage_image_invert is False

    @pytest.mark.parametrize("color", ["ON", "OFF"])
    def test_storage_image_color(self, rigol_ds1000, color):
        rigol_ds1000.storage_image_color = color
        assert rigol_ds1000.storage_image_color == color


# ---------------------------------------------------------------------------
# System Subsystem
# ---------------------------------------------------------------------------
class TestSystemSubsystem:
    """Test system-level settings."""

    def test_system_autoscale_enabled(self, rigol_ds1000):
        rigol_ds1000.system_autoscale_enabled = True
        assert rigol_ds1000.system_autoscale_enabled is True
        rigol_ds1000.system_autoscale_enabled = False
        assert rigol_ds1000.system_autoscale_enabled is False
        rigol_ds1000.system_autoscale_enabled = True  # Leave enabled

    def test_system_beeper(self, rigol_ds1000):
        original = rigol_ds1000.system_beeper
        rigol_ds1000.system_beeper = not original
        assert rigol_ds1000.system_beeper is not original
        rigol_ds1000.system_beeper = original  # Restore

    def test_system_error(self, rigol_ds1000):
        """system_error must return a (int, str) tuple."""
        error_code, error_msg = rigol_ds1000.system_error
        assert isinstance(error_code, int)
        assert isinstance(error_msg, str)

    def test_system_locked(self, rigol_ds1000):
        rigol_ds1000.system_locked = True
        assert rigol_ds1000.system_locked is True
        rigol_ds1000.system_locked = False
        assert rigol_ds1000.system_locked is False

    @pytest.mark.parametrize("setting", ["LAT", "DEF"])
    def test_system_power_on_setting(self, rigol_ds1000, setting):
        rigol_ds1000.system_power_on_setting = setting
        assert rigol_ds1000.system_power_on_setting == setting

    def test_system_gam(self, rigol_ds1000):
        gam = rigol_ds1000.system_gam
        assert isinstance(gam, (int, float))

    def test_system_ram(self, rigol_ds1000):
        ram = rigol_ds1000.system_ram
        assert isinstance(ram, (int, float))

    def test_system_language(self, rigol_ds1000):
        """Set English, verify, then restore."""
        rigol_ds1000.system_language = "ENGL"
        assert rigol_ds1000.system_language == "ENGL"


# ---------------------------------------------------------------------------
# Logic Analyzer Subsystem (MSO models only)
# ---------------------------------------------------------------------------
@pytest.mark.mso_only
class TestLASubsystem:
    """Test the logic analyzer subsystem.

    Only available on MSO1074Z, MSO1104Z, and -S variants.
    Skip on DS-only models:  pytest -m 'not mso_only'
    """

    def test_la_state(self, rigol_ds1000):
        rigol_ds1000.la_state = True
        assert rigol_ds1000.la_state is True
        rigol_ds1000.la_state = False
        assert rigol_ds1000.la_state is False

    @pytest.mark.parametrize("size", ["SMAL", "LARG"])
    def test_la_size(self, rigol_ds1000, size):
        rigol_ds1000.la_state = True
        rigol_ds1000.la_size = size
        assert rigol_ds1000.la_size == size

    def test_la_pod1_display(self, rigol_ds1000):
        rigol_ds1000.la_state = True
        rigol_ds1000.la_pod1_display = True
        assert rigol_ds1000.la_pod1_display is True
        rigol_ds1000.la_pod1_display = False
        assert rigol_ds1000.la_pod1_display is False

    def test_la_pod1_threshold(self, rigol_ds1000):
        rigol_ds1000.la_state = True
        rigol_ds1000.la_pod1_threshold = 1.5
        assert rigol_ds1000.la_pod1_threshold == pytest.approx(1.5, rel=0.01)

    def test_la_pod2_display(self, rigol_ds1000):
        rigol_ds1000.la_state = True
        rigol_ds1000.la_pod2_display = True
        assert rigol_ds1000.la_pod2_display is True
        rigol_ds1000.la_pod2_display = False
        assert rigol_ds1000.la_pod2_display is False

    def test_la_pod2_threshold(self, rigol_ds1000):
        rigol_ds1000.la_state = True
        rigol_ds1000.la_pod2_threshold = 1.5
        assert rigol_ds1000.la_pod2_threshold == pytest.approx(1.5, rel=0.01)

    def test_la_time_calibration(self, rigol_ds1000):
        rigol_ds1000.la_state = True
        rigol_ds1000.la_time_calibration = 0.0
        assert rigol_ds1000.la_time_calibration == pytest.approx(0.0, abs=1e-11)

    @pytest.mark.parametrize("channel", [0, 1, 7, 8, 15])
    def test_la_digital_display(self, rigol_ds1000, channel):
        rigol_ds1000.la_state = True
        rigol_ds1000.la_digital_display(channel, True)
        assert rigol_ds1000.la_digital_display_get(channel) is True
        rigol_ds1000.la_digital_display(channel, False)
        assert rigol_ds1000.la_digital_display_get(channel) is False

    @pytest.mark.parametrize("channel", [0, 7])
    def test_la_digital_label(self, rigol_ds1000, channel):
        rigol_ds1000.la_state = True
        rigol_ds1000.la_digital_label(channel, "CLK")
        label = rigol_ds1000.la_digital_label_get(channel)
        assert isinstance(label, str)


# ---------------------------------------------------------------------------
# Reference Waveform Subsystem
# ---------------------------------------------------------------------------
class TestReferenceSubsystem:
    """Test reference waveform functionality."""

    def test_reference_display(self, rigol_ds1000):
        rigol_ds1000.reference_display = True
        assert rigol_ds1000.reference_display is True
        rigol_ds1000.reference_display = False
        assert rigol_ds1000.reference_display is False

    @pytest.mark.parametrize("ref", [1, 2, 3])
    def test_reference_enable(self, rigol_ds1000, ref):
        rigol_ds1000.reference_enable(ref, True)
        assert rigol_ds1000.reference_enable_get(ref) is True
        rigol_ds1000.reference_enable(ref, False)
        assert rigol_ds1000.reference_enable_get(ref) is False

    def test_reference_vscale(self, rigol_ds1000):
        rigol_ds1000.reference_enable(1, True)
        rigol_ds1000.reference_vscale(1, 1.0)
        assert rigol_ds1000.reference_vscale_get(1) == pytest.approx(1.0, rel=0.01)
        rigol_ds1000.reference_enable(1, False)

    def test_reference_voffset(self, rigol_ds1000):
        rigol_ds1000.reference_enable(1, True)
        rigol_ds1000.reference_voffset(1, 0.0)
        assert rigol_ds1000.reference_voffset_get(1) == pytest.approx(0.0, abs=0.01)
        rigol_ds1000.reference_enable(1, False)

    @pytest.mark.parametrize("color", ["GRAY", "GREE", "LBLU", "MAGE", "ORAN"])
    def test_reference_color(self, rigol_ds1000, color):
        rigol_ds1000.reference_enable(1, True)
        rigol_ds1000.reference_color(1, color)
        result = rigol_ds1000.reference_color_get(1)
        assert isinstance(result, str)
        rigol_ds1000.reference_enable(1, False)

    def test_reference_source(self, rigol_ds1000):
        _ensure_channel_enabled(rigol_ds1000, 1)
        rigol_ds1000.reference_enable(1, True)
        rigol_ds1000.reference_source(1, "CHAN1")
        assert rigol_ds1000.reference_source_get(1) == "CHAN1"
        rigol_ds1000.reference_enable(1, False)


# ---------------------------------------------------------------------------
# Calibration Subsystem
# ---------------------------------------------------------------------------
class TestCalibrationSubsystem:
    """Test every command and property in the Calibration subsystem."""

    @pytest.mark.device_error_warning
    def test_calibrate(self, rigol_ds1000):
        rigol_ds1000.cal_start()
        sleep(5)  # Wait short time

    @pytest.mark.device_error_warning
    def test_stop_calibrate(self, rigol_ds1000):
        """Stop calibration and check for errors.

        Does not work reliably - the device sometimes returns a timeout error (VI_ERROR_TMO) when checking for errors after calibration, even though the calibration completes successfully. Especially, when connected via LAN.
        """
        rigol_ds1000.cal_stop()
        sleep(2)  # Wait short time


# ---------------------------------------------------------------------------
# Waveform Record Subsystem (Optional feature)
# ---------------------------------------------------------------------------
@pytest.mark.optional
class TestWaveformRecord:
    """Test waveform recording (optional feature).

    Skip if the device does not have the waveform record option:
        pytest -m 'not optional'
    """

    def test_wrecord_enable(self, rigol_ds1000):
        rigol_ds1000.wrecord_enable = True
        assert rigol_ds1000.wrecord_enable is True
        rigol_ds1000.wrecord_enable = False
        assert rigol_ds1000.wrecord_enable is False

    def test_wrecord_end_frame(self, rigol_ds1000):
        rigol_ds1000.wrecord_enable = True
        rigol_ds1000.wrecord_end_frame = 100
        assert rigol_ds1000.wrecord_end_frame == 100
        rigol_ds1000.wrecord_enable = False

    def test_wrecord_max_frames(self, rigol_ds1000):
        max_frames = rigol_ds1000.wrecord_max_frames
        assert isinstance(max_frames, (int, float))

    def test_wrecord_interval(self, rigol_ds1000):
        rigol_ds1000.wrecord_enable = True
        rigol_ds1000.wrecord_interval = 1e-3
        assert rigol_ds1000.wrecord_interval == pytest.approx(1e-3, rel=0.01)
        rigol_ds1000.wrecord_enable = False

    def test_wrecord_prompt(self, rigol_ds1000):
        rigol_ds1000.wrecord_enable = True
        rigol_ds1000.wrecord_prompt = True
        assert rigol_ds1000.wrecord_prompt is True
        rigol_ds1000.wrecord_prompt = False
        rigol_ds1000.wrecord_enable = False

    @pytest.mark.parametrize("op", ["RUN", "STOP"])
    def test_wrecord_operate(self, rigol_ds1000, op):
        rigol_ds1000.wrecord_enable = True
        rigol_ds1000.wrecord_operate = op
        assert rigol_ds1000.wrecord_operate == op
        rigol_ds1000.wrecord_operate = "STOP"
        rigol_ds1000.wrecord_enable = False


# ---------------------------------------------------------------------------
# Waveform Replay Subsystem (Optional feature)
# ---------------------------------------------------------------------------
@pytest.mark.optional
class TestWaveformReplay:
    """Test waveform replay (optional feature, requires recorded frames).

    Skip if the device does not have the waveform record/replay option.
    """

    def test_wreplay_start_end_frame(self, rigol_ds1000):
        rigol_ds1000.wreplay_start_frame = 1
        assert rigol_ds1000.wreplay_start_frame == 1
        rigol_ds1000.wreplay_end_frame = 10
        assert rigol_ds1000.wreplay_end_frame == 10

    def test_wreplay_max_frames(self, rigol_ds1000):
        max_frames = rigol_ds1000.wreplay_max_frames
        assert isinstance(max_frames, (int, float))

    def test_wreplay_interval(self, rigol_ds1000):
        rigol_ds1000.wreplay_interval = 1e-3
        assert rigol_ds1000.wreplay_interval == pytest.approx(1e-3, rel=0.01)

    @pytest.mark.parametrize("mode", ["REP", "SING"])
    def test_wreplay_mode(self, rigol_ds1000, mode):
        rigol_ds1000.wreplay_mode = mode
        assert rigol_ds1000.wreplay_mode == mode

    @pytest.mark.parametrize("direction", ["FORW", "BACK"])
    def test_wreplay_direction(self, rigol_ds1000, direction):
        rigol_ds1000.wreplay_direction = direction
        assert rigol_ds1000.wreplay_direction == direction

    @pytest.mark.parametrize("op", ["PLAY", "PAUS", "STOP"])
    def test_wreplay_operate(self, rigol_ds1000, op):
        rigol_ds1000.wreplay_operate = op
        assert rigol_ds1000.wreplay_operate == op
        rigol_ds1000.wreplay_operate = "STOP"


# ---------------------------------------------------------------------------
# Source / Function Generator Subsystem (Optional, -S models only)
# ---------------------------------------------------------------------------
@pytest.mark.optional
class TestSourceSubsystem:
    """Test the built-in function generator (optional, DS1xxxx-S models only).

    Skip if the device does not have the source option:
        pytest -m 'not optional'
    """

    def test_source_output(self, rigol_ds1000):
        rigol_ds1000.source_output = True
        assert rigol_ds1000.source_output is True
        rigol_ds1000.source_output = False
        assert rigol_ds1000.source_output is False

    @pytest.mark.parametrize("function", ["SIN", "SQU", "RAMP", "PULS", "NOIS", "DC"])
    def test_source_function(self, rigol_ds1000, function):
        rigol_ds1000.source_function = function
        assert rigol_ds1000.source_function == function

    @pytest.mark.parametrize("freq", [100.0, 1e3, 10e3, 100e3])
    def test_source_frequency(self, rigol_ds1000, freq):
        rigol_ds1000.source_function = "SIN"
        rigol_ds1000.source_frequency = freq
        assert rigol_ds1000.source_frequency == pytest.approx(freq, rel=0.01)

    def test_source_voltage(self, rigol_ds1000):
        rigol_ds1000.source_function = "SIN"
        rigol_ds1000.source_voltage = 1.0
        assert rigol_ds1000.source_voltage == pytest.approx(1.0, rel=0.01)

    def test_source_voltage_offset(self, rigol_ds1000):
        rigol_ds1000.source_voltage_offset = 0.0
        assert rigol_ds1000.source_voltage_offset == pytest.approx(0.0, abs=0.01)

    def test_source_phase(self, rigol_ds1000):
        rigol_ds1000.source_phase = 90.0
        assert rigol_ds1000.source_phase == pytest.approx(90.0, rel=0.01)
        rigol_ds1000.source_phase = 0.0  # Reset

    @pytest.mark.parametrize("impedance", ["OMEG", "FIFT"])
    def test_source_impedance(self, rigol_ds1000, impedance):
        rigol_ds1000.source_impedance = impedance
        assert rigol_ds1000.source_impedance == impedance

    def test_source_ramp_symmetry(self, rigol_ds1000):
        rigol_ds1000.source_function = "RAMP"
        rigol_ds1000.source_ramp_symmetry = 50.0
        assert rigol_ds1000.source_ramp_symmetry == pytest.approx(50.0, rel=0.01)

    def test_source_pulse_duty(self, rigol_ds1000):
        rigol_ds1000.source_function = "PULS"
        rigol_ds1000.source_pulse_duty = 50.0
        assert rigol_ds1000.source_pulse_duty == pytest.approx(50.0, rel=0.01)

    def test_source_mod_state(self, rigol_ds1000):
        rigol_ds1000.source_function = "SIN"
        rigol_ds1000.source_mod_state = True
        assert rigol_ds1000.source_mod_state is True
        rigol_ds1000.source_mod_state = False

    @pytest.mark.parametrize("mod_type", ["AM", "FM"])
    def test_source_mod_type(self, rigol_ds1000, mod_type):
        rigol_ds1000.source_function = "SIN"
        rigol_ds1000.source_mod_state = True
        rigol_ds1000.source_mod_type = mod_type
        assert rigol_ds1000.source_mod_type == mod_type
        rigol_ds1000.source_mod_state = False

    def test_source_mod_am(self, rigol_ds1000):
        rigol_ds1000.source_function = "SIN"
        rigol_ds1000.source_mod_state = True
        rigol_ds1000.source_mod_type = "AM"
        rigol_ds1000.source_mod_am_depth = 50.0
        assert rigol_ds1000.source_mod_am_depth == pytest.approx(50.0, rel=0.01)
        rigol_ds1000.source_mod_am_frequency = 1e3
        assert rigol_ds1000.source_mod_am_frequency == pytest.approx(1e3, rel=0.01)
        rigol_ds1000.source_mod_am_function = "SIN"
        assert rigol_ds1000.source_mod_am_function == "SIN"
        rigol_ds1000.source_mod_state = False

    def test_source_mod_fm(self, rigol_ds1000):
        rigol_ds1000.source_function = "SIN"
        rigol_ds1000.source_frequency = 10e3
        rigol_ds1000.source_mod_state = True
        rigol_ds1000.source_mod_type = "FM"
        rigol_ds1000.source_mod_fm_deviation = 1e3
        assert rigol_ds1000.source_mod_fm_deviation == pytest.approx(1e3, rel=0.01)
        rigol_ds1000.source_mod_fm_frequency = 500.0
        assert rigol_ds1000.source_mod_fm_frequency == pytest.approx(500.0, rel=0.01)
        rigol_ds1000.source_mod_fm_function = "SIN"
        assert rigol_ds1000.source_mod_fm_function == "SIN"
        rigol_ds1000.source_mod_state = False

    def test_source_apply_sinusoid(self, rigol_ds1000):
        rigol_ds1000.source_apply_sinusoid(frequency=1e3, amplitude=1.0, offset=0.0, phase=0.0)
        sleep(0.2)
        config = rigol_ds1000.source_apply
        assert config is not None

    def test_source_apply_square(self, rigol_ds1000):
        rigol_ds1000.source_apply_square(frequency=1e3, amplitude=1.0, offset=0.0, phase=0.0)
        sleep(0.2)

    def test_source_apply_ramp(self, rigol_ds1000):
        rigol_ds1000.source_apply_ramp(frequency=1e3, amplitude=1.0, offset=0.0, phase=0.0)
        sleep(0.2)

    def test_source_phase_init(self, rigol_ds1000):
        rigol_ds1000.source_phase_init()

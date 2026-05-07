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

from __future__ import annotations
from typing import Literal, Union
import numpy as np
from numpy.typing import NDArray

from pymeasure.instruments import Instrument, Channel, SCPIMixin
from pymeasure.adapters import Adapter

# ---------------------------------------------------------------------------
# Literal type aliases
# ---------------------------------------------------------------------------

BandwidthType = Literal["OFF", "20M"]
CouplingType = Literal["AC", "DC", "GND"]
UnitsType = Literal["VOLT", "WATT", "AMP", "UNKN"]

ChannelListType = Literal[
    "CHAN1", "CHAN2", "CHAN3", "CHAN4",
    "D0", "D1", "D2", "D3", "D4", "D5", "D6", "D7",
    "D8", "D9", "D10", "D11", "D12", "D13", "D14", "D15",
]
ChannelListExtType = Literal[
    "CHAN1", "CHAN2", "CHAN3", "CHAN4",
    "D0", "D1", "D2", "D3", "D4", "D5", "D6", "D7",
    "D8", "D9", "D10", "D11", "D12", "D13", "D14", "D15",
    "EXT", "EXT5", "ACL",
]
ChannelListMathType = Literal[
    "CHAN1", "CHAN2", "CHAN3", "CHAN4",
    "D0", "D1", "D2", "D3", "D4", "D5", "D6", "D7",
    "D8", "D9", "D10", "D11", "D12", "D13", "D14", "D15",
    "MATH",
]
ChannelListWaveformType = Literal[
    "CHAN1", "CHAN2", "CHAN3", "CHAN4",
    "D0", "D1", "D2", "D3", "D4", "D5", "D6", "D7",
    "D8", "D9", "D10", "D11", "D12", "D13", "D14", "D15",
    "MATH",
    "REF1", "REF2", "REF3", "REF4", "REF5",
    "REF6", "REF7", "REF8", "REF9", "REF10",
]
ChannelListDGroupsType = Literal[
    "D0", "D1", "D2", "D3", "D4", "D5", "D6", "D7",
    "D8", "D9", "D10", "D11", "D12", "D13", "D14", "D15",
    "GRO1", "GRO2", "GRO3", "GRO4", "NONE",
]
ChannelListPlusOffType = Literal[
    "CHAN1", "CHAN2", "CHAN3", "CHAN4",
    "D0", "D1", "D2", "D3", "D4", "D5", "D6", "D7",
    "D8", "D9", "D10", "D11", "D12", "D13", "D14", "D15",
    "OFF",
]
AnalogChannelType = Literal["CHAN1", "CHAN2", "CHAN3", "CHAN4"]
DigitalChannelType = Literal[
    "D0", "D1", "D2", "D3", "D4", "D5", "D6", "D7",
    "D8", "D9", "D10", "D11", "D12", "D13", "D14", "D15",
]

AcqAveragesType = Literal[2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]
AcqMemoryDepthType = Union[
    Literal["AUTO", 3000, 6000, 12000, 30000, 60000, 120000,
            300000, 600000, 1200000, 3000000, 6000000, 12000000, 24000000]
]
AcqModeType = Literal["NORMAL", "AVERAGES", "PEAK", "HRESOLUTION"]

TriggerModeType = Literal[
    "EDGE", "PULS", "RUNT", "WIND", "NEDG", "SLOP",
    "VID", "PATT", "DEL", "TIM", "DUR", "SHOL", "RS232", "IIC", "SPI",
]
TriggerCouplingType = Literal["AC", "DC", "LFR", "HFR"]
TriggerSweepType = Literal["AUTO", "NORM", "SING"]
EdgeSlopeType = Literal["POS", "NEG", "RFAL"]
PosNegType = Literal["POS", "NEG"]
PosNegRfalType = Literal["POS", "NEG", "RFAL"]

WaveformModeType = Literal["NORM", "MAX", "RAW"]
WaveformFormatType = Literal["WORD", "BYTE", "ASC"]

CursorModeType = Literal["OFF", "MAN", "TRAC", "AUTO", "XY"]
CursorTimeUnitType = Literal["S", "HZ", "DEGR", "PERC"]

MathOperatorType = Literal[
    "ADD", "SUBT", "MULT", "DIV", "AND", "OR", "XOR", "NOT",
    "FFT", "INTG", "DIFF", "SQRT", "LOG", "LN", "EXP", "ABS", "FILT", "SMO",
]
FftWindowType = Literal["RECT", "BLAC", "HANN", "HAMM", "FLAT", "TRI"]
FilterTypeType = Literal["LPAS", "HPAS", "BPAS", "BST"]

SourceFunctionType = Literal[
    "SIN", "SQU", "RAMP", "PULS", "NOIS", "DC",
    "SINC", "EXPR", "EXPF", "ECG", "GAUS", "LOR", "HAV",
]
SystemLanguageType = Literal["SCH", "TCH", "ENGL", "PORT", "GERM", "POL", "KOR", "JAPA", "FREN", "RUSS"]
StorageImageType = Literal["PNG", "BMP8", "BMP24", "JPEG", "TIFF"]
DecoderModeType = Literal["PAR", "UART", "SPI", "IIC"]
DecoderFormatType = Literal["HEX", "ASC", "DEC", "BIN", "LINE"]
EventTableFormatType = Literal["HEX", "ASC", "DEC"]


class OscilloscopeChannel(Channel):
    """Represents a single channel of the Rigol DS1000Z oscilloscope."""

    def __init__(self, parent: Instrument, id: str, **kwargs) -> None: ...

    @property
    def bandwidth(self) -> BandwidthType:
        """Control the bandwidth limit of the channel (OFF or 20M)."""
        ...

    @bandwidth.setter
    def bandwidth(self, _value: BandwidthType) -> None: ...

    @property
    def coupling(self) -> CouplingType:
        """Control the coupling mode of the channel (AC, DC, or GND)."""
        ...

    @coupling.setter
    def coupling(self, _value: CouplingType) -> None: ...

    @property
    def is_enabled(self) -> bool:
        """Control if the channel is enabled (bool)."""
        ...

    @is_enabled.setter
    def is_enabled(self, _value: bool) -> None: ...

    @property
    def is_inverted(self) -> bool:
        """Control if the waveform of the channel is inverted (bool)."""
        ...

    @is_inverted.setter
    def is_inverted(self, _value: bool) -> None: ...

    @property
    def offset(self) -> float:
        """Control the vertical offset of the channel in volts (float)."""
        ...

    @offset.setter
    def offset(self, _value: float) -> None: ...

    @property
    def range(self) -> float:
        """Control the vertical range of the channel in volts (float)."""
        ...

    @range.setter
    def range(self, _value: float) -> None: ...

    @property
    def delay_calibration(self) -> float:
        """Control the delay calibration time of the channel in seconds (float)."""
        ...

    @delay_calibration.setter
    def delay_calibration(self, _value: float) -> None: ...

    @property
    def scale(self) -> float:
        """Control the vertical scale of the channel in volts per division (float)."""
        ...

    @scale.setter
    def scale(self, _value: float) -> None: ...

    @property
    def probe_ratio(self) -> float:
        """Control the probe attenuation ratio of the channel (float)."""
        ...

    @probe_ratio.setter
    def probe_ratio(self, _value: float) -> None: ...

    @property
    def units(self) -> UnitsType:
        """Control the amplitude display units of the channel."""
        ...

    @units.setter
    def units(self, _value: UnitsType) -> None: ...

    @property
    def vernier_enabled(self) -> bool:
        """Control if fine adjustment (vernier) is enabled for the channel (bool)."""
        ...

    @vernier_enabled.setter
    def vernier_enabled(self, _value: bool) -> None: ...


class RigolDS1000ZSeries(SCPIMixin, Instrument):
    """Represents the Rigol DS1000Z series of oscilloscopes.

    Supports DS1054Z, DS1074Z, DS1104Z, DS1074Z-S, DS1104Z-S,
    MSO1074Z, MSO1104Z, MSO1074Z-S, MSO1104Z-S and Plus variants.

    Args:
        adapter: A PyVISA resource name or adapter instance.
        name: Name of the instrument instance.
        kwargs: Additional keyword arguments passed to the parent Instrument class.

    Example::

        scope = RigolDS1000ZSeries("TCPIP::192.168.1.100::INSTR")
        scope.ch1.scale = 1.0
        scope.ch1.coupling = "DC"
        scope.timebase_scale = 1e-3
        scope.run()
    """

    ch1: OscilloscopeChannel
    ch2: OscilloscopeChannel
    ch3: OscilloscopeChannel
    ch4: OscilloscopeChannel

    def __init__(
        self, adapter: Adapter | str, name: str = "Rigol DS1000Z Series", **kwargs
    ) -> None: ...

    # ------------------------------------------------------------------
    # Basic control methods
    # ------------------------------------------------------------------

    def autoscale(self) -> None:
        """Set the waveform auto setting."""
        ...

    def run(self) -> None:
        """Set the oscilloscope to run mode."""
        ...

    def stop(self) -> None:
        """Set the oscilloscope to stop mode."""
        ...

    def force_trigger(self) -> None:
        """Force a trigger event."""
        ...

    def clear_registers(self) -> None:
        """Clear the status registers of the oscilloscope."""
        ...

    def cal_start(self) -> None:
        """Start the oscilloscope self-calibration process."""
        ...

    def cal_stop(self) -> None:
        """Stop the oscilloscope self-calibration process."""
        ...

    # ------------------------------------------------------------------
    # Acquire Subsystem
    # ------------------------------------------------------------------

    @property
    def acq_averages(self) -> AcqAveragesType:
        """Control the number of averages used in acquisition (int, 2^n with n=1..10)."""
        ...

    @acq_averages.setter
    def acq_averages(self, _value: AcqAveragesType) -> None: ...

    @property
    def acq_memory_depth(self) -> AcqMemoryDepthType:
        """Control the memory depth of the acquisition (int or 'AUTO')."""
        ...

    @acq_memory_depth.setter
    def acq_memory_depth(self, _value: AcqMemoryDepthType) -> None: ...

    @property
    def acq_mode(self) -> AcqModeType:
        """Control the acquisition mode (NORMAL, AVERAGES, PEAK, or HRESOLUTION)."""
        ...

    @acq_mode.setter
    def acq_mode(self, _value: AcqModeType) -> None: ...

    @property
    def acq_sample_rate(self) -> float:
        """Get the current sample rate in Samples/s (read-only)."""
        ...

    # ------------------------------------------------------------------
    # Timebase Subsystem
    # ------------------------------------------------------------------

    @property
    def timebase_offset(self) -> float:
        """Control the timebase offset (delay) in seconds (float)."""
        ...

    @timebase_offset.setter
    def timebase_offset(self, _value: float) -> None: ...

    @property
    def timebase_scale(self) -> float:
        """Control the timebase scale in seconds per division (float)."""
        ...

    @timebase_scale.setter
    def timebase_scale(self, _value: float) -> None: ...

    @property
    def timebase_mode(self) -> Literal["MAIN", "XY", "ROLL"]:
        """Control the timebase mode (MAIN, XY, or ROLL)."""
        ...

    @timebase_mode.setter
    def timebase_mode(self, _value: Literal["MAIN", "XY", "ROLL"]) -> None: ...

    @property
    def timebase_delay_enabled(self) -> bool:
        """Control if the delayed timebase is enabled (bool)."""
        ...

    @timebase_delay_enabled.setter
    def timebase_delay_enabled(self, _value: bool) -> None: ...

    @property
    def timebase_delay_offset(self) -> float:
        """Control the delayed timebase offset in seconds (float)."""
        ...

    @timebase_delay_offset.setter
    def timebase_delay_offset(self, _value: float) -> None: ...

    @property
    def timebase_delay_scale(self) -> float:
        """Control the delayed timebase scale in seconds per division (float)."""
        ...

    @timebase_delay_scale.setter
    def timebase_delay_scale(self, _value: float) -> None: ...

    # ------------------------------------------------------------------
    # Trigger Subsystem - Common
    # ------------------------------------------------------------------

    @property
    def trigger_mode(self) -> TriggerModeType:
        """Control the trigger mode."""
        ...

    @trigger_mode.setter
    def trigger_mode(self, _value: TriggerModeType) -> None: ...

    @property
    def trigger_coupling(self) -> TriggerCouplingType:
        """Control the trigger coupling mode (AC, DC, LFR, or HFR)."""
        ...

    @trigger_coupling.setter
    def trigger_coupling(self, _value: TriggerCouplingType) -> None: ...

    @property
    def trigger_status(self) -> str:
        """Get the current trigger status (TD, WAIT, RUN, AUTO, or STOP, read-only)."""
        ...

    @property
    def trigger_sweep(self) -> TriggerSweepType:
        """Control the trigger sweep mode (AUTO, NORM, or SING)."""
        ...

    @trigger_sweep.setter
    def trigger_sweep(self, _value: TriggerSweepType) -> None: ...

    @property
    def trigger_holdoff(self) -> float:
        """Control the trigger holdoff time in seconds (float)."""
        ...

    @trigger_holdoff.setter
    def trigger_holdoff(self, _value: float) -> None: ...

    @property
    def trigger_noise_reject(self) -> bool:
        """Control if trigger noise rejection is enabled (bool)."""
        ...

    @trigger_noise_reject.setter
    def trigger_noise_reject(self, _value: bool) -> None: ...

    # -- Edge Trigger --

    @property
    def trigger_edge_source(self) -> ChannelListExtType:
        """Control the edge trigger source."""
        ...

    @trigger_edge_source.setter
    def trigger_edge_source(self, _value: ChannelListExtType) -> None: ...

    @property
    def trigger_edge_slope(self) -> EdgeSlopeType:
        """Control the edge trigger slope (POS, NEG, or RFAL)."""
        ...

    @trigger_edge_slope.setter
    def trigger_edge_slope(self, _value: EdgeSlopeType) -> None: ...

    @property
    def trigger_edge_level(self) -> float:
        """Control the edge trigger level in volts (float)."""
        ...

    @trigger_edge_level.setter
    def trigger_edge_level(self, _value: float) -> None: ...

    # -- Pulse Trigger --

    @property
    def trigger_pulse_source(self) -> ChannelListType:
        """Control the pulse trigger source."""
        ...

    @trigger_pulse_source.setter
    def trigger_pulse_source(self, _value: ChannelListType) -> None: ...

    @property
    def trigger_pulse_when(self) -> Literal["PGR", "PLES", "PGL"]:
        """Control the pulse width condition for triggering."""
        ...

    @trigger_pulse_when.setter
    def trigger_pulse_when(self, _value: Literal["PGR", "PLES", "PGL"]) -> None: ...

    @property
    def trigger_pulse_width(self) -> float:
        """Control the pulse width for trigger in seconds (float)."""
        ...

    @trigger_pulse_width.setter
    def trigger_pulse_width(self, _value: float) -> None: ...

    @property
    def trigger_pulse_upper_width(self) -> float:
        """Control the upper pulse width limit in seconds (float)."""
        ...

    @trigger_pulse_upper_width.setter
    def trigger_pulse_upper_width(self, _value: float) -> None: ...

    @property
    def trigger_pulse_lower_width(self) -> float:
        """Control the lower pulse width limit in seconds (float)."""
        ...

    @trigger_pulse_lower_width.setter
    def trigger_pulse_lower_width(self, _value: float) -> None: ...

    @property
    def trigger_pulse_level(self) -> float:
        """Control the pulse trigger threshold level in volts (float)."""
        ...

    @trigger_pulse_level.setter
    def trigger_pulse_level(self, _value: float) -> None: ...

    # -- Slope Trigger --

    @property
    def trigger_slope_source(self) -> AnalogChannelType:
        """Control the slope trigger source (CHANnel1-4)."""
        ...

    @trigger_slope_source.setter
    def trigger_slope_source(self, _value: AnalogChannelType) -> None: ...

    @property
    def trigger_slope_when(self) -> Literal["PGR", "PLES", "PGL", "NGR", "NLES", "NGL"]:
        """Control the slope time condition for triggering."""
        ...

    @trigger_slope_when.setter
    def trigger_slope_when(self, _value: Literal["PGR", "PLES", "PGL", "NGR", "NLES", "NGL"]) -> None: ...

    @property
    def trigger_slope_time(self) -> float:
        """Control the slope time for trigger in seconds (float)."""
        ...

    @trigger_slope_time.setter
    def trigger_slope_time(self, _value: float) -> None: ...

    @property
    def trigger_slope_time_upper(self) -> float:
        """Control the upper slope time limit in seconds (float)."""
        ...

    @trigger_slope_time_upper.setter
    def trigger_slope_time_upper(self, _value: float) -> None: ...

    @property
    def trigger_slope_time_lower(self) -> float:
        """Control the lower slope time limit in seconds (float)."""
        ...

    @trigger_slope_time_lower.setter
    def trigger_slope_time_lower(self, _value: float) -> None: ...

    @property
    def trigger_slope_window(self) -> Literal["TA", "TB", "TAB"]:
        """Control the slope trigger window type (TA, TB, or TAB)."""
        ...

    @trigger_slope_window.setter
    def trigger_slope_window(self, _value: Literal["TA", "TB", "TAB"]) -> None: ...

    @property
    def trigger_slope_level_a(self) -> float:
        """Control slope trigger level A in volts (float)."""
        ...

    @trigger_slope_level_a.setter
    def trigger_slope_level_a(self, _value: float) -> None: ...

    @property
    def trigger_slope_level_b(self) -> float:
        """Control slope trigger level B in volts (float)."""
        ...

    @trigger_slope_level_b.setter
    def trigger_slope_level_b(self, _value: float) -> None: ...

    # -- Video Trigger --

    @property
    def trigger_video_source(self) -> AnalogChannelType:
        """Control the video trigger source (CHANnel1-4)."""
        ...

    @trigger_video_source.setter
    def trigger_video_source(self, _value: AnalogChannelType) -> None: ...

    @property
    def trigger_video_polarity(self) -> PosNegType:
        """Control the video sync polarity (POS or NEG)."""
        ...

    @trigger_video_polarity.setter
    def trigger_video_polarity(self, _value: PosNegType) -> None: ...

    @property
    def trigger_video_mode(self) -> Literal["ODDF", "EVEN", "LINE", "ALIN"]:
        """Control the video trigger mode."""
        ...

    @trigger_video_mode.setter
    def trigger_video_mode(self, _value: Literal["ODDF", "EVEN", "LINE", "ALIN"]) -> None: ...

    @property
    def trigger_video_line(self) -> int:
        """Control the video line number for triggering (int)."""
        ...

    @trigger_video_line.setter
    def trigger_video_line(self, _value: int) -> None: ...

    @property
    def trigger_video_standard(self) -> Literal["PALS", "NTSC", "480P", "576P"]:
        """Control the video standard."""
        ...

    @trigger_video_standard.setter
    def trigger_video_standard(self, _value: Literal["PALS", "NTSC", "480P", "576P"]) -> None: ...

    @property
    def trigger_video_level(self) -> float:
        """Control the video trigger level in volts (float)."""
        ...

    @trigger_video_level.setter
    def trigger_video_level(self, _value: float) -> None: ...

    # -- Pattern Trigger --

    @property
    def trigger_pattern_pattern(self) -> Literal["H", "L", "X", "R", "F"]:
        """Control the pattern for pattern triggering."""
        ...

    @trigger_pattern_pattern.setter
    def trigger_pattern_pattern(self, _value: Literal["H", "L", "X", "R", "F"]) -> None: ...

    @property
    def trigger_pattern_level(self) -> float:
        """Control the threshold level for a specific channel in pattern trigger (float)."""
        ...

    @trigger_pattern_level.setter
    def trigger_pattern_level(self, _value: float) -> None: ...

    # -- Duration Trigger --

    @property
    def trigger_duration_source(self) -> ChannelListType:
        """Control the duration trigger source."""
        ...

    @trigger_duration_source.setter
    def trigger_duration_source(self, _value: ChannelListType) -> None: ...

    @property
    def trigger_duration_type(self) -> Literal["PGR", "PLES", "PGL", "NGR", "NLES", "NGL"]:
        """Control the duration trigger polarity type."""
        ...

    @trigger_duration_type.setter
    def trigger_duration_type(self, _value: Literal["PGR", "PLES", "PGL", "NGR", "NLES", "NGL"]) -> None: ...

    @property
    def trigger_duration_when(self) -> Literal["TIME", "TIM"]:
        """Control when to trigger on duration (TIME or TIM)."""
        ...

    @trigger_duration_when.setter
    def trigger_duration_when(self, _value: Literal["TIME", "TIM"]) -> None: ...

    @property
    def trigger_duration_time_upper(self) -> float:
        """Control the upper duration time limit in seconds (float)."""
        ...

    @trigger_duration_time_upper.setter
    def trigger_duration_time_upper(self, _value: float) -> None: ...

    @property
    def trigger_duration_time_lower(self) -> float:
        """Control the lower duration time limit in seconds (float)."""
        ...

    @trigger_duration_time_lower.setter
    def trigger_duration_time_lower(self, _value: float) -> None: ...

    # -- Timeout Trigger --

    @property
    def trigger_timeout_source(self) -> ChannelListType:
        """Control the timeout trigger source."""
        ...

    @trigger_timeout_source.setter
    def trigger_timeout_source(self, _value: ChannelListType) -> None: ...

    @property
    def trigger_timeout_slope(self) -> PosNegRfalType:
        """Control the edge slope for timeout trigger."""
        ...

    @trigger_timeout_slope.setter
    def trigger_timeout_slope(self, _value: PosNegRfalType) -> None: ...

    @property
    def trigger_timeout_time(self) -> float:
        """Control the timeout time in seconds (float)."""
        ...

    @trigger_timeout_time.setter
    def trigger_timeout_time(self, _value: float) -> None: ...

    # -- Runt Trigger --

    @property
    def trigger_runt_source(self) -> AnalogChannelType:
        """Control the runt trigger source (CHANnel1-4)."""
        ...

    @trigger_runt_source.setter
    def trigger_runt_source(self, _value: AnalogChannelType) -> None: ...

    @property
    def trigger_runt_polarity(self) -> PosNegType:
        """Control the runt pulse polarity (POS or NEG)."""
        ...

    @trigger_runt_polarity.setter
    def trigger_runt_polarity(self, _value: PosNegType) -> None: ...

    @property
    def trigger_runt_when(self) -> Literal["NONE", "PGR", "PLES", "PGL"]:
        """Control the runt time qualifying condition."""
        ...

    @trigger_runt_when.setter
    def trigger_runt_when(self, _value: Literal["NONE", "PGR", "PLES", "PGL"]) -> None: ...

    @property
    def trigger_runt_width(self) -> float:
        """Control the runt pulse width for time qualification in seconds (float)."""
        ...

    @trigger_runt_width.setter
    def trigger_runt_width(self, _value: float) -> None: ...

    @property
    def trigger_runt_upper_width(self) -> float:
        """Control the upper runt width limit in seconds (float)."""
        ...

    @trigger_runt_upper_width.setter
    def trigger_runt_upper_width(self, _value: float) -> None: ...

    @property
    def trigger_runt_lower_width(self) -> float:
        """Control the lower runt width limit in seconds (float)."""
        ...

    @trigger_runt_lower_width.setter
    def trigger_runt_lower_width(self, _value: float) -> None: ...

    @property
    def trigger_runt_level_upper(self) -> float:
        """Control the upper threshold level for runt trigger in volts (float)."""
        ...

    @trigger_runt_level_upper.setter
    def trigger_runt_level_upper(self, _value: float) -> None: ...

    @property
    def trigger_runt_level_lower(self) -> float:
        """Control the lower threshold level for runt trigger in volts (float)."""
        ...

    @trigger_runt_level_lower.setter
    def trigger_runt_level_lower(self, _value: float) -> None: ...

    # -- Windows Trigger --

    @property
    def trigger_windows_source(self) -> AnalogChannelType:
        """Control the windows trigger source (CHANnel1-4)."""
        ...

    @trigger_windows_source.setter
    def trigger_windows_source(self, _value: AnalogChannelType) -> None: ...

    @property
    def trigger_windows_slope(self) -> PosNegRfalType:
        """Control the windows trigger slope condition."""
        ...

    @trigger_windows_slope.setter
    def trigger_windows_slope(self, _value: PosNegRfalType) -> None: ...

    @property
    def trigger_windows_position(self) -> Literal["EXIT", "ENTER", "TIM"]:
        """Control the windows position condition (EXIT, ENTER, or TIM)."""
        ...

    @trigger_windows_position.setter
    def trigger_windows_position(self, _value: Literal["EXIT", "ENTER", "TIM"]) -> None: ...

    @property
    def trigger_windows_time(self) -> float:
        """Control the time qualification for windows trigger in seconds (float)."""
        ...

    @trigger_windows_time.setter
    def trigger_windows_time(self, _value: float) -> None: ...

    @property
    def trigger_windows_level_upper(self) -> float:
        """Control the upper window threshold level in volts (float)."""
        ...

    @trigger_windows_level_upper.setter
    def trigger_windows_level_upper(self, _value: float) -> None: ...

    @property
    def trigger_windows_level_lower(self) -> float:
        """Control the lower window threshold level in volts (float)."""
        ...

    @trigger_windows_level_lower.setter
    def trigger_windows_level_lower(self, _value: float) -> None: ...

    # -- Delay Trigger --

    @property
    def trigger_delay_source_a(self) -> ChannelListType:
        """Control source A for delay trigger."""
        ...

    @trigger_delay_source_a.setter
    def trigger_delay_source_a(self, _value: ChannelListType) -> None: ...

    @property
    def trigger_delay_source_b(self) -> ChannelListType:
        """Control source B for delay trigger."""
        ...

    @trigger_delay_source_b.setter
    def trigger_delay_source_b(self, _value: ChannelListType) -> None: ...

    @property
    def trigger_delay_slope_a(self) -> PosNegType:
        """Control the edge slope for source A in delay trigger (POS or NEG)."""
        ...

    @trigger_delay_slope_a.setter
    def trigger_delay_slope_a(self, _value: PosNegType) -> None: ...

    @property
    def trigger_delay_slope_b(self) -> PosNegType:
        """Control the edge slope for source B in delay trigger (POS or NEG)."""
        ...

    @trigger_delay_slope_b.setter
    def trigger_delay_slope_b(self, _value: PosNegType) -> None: ...

    @property
    def trigger_delay_type(self) -> Literal["GRE", "LESS", "GLES", "GOUT"]:
        """Control the delay type condition."""
        ...

    @trigger_delay_type.setter
    def trigger_delay_type(self, _value: Literal["GRE", "LESS", "GLES", "GOUT"]) -> None: ...

    @property
    def trigger_delay_time_upper(self) -> float:
        """Control the upper delay time limit in seconds (float)."""
        ...

    @trigger_delay_time_upper.setter
    def trigger_delay_time_upper(self, _value: float) -> None: ...

    @property
    def trigger_delay_time_lower(self) -> float:
        """Control the lower delay time limit in seconds (float)."""
        ...

    @trigger_delay_time_lower.setter
    def trigger_delay_time_lower(self, _value: float) -> None: ...

    # -- Setup/Hold Trigger --

    @property
    def trigger_shol_data_source(self) -> ChannelListType:
        """Control the data source for setup/hold trigger."""
        ...

    @trigger_shol_data_source.setter
    def trigger_shol_data_source(self, _value: ChannelListType) -> None: ...

    @property
    def trigger_shol_clock_source(self) -> ChannelListType:
        """Control the clock source for setup/hold trigger."""
        ...

    @trigger_shol_clock_source.setter
    def trigger_shol_clock_source(self, _value: ChannelListType) -> None: ...

    @property
    def trigger_shol_slope(self) -> PosNegType:
        """Control the clock edge slope for setup/hold trigger (POS or NEG)."""
        ...

    @trigger_shol_slope.setter
    def trigger_shol_slope(self, _value: PosNegType) -> None: ...

    @property
    def trigger_shol_pattern(self) -> Literal["H", "L"]:
        """Control the data pattern for setup/hold trigger (H or L)."""
        ...

    @trigger_shol_pattern.setter
    def trigger_shol_pattern(self, _value: Literal["H", "L"]) -> None: ...

    @property
    def trigger_shol_type(self) -> Literal["SET", "HOL", "SETHOL"]:
        """Control the setup/hold type (SET, HOL, or SETHOL)."""
        ...

    @trigger_shol_type.setter
    def trigger_shol_type(self, _value: Literal["SET", "HOL", "SETHOL"]) -> None: ...

    @property
    def trigger_shol_setup_time(self) -> float:
        """Control the setup time in seconds (float)."""
        ...

    @trigger_shol_setup_time.setter
    def trigger_shol_setup_time(self, _value: float) -> None: ...

    @property
    def trigger_shol_hold_time(self) -> float:
        """Control the hold time in seconds (float)."""
        ...

    @trigger_shol_hold_time.setter
    def trigger_shol_hold_time(self, _value: float) -> None: ...

    # -- Nth Edge Trigger --

    @property
    def trigger_nedge_source(self) -> AnalogChannelType:
        """Control the Nth edge trigger source (CHANnel1-4)."""
        ...

    @trigger_nedge_source.setter
    def trigger_nedge_source(self, _value: AnalogChannelType) -> None: ...

    @property
    def trigger_nedge_slope(self) -> PosNegType:
        """Control the edge slope for Nth edge trigger (POS or NEG)."""
        ...

    @trigger_nedge_slope.setter
    def trigger_nedge_slope(self, _value: PosNegType) -> None: ...

    @property
    def trigger_nedge_idle(self) -> float:
        """Control the idle time before edge counting starts in seconds (float)."""
        ...

    @trigger_nedge_idle.setter
    def trigger_nedge_idle(self, _value: float) -> None: ...

    @property
    def trigger_nedge_edge(self) -> int:
        """Control which edge number to trigger on (int, 1-65535)."""
        ...

    @trigger_nedge_edge.setter
    def trigger_nedge_edge(self, _value: int) -> None: ...

    @property
    def trigger_nedge_level(self) -> float:
        """Control the threshold level for Nth edge trigger in volts (float)."""
        ...

    @trigger_nedge_level.setter
    def trigger_nedge_level(self, _value: float) -> None: ...

    # -- RS232 Trigger --

    @property
    def trigger_rs232_source(self) -> ChannelListType:
        """Control the RS232 trigger data source."""
        ...

    @trigger_rs232_source.setter
    def trigger_rs232_source(self, _value: ChannelListType) -> None: ...

    @property
    def trigger_rs232_when(self) -> Literal["STAR", "ERR", "PAR", "DATA"]:
        """Control when to trigger on RS232 data."""
        ...

    @trigger_rs232_when.setter
    def trigger_rs232_when(self, _value: Literal["STAR", "ERR", "PAR", "DATA"]) -> None: ...

    @property
    def trigger_rs232_parity(self) -> Literal["NONE", "EVEN", "ODD"]:
        """Control the RS232 parity mode."""
        ...

    @trigger_rs232_parity.setter
    def trigger_rs232_parity(self, _value: Literal["NONE", "EVEN", "ODD"]) -> None: ...

    @property
    def trigger_rs232_stop_bits(self) -> Literal[1, 2]:
        """Control the number of stop bits in RS232 frame (1 or 2)."""
        ...

    @trigger_rs232_stop_bits.setter
    def trigger_rs232_stop_bits(self, _value: Literal[1, 2]) -> None: ...

    @property
    def trigger_rs232_data_width(self) -> int:
        """Control the length of data in the RS232 trigger frame (int, 0-255)."""
        ...

    @trigger_rs232_data_width.setter
    def trigger_rs232_data_width(self, _value: int) -> None: ...

    @property
    def trigger_rs232_data_bits(self) -> Literal[5, 6, 7, 8]:
        """Control the number of data bits in the RS232 trigger frame."""
        ...

    @trigger_rs232_data_bits.setter
    def trigger_rs232_data_bits(self, _value: Literal[5, 6, 7, 8]) -> None: ...

    @property
    def trigger_rs232_baud(self) -> Union[int, Literal["USER"]]:
        """Control the RS232 baud rate in bps (int or 'USER')."""
        ...

    @trigger_rs232_baud.setter
    def trigger_rs232_baud(self, _value: Union[int, Literal["USER"]]) -> None: ...

    @property
    def trigger_rs232_user_baud(self) -> int:
        """Control the user-defined RS232 baud rate in bps (int, 110-1000000)."""
        ...

    @trigger_rs232_user_baud.setter
    def trigger_rs232_user_baud(self, _value: int) -> None: ...

    @property
    def trigger_rs232_level(self) -> float:
        """Control the RS232 trigger threshold level in volts (float)."""
        ...

    @trigger_rs232_level.setter
    def trigger_rs232_level(self, _value: float) -> None: ...

    # -- I2C Trigger --

    @property
    def trigger_i2c_clock_source(self) -> ChannelListType:
        """Control the I2C clock (SCL) source."""
        ...

    @trigger_i2c_clock_source.setter
    def trigger_i2c_clock_source(self, _value: ChannelListType) -> None: ...

    @property
    def trigger_i2c_data_source(self) -> ChannelListType:
        """Control the I2C data (SDA) source."""
        ...

    @trigger_i2c_data_source.setter
    def trigger_i2c_data_source(self, _value: ChannelListType) -> None: ...

    @property
    def trigger_i2c_when(self) -> Literal["STAR", "REST", "STOP", "NACK", "ADDR", "DATA", "ADAT"]:
        """Control when to trigger on I2C bus."""
        ...

    @trigger_i2c_when.setter
    def trigger_i2c_when(self, _value: Literal["STAR", "REST", "STOP", "NACK", "ADDR", "DATA", "ADAT"]) -> None: ...

    @property
    def trigger_i2c_awidth(self) -> Literal[7, 8, 10]:
        """Control the I2C address width in bits (7, 8, or 10)."""
        ...

    @trigger_i2c_awidth.setter
    def trigger_i2c_awidth(self, _value: Literal[7, 8, 10]) -> None: ...

    @property
    def trigger_i2c_address(self) -> int:
        """Control the I2C address to trigger on (int, 0-1023)."""
        ...

    @trigger_i2c_address.setter
    def trigger_i2c_address(self, _value: int) -> None: ...

    @property
    def trigger_i2c_direction(self) -> Literal["READ", "WRIT", "RWR"]:
        """Control the I2C transfer direction for triggering."""
        ...

    @trigger_i2c_direction.setter
    def trigger_i2c_direction(self, _value: Literal["READ", "WRIT", "RWR"]) -> None: ...

    @property
    def trigger_i2c_data(self) -> int:
        """Control the I2C data value to trigger on (int, 0-2^40-1)."""
        ...

    @trigger_i2c_data.setter
    def trigger_i2c_data(self, _value: int) -> None: ...

    @property
    def trigger_i2c_clock_level(self) -> float:
        """Control the I2C clock (SCL) threshold level in volts (float)."""
        ...

    @trigger_i2c_clock_level.setter
    def trigger_i2c_clock_level(self, _value: float) -> None: ...

    @property
    def trigger_i2c_data_level(self) -> float:
        """Control the I2C data (SDA) threshold level in volts (float)."""
        ...

    @trigger_i2c_data_level.setter
    def trigger_i2c_data_level(self, _value: float) -> None: ...

    # -- SPI Trigger --

    @property
    def trigger_spi_clock_source(self) -> ChannelListType:
        """Control the SPI clock (SCL/SCK) source."""
        ...

    @trigger_spi_clock_source.setter
    def trigger_spi_clock_source(self, _value: ChannelListType) -> None: ...

    @property
    def trigger_spi_data_source(self) -> ChannelListType:
        """Control the SPI data (MOSI/MISO) source."""
        ...

    @trigger_spi_data_source.setter
    def trigger_spi_data_source(self, _value: ChannelListType) -> None: ...

    @property
    def trigger_spi_timeout(self) -> bool:
        """Control if SPI timeout detection is enabled (bool)."""
        ...

    @trigger_spi_timeout.setter
    def trigger_spi_timeout(self, _value: bool) -> None: ...

    @property
    def trigger_spi_when(self) -> Literal["CS", "TIM", "DATA"]:
        """Control when to trigger on SPI bus (CS, TIM, or DATA)."""
        ...

    @trigger_spi_when.setter
    def trigger_spi_when(self, _value: Literal["CS", "TIM", "DATA"]) -> None: ...

    @property
    def trigger_spi_width(self) -> int:
        """Control the SPI data width in bits (int, 4-32)."""
        ...

    @trigger_spi_width.setter
    def trigger_spi_width(self, _value: int) -> None: ...

    @property
    def trigger_spi_data_value(self) -> str:
        """Control the SPI data value to trigger on (hex string)."""
        ...

    @trigger_spi_data_value.setter
    def trigger_spi_data_value(self, _value: str) -> None: ...

    @property
    def trigger_spi_clock_slope(self) -> PosNegType:
        """Control the SPI clock edge for data sampling (POS or NEG)."""
        ...

    @trigger_spi_clock_slope.setter
    def trigger_spi_clock_slope(self, _value: PosNegType) -> None: ...

    @property
    def trigger_spi_cs_source(self) -> ChannelListType:
        """Control the SPI chip select (CS) source."""
        ...

    @trigger_spi_cs_source.setter
    def trigger_spi_cs_source(self, _value: ChannelListType) -> None: ...

    @property
    def trigger_spi_cs_polarity(self) -> PosNegType:
        """Control the SPI chip select polarity (POS active-high, NEG active-low)."""
        ...

    @trigger_spi_cs_polarity.setter
    def trigger_spi_cs_polarity(self, _value: PosNegType) -> None: ...

    @property
    def trigger_spi_clock_level(self) -> float:
        """Control the SPI clock threshold level in volts (float)."""
        ...

    @trigger_spi_clock_level.setter
    def trigger_spi_clock_level(self, _value: float) -> None: ...

    @property
    def trigger_spi_data_level(self) -> float:
        """Control the SPI data threshold level in volts (float)."""
        ...

    @trigger_spi_data_level.setter
    def trigger_spi_data_level(self, _value: float) -> None: ...

    @property
    def trigger_spi_cs_level(self) -> float:
        """Control the SPI chip select threshold level in volts (float)."""
        ...

    @trigger_spi_cs_level.setter
    def trigger_spi_cs_level(self, _value: float) -> None: ...

    # ------------------------------------------------------------------
    # Waveform Subsystem
    # ------------------------------------------------------------------

    @property
    def waveform_source(self) -> ChannelListWaveformType:
        """Control the waveform data source."""
        ...

    @waveform_source.setter
    def waveform_source(self, _value: ChannelListWaveformType) -> None: ...

    @property
    def waveform_mode(self) -> WaveformModeType:
        """Control the waveform reading mode (NORM, MAX, or RAW)."""
        ...

    @waveform_mode.setter
    def waveform_mode(self, _value: WaveformModeType) -> None: ...

    @property
    def waveform_format(self) -> WaveformFormatType:
        """Control the format of waveform data transmission (WORD, BYTE, or ASC)."""
        ...

    @waveform_format.setter
    def waveform_format(self, _value: WaveformFormatType) -> None: ...

    @property
    def waveform_start(self) -> int:
        """Control the starting point for waveform data reading (int)."""
        ...

    @waveform_start.setter
    def waveform_start(self, _value: int) -> None: ...

    @property
    def waveform_stop(self) -> int:
        """Control the stopping point for waveform data reading (int)."""
        ...

    @waveform_stop.setter
    def waveform_stop(self, _value: int) -> None: ...

    @property
    def waveform_xincrement(self) -> float:
        """Get the time difference between two adjacent waveform points in seconds (read-only)."""
        ...

    @property
    def waveform_xorigin(self) -> float:
        """Get the time offset of the first waveform point in seconds (read-only)."""
        ...

    @property
    def waveform_xreference(self) -> float:
        """Get the reference time of the waveform in seconds (read-only)."""
        ...

    @property
    def waveform_yincrement(self) -> float:
        """Get the voltage difference per vertical division in volts (read-only)."""
        ...

    @property
    def waveform_yorigin(self) -> float:
        """Get the voltage offset of the waveform in volts (read-only)."""
        ...

    @property
    def waveform_yreference(self) -> float:
        """Get the reference position in the vertical direction (read-only)."""
        ...

    def get_waveform_preamble(self) -> dict:
        """Get all waveform preamble parameters as a dictionary.

        Returns:
            dict: Keys are format, type, points, count, xincrement, xorigin,
                  xreference, yincrement, yorigin, yreference.
        """
        ...

    def get_waveform_data(self, raw: bool = False) -> NDArray | bytes:
        """Retrieve waveform data from the oscilloscope.

        Args:
            raw: If True, returns raw bytes. If False (default), returns numpy voltage array.

        Returns:
            bytes if raw=True, numpy array of voltages otherwise.
        """
        ...

    # ------------------------------------------------------------------
    # Display Subsystem
    # ------------------------------------------------------------------

    def display_clear(self) -> None:
        """Clear all waveforms on the screen."""
        ...

    @property
    def display_type(self) -> Literal["VECT", "DOTS"]:
        """Control the display connection type for waveform points (VECT or DOTS)."""
        ...

    @display_type.setter
    def display_type(self, _value: Literal["VECT", "DOTS"]) -> None: ...

    @property
    def display_grading_time(self) -> float:
        """Control the persistence time in seconds (float, 0.1-10.0)."""
        ...

    @display_grading_time.setter
    def display_grading_time(self, _value: float) -> None: ...

    @property
    def display_waveform_brightness(self) -> int:
        """Control the waveform brightness as a percentage (int, 0-100)."""
        ...

    @display_waveform_brightness.setter
    def display_waveform_brightness(self, _value: int) -> None: ...

    @property
    def display_grid(self) -> Literal["FULL", "HALF", "NONE"]:
        """Control the grid display mode (FULL, HALF, or NONE)."""
        ...

    @display_grid.setter
    def display_grid(self, _value: Literal["FULL", "HALF", "NONE"]) -> None: ...

    @property
    def display_grid_brightness(self) -> int:
        """Control the grid brightness as a percentage (int, 0-100)."""
        ...

    @display_grid_brightness.setter
    def display_grid_brightness(self, _value: int) -> None: ...

    def get_display_data(self) -> bytes:
        """Retrieve a screenshot of the oscilloscope display as bytes."""
        ...

    # ------------------------------------------------------------------
    # Measurement Subsystem
    # ------------------------------------------------------------------

    @property
    def measure_source(self) -> ChannelListMathType:
        """Control the source for single-item measurements."""
        ...

    @measure_source.setter
    def measure_source(self, _value: ChannelListMathType) -> None: ...

    @property
    def measure_counter_source(self) -> ChannelListType:
        """Control the source for frequency counter measurements."""
        ...

    @measure_counter_source.setter
    def measure_counter_source(self, _value: ChannelListType) -> None: ...

    @property
    def measure_counter_value(self) -> float:
        """Get the frequency counter measurement value in Hz (read-only)."""
        ...

    def measure_clear(self) -> None:
        """Clear all measurements from the display."""
        ...

    def measure_recover(self) -> None:
        """Recover the last cleared measurement."""
        ...

    @property
    def measure_all_display(self) -> bool:
        """Control if all 5 measurement items are displayed simultaneously (bool)."""
        ...

    @measure_all_display.setter
    def measure_all_display(self, _value: bool) -> None: ...

    @property
    def measure_all_source(self) -> ChannelListMathType:
        """Control the source for all-measurement mode."""
        ...

    @measure_all_source.setter
    def measure_all_source(self, _value: ChannelListMathType) -> None: ...

    @property
    def measure_setup_max(self) -> int:
        """Control the upper threshold percentage for measurements (int, 7-95)."""
        ...

    @measure_setup_max.setter
    def measure_setup_max(self, _value: int) -> None: ...

    @property
    def measure_setup_mid(self) -> int:
        """Control the middle threshold percentage for measurements (int, 7-95)."""
        ...

    @measure_setup_mid.setter
    def measure_setup_mid(self, _value: int) -> None: ...

    @property
    def measure_setup_min(self) -> int:
        """Control the lower threshold percentage for measurements (int, 5-93)."""
        ...

    @measure_setup_min.setter
    def measure_setup_min(self, _value: int) -> None: ...

    @property
    def measure_phase_source_a(self) -> AnalogChannelType:
        """Control source A for phase measurements (CHANnel1-4)."""
        ...

    @measure_phase_source_a.setter
    def measure_phase_source_a(self, _value: AnalogChannelType) -> None: ...

    @property
    def measure_phase_source_b(self) -> AnalogChannelType:
        """Control source B for phase measurements (CHANnel1-4)."""
        ...

    @measure_phase_source_b.setter
    def measure_phase_source_b(self, _value: AnalogChannelType) -> None: ...

    @property
    def measure_delay_source_a(self) -> AnalogChannelType:
        """Control source A for delay measurements (CHANnel1-4)."""
        ...

    @measure_delay_source_a.setter
    def measure_delay_source_a(self, _value: AnalogChannelType) -> None: ...

    @property
    def measure_delay_source_b(self) -> AnalogChannelType:
        """Control source B for delay measurements (CHANnel1-4)."""
        ...

    @measure_delay_source_b.setter
    def measure_delay_source_b(self, _value: AnalogChannelType) -> None: ...

    @property
    def measure_statistic_display(self) -> bool:
        """Control if measurement statistics are displayed (bool)."""
        ...

    @measure_statistic_display.setter
    def measure_statistic_display(self, _value: bool) -> None: ...

    @property
    def measure_statistic_mode(self) -> Literal["DIFF", "EXTR"]:
        """Control the statistics calculation mode (DIFF or EXTR)."""
        ...

    @measure_statistic_mode.setter
    def measure_statistic_mode(self, _value: Literal["DIFF", "EXTR"]) -> None: ...

    def measure_statistic_reset(self) -> None:
        """Reset measurement statistics calculations."""
        ...

    def measure_item(self, item: str, source: str | None = None) -> float:
        """Measure a specific item.

        Args:
            item: Measurement item name (e.g. VMAX, VMIN, VPP, FREQ, PER).
            source: Optional source channel (e.g. CHAN1).

        Returns:
            Measurement value as float.
        """
        ...

    def measure_item_statistic(self, item: str, source: str | None = None) -> dict:
        """Get statistics for a specific measurement item.

        Args:
            item: Measurement item name.
            source: Optional source channel.

        Returns:
            dict with keys: current, average, min, max, deviation.
        """
        ...

    # ------------------------------------------------------------------
    # Cursor Subsystem
    # ------------------------------------------------------------------

    @property
    def cursor_mode(self) -> CursorModeType:
        """Control the cursor measurement mode (OFF, MAN, TRAC, AUTO, or XY)."""
        ...

    @cursor_mode.setter
    def cursor_mode(self, _value: CursorModeType) -> None: ...

    @property
    def cursor_manual_type(self) -> Literal["X", "Y", "XY"]:
        """Control the manual cursor type (X, Y, or XY)."""
        ...

    @cursor_manual_type.setter
    def cursor_manual_type(self, _value: Literal["X", "Y", "XY"]) -> None: ...

    @property
    def cursor_manual_source(self) -> Literal["CHAN1", "CHAN2", "CHAN3", "CHAN4", "MATH"]:
        """Control the source for manual cursor measurements."""
        ...

    @cursor_manual_source.setter
    def cursor_manual_source(self, _value: Literal["CHAN1", "CHAN2", "CHAN3", "CHAN4", "MATH"]) -> None: ...

    @property
    def cursor_manual_time_unit(self) -> CursorTimeUnitType:
        """Control the time unit for manual cursor X measurements."""
        ...

    @cursor_manual_time_unit.setter
    def cursor_manual_time_unit(self, _value: CursorTimeUnitType) -> None: ...

    @property
    def cursor_manual_voltage_unit(self) -> UnitsType:
        """Control the voltage unit for manual cursor Y measurements."""
        ...

    @cursor_manual_voltage_unit.setter
    def cursor_manual_voltage_unit(self, _value: UnitsType) -> None: ...

    @property
    def cursor_manual_ax(self) -> float:
        """Control the X position of cursor A in seconds (float)."""
        ...

    @cursor_manual_ax.setter
    def cursor_manual_ax(self, _value: float) -> None: ...

    @property
    def cursor_manual_bx(self) -> float:
        """Control the X position of cursor B in seconds (float)."""
        ...

    @cursor_manual_bx.setter
    def cursor_manual_bx(self, _value: float) -> None: ...

    @property
    def cursor_manual_ay(self) -> float:
        """Control the Y position of cursor A in volts (float)."""
        ...

    @cursor_manual_ay.setter
    def cursor_manual_ay(self, _value: float) -> None: ...

    @property
    def cursor_manual_by(self) -> float:
        """Control the Y position of cursor B in volts (float)."""
        ...

    @cursor_manual_by.setter
    def cursor_manual_by(self, _value: float) -> None: ...

    @property
    def cursor_manual_axvalue(self) -> float:
        """Get the X value at cursor A position in current time units (read-only)."""
        ...

    @property
    def cursor_manual_bxvalue(self) -> float:
        """Get the X value at cursor B position in current time units (read-only)."""
        ...

    @property
    def cursor_manual_ayvalue(self) -> float:
        """Get the Y value at cursor A position in current voltage units (read-only)."""
        ...

    @property
    def cursor_manual_byvalue(self) -> float:
        """Get the Y value at cursor B position in current voltage units (read-only)."""
        ...

    @property
    def cursor_manual_xdelta(self) -> float:
        """Get the difference between X-cursor A and B in current time units (read-only)."""
        ...

    @property
    def cursor_manual_inverse_xdelta(self) -> float:
        """Get the reciprocal of X delta (1/delta) in current units (read-only)."""
        ...

    @property
    def cursor_manual_ydelta(self) -> float:
        """Get the difference between Y-cursor A and B in current voltage units (read-only)."""
        ...

    @property
    def cursor_track_source_a(self) -> Literal["CHAN1", "CHAN2", "CHAN3", "CHAN4", "MATH"]:
        """Control the source for track cursor A."""
        ...

    @cursor_track_source_a.setter
    def cursor_track_source_a(self, _value: Literal["CHAN1", "CHAN2", "CHAN3", "CHAN4", "MATH"]) -> None: ...

    @property
    def cursor_track_source_b(self) -> Literal["CHAN1", "CHAN2", "CHAN3", "CHAN4", "MATH"]:
        """Control the source for track cursor B."""
        ...

    @cursor_track_source_b.setter
    def cursor_track_source_b(self, _value: Literal["CHAN1", "CHAN2", "CHAN3", "CHAN4", "MATH"]) -> None: ...

    @property
    def cursor_track_time_unit(self) -> CursorTimeUnitType:
        """Control the time unit for track cursor X measurements."""
        ...

    @cursor_track_time_unit.setter
    def cursor_track_time_unit(self, _value: CursorTimeUnitType) -> None: ...

    @property
    def cursor_track_voltage_unit_a(self) -> UnitsType:
        """Control the voltage unit for track cursor A Y measurements."""
        ...

    @cursor_track_voltage_unit_a.setter
    def cursor_track_voltage_unit_a(self, _value: UnitsType) -> None: ...

    @property
    def cursor_track_voltage_unit_b(self) -> UnitsType:
        """Control the voltage unit for track cursor B Y measurements."""
        ...

    @cursor_track_voltage_unit_b.setter
    def cursor_track_voltage_unit_b(self, _value: UnitsType) -> None: ...

    @property
    def cursor_track_ax(self) -> float:
        """Control the X position of track cursor A in seconds (float)."""
        ...

    @cursor_track_ax.setter
    def cursor_track_ax(self, _value: float) -> None: ...

    @property
    def cursor_track_bx(self) -> float:
        """Control the X position of track cursor B in seconds (float)."""
        ...

    @cursor_track_bx.setter
    def cursor_track_bx(self, _value: float) -> None: ...

    @property
    def cursor_track_axvalue(self) -> float:
        """Get the X value at track cursor A in current time units (read-only)."""
        ...

    @property
    def cursor_track_bxvalue(self) -> float:
        """Get the X value at track cursor B in current time units (read-only)."""
        ...

    @property
    def cursor_track_ayvalue(self) -> float:
        """Get the Y value at track cursor A in current voltage units (read-only)."""
        ...

    @property
    def cursor_track_byvalue(self) -> float:
        """Get the Y value at track cursor B in current voltage units (read-only)."""
        ...

    @property
    def cursor_track_xdelta(self) -> float:
        """Get the difference between X-track A and B in current time units (read-only)."""
        ...

    @property
    def cursor_track_inverse_xdelta(self) -> float:
        """Get the reciprocal of track X delta (1/delta) in current units (read-only)."""
        ...

    @property
    def cursor_track_ydelta(self) -> float:
        """Get the difference between Y-track A and B in current voltage units (read-only)."""
        ...

    @property
    def cursor_auto_item(self) -> Literal[
        "VMAX", "VMIN", "VPP", "VTOP", "VBAS", "VAMP", "VAVG", "VRMS",
        "OVER", "PRES", "MAR", "MPER", "FREQ", "RTIM", "FTIM", "PWID",
        "NWID", "PDUT", "NDUT", "TVMA", "TVMI", "PSL", "NSL",
        "VUPP", "VMID", "VLOW", "VAR", "PVRM",
    ]:
        """Control which measurement item the auto cursor displays."""
        ...

    @cursor_auto_item.setter
    def cursor_auto_item(self, _value: str) -> None: ...

    @property
    def cursor_auto_source(self) -> Literal["CHAN1", "CHAN2", "CHAN3", "CHAN4", "MATH"]:
        """Control the source for auto cursor measurements."""
        ...

    @cursor_auto_source.setter
    def cursor_auto_source(self, _value: Literal["CHAN1", "CHAN2", "CHAN3", "CHAN4", "MATH"]) -> None: ...

    @property
    def cursor_auto_time_unit(self) -> CursorTimeUnitType:
        """Control the time unit for auto cursor X measurements."""
        ...

    @cursor_auto_time_unit.setter
    def cursor_auto_time_unit(self, _value: CursorTimeUnitType) -> None: ...

    @property
    def cursor_auto_voltage_unit(self) -> UnitsType:
        """Control the voltage unit for auto cursor Y measurements."""
        ...

    @cursor_auto_voltage_unit.setter
    def cursor_auto_voltage_unit(self, _value: UnitsType) -> None: ...

    @property
    def cursor_auto_axvalue(self) -> float:
        """Get the X value at auto cursor A in current time units (read-only)."""
        ...

    @property
    def cursor_auto_bxvalue(self) -> float:
        """Get the X value at auto cursor B in current time units (read-only)."""
        ...

    @property
    def cursor_auto_ayvalue(self) -> float:
        """Get the Y value at auto cursor A in current voltage units (read-only)."""
        ...

    @property
    def cursor_auto_byvalue(self) -> float:
        """Get the Y value at auto cursor B in current voltage units (read-only)."""
        ...

    @property
    def cursor_auto_xdelta(self) -> float:
        """Get the difference between auto cursor A and B X positions (read-only)."""
        ...

    @property
    def cursor_xy_ax(self) -> float:
        """Control the X position of XY cursor A in volts (float)."""
        ...

    @cursor_xy_ax.setter
    def cursor_xy_ax(self, _value: float) -> None: ...

    @property
    def cursor_xy_bx(self) -> float:
        """Control the X position of XY cursor B in volts (float)."""
        ...

    @cursor_xy_bx.setter
    def cursor_xy_bx(self, _value: float) -> None: ...

    @property
    def cursor_xy_ay(self) -> float:
        """Control the Y position of XY cursor A in volts (float)."""
        ...

    @cursor_xy_ay.setter
    def cursor_xy_ay(self, _value: float) -> None: ...

    @property
    def cursor_xy_by(self) -> float:
        """Control the Y position of XY cursor B in volts (float)."""
        ...

    @cursor_xy_by.setter
    def cursor_xy_by(self, _value: float) -> None: ...

    @property
    def cursor_xy_axvalue(self) -> float:
        """Get the X value at XY cursor A in volts (read-only)."""
        ...

    @property
    def cursor_xy_bxvalue(self) -> float:
        """Get the X value at XY cursor B in volts (read-only)."""
        ...

    @property
    def cursor_xy_ayvalue(self) -> float:
        """Get the Y value at XY cursor A in volts (read-only)."""
        ...

    @property
    def cursor_xy_byvalue(self) -> float:
        """Get the Y value at XY cursor B in volts (read-only)."""
        ...

    # ------------------------------------------------------------------
    # Math Subsystem
    # ------------------------------------------------------------------

    @property
    def math_display(self) -> bool:
        """Control if the math waveform is displayed (bool)."""
        ...

    @math_display.setter
    def math_display(self, _value: bool) -> None: ...

    @property
    def math_operator(self) -> MathOperatorType:
        """Control the math operation type."""
        ...

    @math_operator.setter
    def math_operator(self, _value: MathOperatorType) -> None: ...

    @property
    def math_source1(self) -> ChannelListType:
        """Control the first source for math operations."""
        ...

    @math_source1.setter
    def math_source1(self, _value: ChannelListType) -> None: ...

    @property
    def math_source2(self) -> ChannelListType:
        """Control the second source for math operations."""
        ...

    @math_source2.setter
    def math_source2(self, _value: ChannelListType) -> None: ...

    @property
    def math_logic_source1(self) -> DigitalChannelType:
        """Control the first source for logical math operations (D0-D15)."""
        ...

    @math_logic_source1.setter
    def math_logic_source1(self, _value: DigitalChannelType) -> None: ...

    @property
    def math_logic_source2(self) -> DigitalChannelType:
        """Control the second source for logical math operations (D0-D15)."""
        ...

    @math_logic_source2.setter
    def math_logic_source2(self, _value: DigitalChannelType) -> None: ...

    @property
    def math_scale(self) -> float:
        """Control the vertical scale of the math waveform in units per division (float)."""
        ...

    @math_scale.setter
    def math_scale(self, _value: float) -> None: ...

    @property
    def math_offset(self) -> float:
        """Control the vertical offset of the math waveform (float)."""
        ...

    @math_offset.setter
    def math_offset(self, _value: float) -> None: ...

    @property
    def math_invert(self) -> bool:
        """Control if the math waveform is inverted (bool)."""
        ...

    @math_invert.setter
    def math_invert(self, _value: bool) -> None: ...

    def math_reset(self) -> None:
        """Reset the math waveform to default settings."""
        ...

    @property
    def math_fft_source(self) -> AnalogChannelType:
        """Control the source for FFT operations (CHANnel1-4)."""
        ...

    @math_fft_source.setter
    def math_fft_source(self, _value: AnalogChannelType) -> None: ...

    @property
    def math_fft_window(self) -> FftWindowType:
        """Control the FFT window function."""
        ...

    @math_fft_window.setter
    def math_fft_window(self, _value: FftWindowType) -> None: ...

    @property
    def math_fft_split(self) -> bool:
        """Control if FFT display is split screen (bool)."""
        ...

    @math_fft_split.setter
    def math_fft_split(self, _value: bool) -> None: ...

    @property
    def math_fft_unit(self) -> Literal["DB", "VRMS"]:
        """Control the FFT vertical unit (DB or VRMS)."""
        ...

    @math_fft_unit.setter
    def math_fft_unit(self, _value: Literal["DB", "VRMS"]) -> None: ...

    @property
    def math_fft_horizontal_scale(self) -> float:
        """Control the FFT horizontal scale in Hz per division (float)."""
        ...

    @math_fft_horizontal_scale.setter
    def math_fft_horizontal_scale(self, _value: float) -> None: ...

    @property
    def math_fft_horizontal_center(self) -> float:
        """Control the FFT horizontal center frequency in Hz (float)."""
        ...

    @math_fft_horizontal_center.setter
    def math_fft_horizontal_center(self, _value: float) -> None: ...

    @property
    def math_fft_mode(self) -> Literal["AMPL", "PSD"]:
        """Control the FFT display mode (AMPL or PSD)."""
        ...

    @math_fft_mode.setter
    def math_fft_mode(self, _value: Literal["AMPL", "PSD"]) -> None: ...

    @property
    def math_filter_type(self) -> FilterTypeType:
        """Control the filter type (LPAS, HPAS, BPAS, or BST)."""
        ...

    @math_filter_type.setter
    def math_filter_type(self, _value: FilterTypeType) -> None: ...

    @property
    def math_filter_w1(self) -> float:
        """Control the filter cutoff frequency 1 in Hz (float)."""
        ...

    @math_filter_w1.setter
    def math_filter_w1(self, _value: float) -> None: ...

    @property
    def math_filter_w2(self) -> float:
        """Control the filter cutoff frequency 2 in Hz (float)."""
        ...

    @math_filter_w2.setter
    def math_filter_w2(self, _value: float) -> None: ...

    # -- Math Options --

    @property
    def math_option_start(self) -> int:
        """Control the start point for math operations (int, 0-1198)."""
        ...

    @math_option_start.setter
    def math_option_start(self, _value: int) -> None: ...

    @property
    def math_option_end(self) -> int:
        """Control the end point for math operations (int, 1-1199)."""
        ...

    @math_option_end.setter
    def math_option_end(self, _value: int) -> None: ...

    @property
    def math_option_invert(self) -> bool:
        """Control if math option inversion is enabled (bool)."""
        ...

    @math_option_invert.setter
    def math_option_invert(self, _value: bool) -> None: ...

    @property
    def math_option_sensitivity(self) -> float:
        """Control the sensitivity for math differentiation (float, 0-0.96)."""
        ...

    @math_option_sensitivity.setter
    def math_option_sensitivity(self, _value: float) -> None: ...

    @property
    def math_option_distance(self) -> int:
        """Control the smoothing window width for math operations (int, 3-201)."""
        ...

    @math_option_distance.setter
    def math_option_distance(self, _value: int) -> None: ...

    @property
    def math_option_auto_scale(self) -> bool:
        """Control if auto scale is enabled for math operations (bool)."""
        ...

    @math_option_auto_scale.setter
    def math_option_auto_scale(self, _value: bool) -> None: ...

    @property
    def math_option_threshold1(self) -> float:
        """Control threshold 1 for logic math operations in volts (float)."""
        ...

    @math_option_threshold1.setter
    def math_option_threshold1(self, _value: float) -> None: ...

    @property
    def math_option_threshold2(self) -> float:
        """Control threshold 2 for logic math operations in volts (float)."""
        ...

    @math_option_threshold2.setter
    def math_option_threshold2(self, _value: float) -> None: ...

    @property
    def math_option_fx_source1(self) -> AnalogChannelType:
        """Control source 1 for f(x) math operations (CHANnel1-4)."""
        ...

    @math_option_fx_source1.setter
    def math_option_fx_source1(self, _value: AnalogChannelType) -> None: ...

    @property
    def math_option_fx_source2(self) -> AnalogChannelType:
        """Control source 2 for f(x) math operations (CHANnel1-4)."""
        ...

    @math_option_fx_source2.setter
    def math_option_fx_source2(self, _value: AnalogChannelType) -> None: ...

    @property
    def math_option_fx_operator(self) -> Literal["ADD", "SUBT", "MULT", "DIV"]:
        """Control the operator for f(x) math operations."""
        ...

    @math_option_fx_operator.setter
    def math_option_fx_operator(self, _value: Literal["ADD", "SUBT", "MULT", "DIV"]) -> None: ...

    # ------------------------------------------------------------------
    # Mask Testing Subsystem
    # ------------------------------------------------------------------

    @property
    def mask_enable(self) -> bool:
        """Control if pass/fail mask testing is enabled (bool)."""
        ...

    @mask_enable.setter
    def mask_enable(self, _value: bool) -> None: ...

    @property
    def mask_source(self) -> AnalogChannelType:
        """Control the source for mask testing (CHANnel1-4)."""
        ...

    @mask_source.setter
    def mask_source(self, _value: AnalogChannelType) -> None: ...

    @property
    def mask_operate(self) -> Literal["RUN", "STOP"]:
        """Control the mask test operation mode (RUN or STOP)."""
        ...

    @mask_operate.setter
    def mask_operate(self, _value: Literal["RUN", "STOP"]) -> None: ...

    @property
    def mask_message_display(self) -> bool:
        """Control if mask test results are displayed on screen (bool)."""
        ...

    @mask_message_display.setter
    def mask_message_display(self, _value: bool) -> None: ...

    @property
    def mask_stop_on_fail(self) -> bool:
        """Control if testing stops when mask test fails (bool)."""
        ...

    @mask_stop_on_fail.setter
    def mask_stop_on_fail(self, _value: bool) -> None: ...

    @property
    def mask_sound_output(self) -> bool:
        """Control if a sound is played on mask test failure (bool)."""
        ...

    @mask_sound_output.setter
    def mask_sound_output(self, _value: bool) -> None: ...

    @property
    def mask_x(self) -> float:
        """Control the horizontal (time) adjustment of the mask (float)."""
        ...

    @mask_x.setter
    def mask_x(self, _value: float) -> None: ...

    @property
    def mask_y(self) -> float:
        """Control the vertical (voltage) adjustment of the mask (float)."""
        ...

    @mask_y.setter
    def mask_y(self, _value: float) -> None: ...

    def mask_create(self) -> None:
        """Create a mask from the current waveform."""
        ...

    @property
    def mask_passed(self) -> float:
        """Get the number of passed mask tests (read-only)."""
        ...

    @property
    def mask_failed(self) -> float:
        """Get the number of failed mask tests (read-only)."""
        ...

    @property
    def mask_total(self) -> float:
        """Get the total number of mask tests performed (read-only)."""
        ...

    def mask_reset(self) -> None:
        """Reset mask test statistics."""
        ...

    # ------------------------------------------------------------------
    # Storage Subsystem
    # ------------------------------------------------------------------

    @property
    def storage_image_type(self) -> StorageImageType:
        """Control the image storage format (PNG, BMP8, BMP24, JPEG, or TIFF)."""
        ...

    @storage_image_type.setter
    def storage_image_type(self, _value: StorageImageType) -> None: ...

    @property
    def storage_image_invert(self) -> bool:
        """Control if the stored image colors are inverted (bool)."""
        ...

    @storage_image_invert.setter
    def storage_image_invert(self, _value: bool) -> None: ...

    @property
    def storage_image_color(self) -> Literal["ON", "OFF"]:
        """Control if the stored image is in color or intensity-graded (ON or OFF)."""
        ...

    @storage_image_color.setter
    def storage_image_color(self, _value: Literal["ON", "OFF"]) -> None: ...

    # ------------------------------------------------------------------
    # System Subsystem
    # ------------------------------------------------------------------

    @property
    def system_autoscale_enabled(self) -> bool:
        """Control if the autoscale function is enabled (bool)."""
        ...

    @system_autoscale_enabled.setter
    def system_autoscale_enabled(self, _value: bool) -> None: ...

    @property
    def system_beeper(self) -> bool:
        """Control if the beeper is enabled (bool)."""
        ...

    @system_beeper.setter
    def system_beeper(self, _value: bool) -> None: ...

    @property
    def system_error(self) -> tuple:
        """Get the last system error as (error_code, error_message) (read-only)."""
        ...

    @property
    def system_gam(self) -> int:
        """Get the number of analog channels available (read-only, always 12)."""
        ...

    @property
    def system_language(self) -> SystemLanguageType:
        """Control the display language."""
        ...

    @system_language.setter
    def system_language(self, _value: SystemLanguageType) -> None: ...

    @property
    def system_locked(self) -> bool:
        """Control if the front panel keyboard is locked (bool)."""
        ...

    @system_locked.setter
    def system_locked(self, _value: bool) -> None: ...

    @property
    def system_power_on_setting(self) -> Literal["LAT", "DEF"]:
        """Control the power-on configuration (LAT or DEF)."""
        ...

    @system_power_on_setting.setter
    def system_power_on_setting(self, _value: Literal["LAT", "DEF"]) -> None: ...

    @property
    def system_ram(self) -> int:
        """Get the system RAM size information (read-only, always 4)."""
        ...

    def system_option_install(self, license_key: str) -> None:
        """Install an option using a 28-character license key."""
        ...

    def system_option_uninstall(self) -> None:
        """Uninstall all installed options."""
        ...

    # ------------------------------------------------------------------
    # Logic Analyzer Subsystem (MSO models only)
    # ------------------------------------------------------------------

    @property
    def la_state(self) -> bool:
        """Control if the logic analyzer is enabled (bool, MSO models only)."""
        ...

    @la_state.setter
    def la_state(self, _value: bool) -> None: ...

    @property
    def la_active(self) -> ChannelListDGroupsType:
        """Control the active digital channel or group."""
        ...

    @la_active.setter
    def la_active(self, _value: ChannelListDGroupsType) -> None: ...

    def la_autosort(self, _value: bool) -> None:
        """Set the auto sort mode for digital channels (bool)."""
        ...

    @property
    def la_size(self) -> Literal["SMAL", "LARG"]:
        """Control the display size of digital channels (SMAL or LARG)."""
        ...

    @la_size.setter
    def la_size(self, _value: Literal["SMAL", "LARG"]) -> None: ...

    @property
    def la_time_calibration(self) -> float:
        """Control the time calibration offset for digital channels in seconds (float)."""
        ...

    @la_time_calibration.setter
    def la_time_calibration(self, _value: float) -> None: ...

    @property
    def la_pod1_display(self) -> bool:
        """Control if POD1 (D0-D7) is displayed (bool)."""
        ...

    @la_pod1_display.setter
    def la_pod1_display(self, _value: bool) -> None: ...

    @property
    def la_pod2_display(self) -> bool:
        """Control if POD2 (D8-D15) is displayed (bool)."""
        ...

    @la_pod2_display.setter
    def la_pod2_display(self, _value: bool) -> None: ...

    @property
    def la_pod1_threshold(self) -> float:
        """Control the threshold voltage for POD1 (D0-D7) in volts (float, -15 to 15)."""
        ...

    @la_pod1_threshold.setter
    def la_pod1_threshold(self, _value: float) -> None: ...

    @property
    def la_pod2_threshold(self) -> float:
        """Control the threshold voltage for POD2 (D8-D15) in volts (float, -15 to 15)."""
        ...

    @la_pod2_threshold.setter
    def la_pod2_threshold(self, _value: float) -> None: ...

    def la_digital_display(self, channel: int, enabled: bool) -> None:
        """Control if a specific digital channel is displayed."""
        ...

    def la_digital_display_get(self, channel: int) -> bool:
        """Get if a specific digital channel is displayed."""
        ...

    def la_digital_position(self, channel: int, position: int) -> None:
        """Set the display position of a specific digital channel."""
        ...

    def la_digital_position_get(self, channel: int) -> int:
        """Get the display position of a specific digital channel."""
        ...

    def la_digital_label(self, channel: int, label: str) -> None:
        """Set the label for a specific digital channel (max 4 chars)."""
        ...

    def la_digital_label_get(self, channel: int) -> str:
        """Get the label for a specific digital channel."""
        ...

    # ------------------------------------------------------------------
    # Reference Waveform Subsystem
    # ------------------------------------------------------------------

    @property
    def reference_display(self) -> bool:
        """Control if reference waveform display is globally enabled (bool)."""
        ...

    @reference_display.setter
    def reference_display(self, _value: bool) -> None: ...

    def reference_enable(self, ref: int, enabled: bool) -> None:
        """Enable or disable a specific reference waveform (ref 1-10)."""
        ...

    def reference_enable_get(self, ref: int) -> bool:
        """Get if a specific reference waveform is enabled."""
        ...

    def reference_source(self, ref: int, source: str) -> None:
        """Set the source for a reference waveform (ref 1-10)."""
        ...

    def reference_source_get(self, ref: int) -> str:
        """Get the source for a reference waveform."""
        ...

    def reference_vscale(self, ref: int, scale: float) -> None:
        """Set the vertical scale of a reference waveform in V/div."""
        ...

    def reference_vscale_get(self, ref: int) -> float:
        """Get the vertical scale of a reference waveform in V/div."""
        ...

    def reference_voffset(self, ref: int, offset: float) -> None:
        """Set the vertical offset of a reference waveform in volts."""
        ...

    def reference_voffset_get(self, ref: int) -> float:
        """Get the vertical offset of a reference waveform in volts."""
        ...

    def reference_reset(self, ref: int) -> None:
        """Reset a reference waveform to default settings."""
        ...

    def reference_save(self, ref: int) -> None:
        """Save the current waveform to a reference slot."""
        ...

    def reference_current(self, ref: int) -> None:
        """Set the reference waveform data to the current waveform."""
        ...

    def reference_color(self, ref: int, color: str) -> None:
        """Set the display color of a reference waveform (GRAY, GREEn, LBLue, MAGenta, ORANge)."""
        ...

    def reference_color_get(self, ref: int) -> str:
        """Get the display color of a reference waveform."""
        ...

    # ------------------------------------------------------------------
    # Waveform Record Subsystem
    # ------------------------------------------------------------------

    @property
    def wrecord_enable(self) -> bool:
        """Control if waveform recording is enabled (bool)."""
        ...

    @wrecord_enable.setter
    def wrecord_enable(self, _value: bool) -> None: ...

    @property
    def wrecord_end_frame(self) -> int:
        """Control the end frame number for waveform recording (int)."""
        ...

    @wrecord_end_frame.setter
    def wrecord_end_frame(self, _value: int) -> None: ...

    @property
    def wrecord_max_frames(self) -> float:
        """Get the maximum number of frames that can be recorded (read-only)."""
        ...

    @property
    def wrecord_interval(self) -> float:
        """Control the frame recording interval in seconds (float, 100ns-10s)."""
        ...

    @wrecord_interval.setter
    def wrecord_interval(self, _value: float) -> None: ...

    @property
    def wrecord_prompt(self) -> bool:
        """Control if recording status prompt is displayed (bool)."""
        ...

    @wrecord_prompt.setter
    def wrecord_prompt(self, _value: bool) -> None: ...

    @property
    def wrecord_operate(self) -> Literal["RUN", "STOP"]:
        """Control the waveform recording operation (RUN or STOP)."""
        ...

    @wrecord_operate.setter
    def wrecord_operate(self, _value: Literal["RUN", "STOP"]) -> None: ...

    # ------------------------------------------------------------------
    # Waveform Replay Subsystem
    # ------------------------------------------------------------------

    @property
    def wreplay_start_frame(self) -> int:
        """Control the start frame number for replay (int)."""
        ...

    @wreplay_start_frame.setter
    def wreplay_start_frame(self, _value: int) -> None: ...

    @property
    def wreplay_end_frame(self) -> int:
        """Control the end frame number for replay (int)."""
        ...

    @wreplay_end_frame.setter
    def wreplay_end_frame(self, _value: int) -> None: ...

    @property
    def wreplay_max_frames(self) -> float:
        """Get the maximum number of frames available for replay (read-only)."""
        ...

    @property
    def wreplay_interval(self) -> float:
        """Control the frame replay interval in seconds (float)."""
        ...

    @wreplay_interval.setter
    def wreplay_interval(self, _value: float) -> None: ...

    @property
    def wreplay_mode(self) -> Literal["REP", "SING"]:
        """Control the playback mode (REP or SING)."""
        ...

    @wreplay_mode.setter
    def wreplay_mode(self, _value: Literal["REP", "SING"]) -> None: ...

    @property
    def wreplay_direction(self) -> Literal["FORW", "BACK"]:
        """Control the playback direction (FORW or BACK)."""
        ...

    @wreplay_direction.setter
    def wreplay_direction(self, _value: Literal["FORW", "BACK"]) -> None: ...

    @property
    def wreplay_operate(self) -> Literal["PLAY", "PAUS", "STOP"]:
        """Control the playback operation (PLAY, PAUS, or STOP)."""
        ...

    @wreplay_operate.setter
    def wreplay_operate(self, _value: Literal["PLAY", "PAUS", "STOP"]) -> None: ...

    @property
    def wreplay_current_frame(self) -> int:
        """Control the current frame number during playback (int)."""
        ...

    @wreplay_current_frame.setter
    def wreplay_current_frame(self, _value: int) -> None: ...

    # ------------------------------------------------------------------
    # Source / Function Generator Subsystem (-S models only)
    # ------------------------------------------------------------------

    @property
    def source_output(self) -> bool:
        """Control if source output 1 is enabled (bool, -S models only)."""
        ...

    @source_output.setter
    def source_output(self, _value: bool) -> None: ...

    @property
    def source_output2(self) -> bool:
        """Control if source output 2 is enabled (bool)."""
        ...

    @source_output2.setter
    def source_output2(self, _value: bool) -> None: ...

    @property
    def source_impedance(self) -> Literal["OMEG", "FIFT"]:
        """Control the output impedance of source 1 (OMEG or FIFT)."""
        ...

    @source_impedance.setter
    def source_impedance(self, _value: Literal["OMEG", "FIFT"]) -> None: ...

    @property
    def source_frequency(self) -> float:
        """Control the output frequency of source 1 in Hz (float)."""
        ...

    @source_frequency.setter
    def source_frequency(self, _value: float) -> None: ...

    @property
    def source_phase(self) -> float:
        """Control the start phase of source 1 in degrees (float, 0-360)."""
        ...

    @source_phase.setter
    def source_phase(self, _value: float) -> None: ...

    def source_phase_init(self) -> None:
        """Initialize the phase of source 1, aligning it with source 2."""
        ...

    @property
    def source_function(self) -> SourceFunctionType:
        """Control the waveform function of source 1."""
        ...

    @source_function.setter
    def source_function(self, _value: SourceFunctionType) -> None: ...

    @property
    def source_ramp_symmetry(self) -> float:
        """Control the symmetry of the ramp waveform in percent (float, 0-100)."""
        ...

    @source_ramp_symmetry.setter
    def source_ramp_symmetry(self, _value: float) -> None: ...

    @property
    def source_voltage(self) -> float:
        """Control the output voltage amplitude of source 1 in Vpp (float)."""
        ...

    @source_voltage.setter
    def source_voltage(self, _value: float) -> None: ...

    @property
    def source_voltage_offset(self) -> float:
        """Control the DC offset of the source output in VDC (float)."""
        ...

    @source_voltage_offset.setter
    def source_voltage_offset(self, _value: float) -> None: ...

    @property
    def source_pulse_duty(self) -> float:
        """Control the duty cycle of the pulse waveform in percent (float, 10-90)."""
        ...

    @source_pulse_duty.setter
    def source_pulse_duty(self, _value: float) -> None: ...

    @property
    def source_mod_state(self) -> bool:
        """Control if modulation is enabled for source 1 (bool)."""
        ...

    @source_mod_state.setter
    def source_mod_state(self, _value: bool) -> None: ...

    @property
    def source_mod_type(self) -> Literal["AM", "FM"]:
        """Control the modulation type (AM or FM)."""
        ...

    @source_mod_type.setter
    def source_mod_type(self, _value: Literal["AM", "FM"]) -> None: ...

    @property
    def source_mod_am_depth(self) -> float:
        """Control the AM modulation depth in percent (float, 0-120)."""
        ...

    @source_mod_am_depth.setter
    def source_mod_am_depth(self, _value: float) -> None: ...

    @property
    def source_mod_am_frequency(self) -> float:
        """Control the AM modulation frequency in Hz (float, 1-50000)."""
        ...

    @source_mod_am_frequency.setter
    def source_mod_am_frequency(self, _value: float) -> None: ...

    @property
    def source_mod_am_function(self) -> Literal["SIN", "SQU", "TRI", "NOIS"]:
        """Control the AM modulation waveform."""
        ...

    @source_mod_am_function.setter
    def source_mod_am_function(self, _value: Literal["SIN", "SQU", "TRI", "NOIS"]) -> None: ...

    @property
    def source_mod_fm_deviation(self) -> float:
        """Control the FM frequency deviation in Hz (float)."""
        ...

    @source_mod_fm_deviation.setter
    def source_mod_fm_deviation(self, _value: float) -> None: ...

    @property
    def source_mod_fm_frequency(self) -> float:
        """Control the FM modulation frequency in Hz (float, 1-50000)."""
        ...

    @source_mod_fm_frequency.setter
    def source_mod_fm_frequency(self, _value: float) -> None: ...

    @property
    def source_mod_fm_function(self) -> Literal["SIN", "SQU", "TRI", "NOIS"]:
        """Control the FM modulation waveform."""
        ...

    @source_mod_fm_function.setter
    def source_mod_fm_function(self, _value: Literal["SIN", "SQU", "TRI", "NOIS"]) -> None: ...

    @property
    def source_apply(self) -> str:
        """Get the current source configuration as a comma-separated string (read-only)."""
        ...

    def source_apply_sinusoid(
        self,
        frequency: float = 1e3,
        amplitude: float = 5.0,
        offset: float = 0.0,
        phase: float = 0.0,
    ) -> None:
        """Apply a sinusoidal waveform to source 1."""
        ...

    def source_apply_square(
        self,
        frequency: float = 1e3,
        amplitude: float = 5.0,
        offset: float = 0.0,
        phase: float = 0.0,
    ) -> None:
        """Apply a square waveform to source 1."""
        ...

    def source_apply_ramp(
        self,
        frequency: float = 1e3,
        amplitude: float = 5.0,
        offset: float = 0.0,
        phase: float = 0.0,
    ) -> None:
        """Apply a ramp waveform to source 1."""
        ...

    def source_apply_pulse(
        self,
        frequency: float = 1e3,
        amplitude: float = 5.0,
        offset: float = 0.0,
        phase: float = 0.0,
    ) -> None:
        """Apply a pulse waveform to source 1."""
        ...

    def source_apply_noise(self, amplitude: float = 5.0, offset: float = 0.0) -> None:
        """Apply a noise waveform to source 1."""
        ...

    def source_apply_user(
        self,
        frequency: float = 1e3,
        amplitude: float = 5.0,
        offset: float = 0.0,
        phase: float = 0.0,
    ) -> None:
        """Apply an arbitrary user waveform to source 1."""
        ...

    # ------------------------------------------------------------------
    # Decoder Subsystem
    # ------------------------------------------------------------------

    @property
    def decoder1_mode(self) -> DecoderModeType:
        """Control the protocol decoder 1 mode (PAR, UART, SPI, or IIC)."""
        ...

    @decoder1_mode.setter
    def decoder1_mode(self, _value: DecoderModeType) -> None: ...

    @property
    def decoder1_display(self) -> bool:
        """Control if decoder 1 results are displayed (bool)."""
        ...

    @decoder1_display.setter
    def decoder1_display(self, _value: bool) -> None: ...

    @property
    def decoder1_format(self) -> DecoderFormatType:
        """Control the display format for decoder 1."""
        ...

    @decoder1_format.setter
    def decoder1_format(self, _value: DecoderFormatType) -> None: ...

    @property
    def decoder1_position(self) -> int:
        """Control the vertical position of decoder 1 display (int, 50-350)."""
        ...

    @decoder1_position.setter
    def decoder1_position(self, _value: int) -> None: ...

    @property
    def decoder1_threshold_auto(self) -> bool:
        """Control if automatic threshold detection is enabled for decoder 1 (bool)."""
        ...

    @decoder1_threshold_auto.setter
    def decoder1_threshold_auto(self, _value: bool) -> None: ...

    @property
    def decoder1_config_label(self) -> bool:
        """Control if labels are displayed for decoder 1 (bool)."""
        ...

    @decoder1_config_label.setter
    def decoder1_config_label(self, _value: bool) -> None: ...

    @property
    def decoder1_config_line(self) -> bool:
        """Control if bus lines are displayed for decoder 1 (bool)."""
        ...

    @decoder1_config_line.setter
    def decoder1_config_line(self, _value: bool) -> None: ...

    @property
    def decoder1_config_format(self) -> bool:
        """Control if format display is enabled for decoder 1 (bool)."""
        ...

    @decoder1_config_format.setter
    def decoder1_config_format(self, _value: bool) -> None: ...

    @property
    def decoder1_config_endian(self) -> bool:
        """Control if MSB-first (big endian) display is enabled for decoder 1 (bool)."""
        ...

    @decoder1_config_endian.setter
    def decoder1_config_endian(self, _value: bool) -> None: ...

    @property
    def decoder1_config_width(self) -> bool:
        """Control if data width display is enabled for decoder 1 (bool)."""
        ...

    @decoder1_config_width.setter
    def decoder1_config_width(self, _value: bool) -> None: ...

    @property
    def decoder1_config_sample_rate(self) -> float:
        """Get the decoder 1 sample rate (read-only)."""
        ...

    @property
    def decoder1_uart_tx(self) -> ChannelListPlusOffType:
        """Control the UART TX source for decoder 1."""
        ...

    @decoder1_uart_tx.setter
    def decoder1_uart_tx(self, _value: ChannelListPlusOffType) -> None: ...

    @property
    def decoder1_uart_rx(self) -> ChannelListPlusOffType:
        """Control the UART RX source for decoder 1."""
        ...

    @decoder1_uart_rx.setter
    def decoder1_uart_rx(self, _value: ChannelListPlusOffType) -> None: ...

    @property
    def decoder1_uart_polarity(self) -> PosNegType:
        """Control the UART signal polarity for decoder 1 (NEG or POS)."""
        ...

    @decoder1_uart_polarity.setter
    def decoder1_uart_polarity(self, _value: PosNegType) -> None: ...

    @property
    def decoder1_uart_endian(self) -> Literal["LSB", "MSB"]:
        """Control the UART bit order for decoder 1 (LSB or MSB)."""
        ...

    @decoder1_uart_endian.setter
    def decoder1_uart_endian(self, _value: Literal["LSB", "MSB"]) -> None: ...

    @property
    def decoder1_uart_baud(self) -> int:
        """Control the UART baud rate for decoder 1 in bps (int, 110-20000000)."""
        ...

    @decoder1_uart_baud.setter
    def decoder1_uart_baud(self, _value: int) -> None: ...

    @property
    def decoder1_uart_width(self) -> Literal[5, 6, 7, 8]:
        """Control the UART data width for decoder 1 (5, 6, 7, or 8 bits)."""
        ...

    @decoder1_uart_width.setter
    def decoder1_uart_width(self, _value: Literal[5, 6, 7, 8]) -> None: ...

    @property
    def decoder1_uart_stop(self) -> Literal["1", "1.5", "2"]:
        """Control the UART stop bit configuration for decoder 1."""
        ...

    @decoder1_uart_stop.setter
    def decoder1_uart_stop(self, _value: Literal["1", "1.5", "2"]) -> None: ...

    @property
    def decoder1_uart_parity(self) -> Literal["NONE", "EVEN", "ODD"]:
        """Control the UART parity for decoder 1."""
        ...

    @decoder1_uart_parity.setter
    def decoder1_uart_parity(self, _value: Literal["NONE", "EVEN", "ODD"]) -> None: ...

    @property
    def decoder1_iic_clock(self) -> ChannelListType:
        """Control the I2C clock source for decoder 1."""
        ...

    @decoder1_iic_clock.setter
    def decoder1_iic_clock(self, _value: ChannelListType) -> None: ...

    @property
    def decoder1_iic_data(self) -> ChannelListType:
        """Control the I2C data source for decoder 1."""
        ...

    @decoder1_iic_data.setter
    def decoder1_iic_data(self, _value: ChannelListType) -> None: ...

    @property
    def decoder1_iic_address(self) -> Literal["NORM", "RW"]:
        """Control the I2C address mode for decoder 1 (NORM or RW)."""
        ...

    @decoder1_iic_address.setter
    def decoder1_iic_address(self, _value: Literal["NORM", "RW"]) -> None: ...

    @property
    def decoder1_spi_clock(self) -> ChannelListType:
        """Control the SPI clock source for decoder 1."""
        ...

    @decoder1_spi_clock.setter
    def decoder1_spi_clock(self, _value: ChannelListType) -> None: ...

    @property
    def decoder1_spi_miso(self) -> ChannelListPlusOffType:
        """Control the SPI MISO source for decoder 1."""
        ...

    @decoder1_spi_miso.setter
    def decoder1_spi_miso(self, _value: ChannelListPlusOffType) -> None: ...

    @property
    def decoder1_spi_mosi(self) -> ChannelListPlusOffType:
        """Control the SPI MOSI source for decoder 1."""
        ...

    @decoder1_spi_mosi.setter
    def decoder1_spi_mosi(self, _value: ChannelListPlusOffType) -> None: ...

    @property
    def decoder1_spi_cs(self) -> ChannelListType:
        """Control the SPI chip select source for decoder 1."""
        ...

    @decoder1_spi_cs.setter
    def decoder1_spi_cs(self, _value: ChannelListType) -> None: ...

    @property
    def decoder1_spi_select(self) -> Literal["NCS", "CS"]:
        """Control the SPI chip select polarity for decoder 1 (NCS or CS)."""
        ...

    @decoder1_spi_select.setter
    def decoder1_spi_select(self, _value: Literal["NCS", "CS"]) -> None: ...

    @property
    def decoder1_spi_mode(self) -> Literal["CS", "TIM"]:
        """Control the SPI framing mode for decoder 1 (CS or TIM)."""
        ...

    @decoder1_spi_mode.setter
    def decoder1_spi_mode(self, _value: Literal["CS", "TIM"]) -> None: ...

    @property
    def decoder1_spi_timeout(self) -> float:
        """Control the SPI timeout value for decoder 1 in seconds (float)."""
        ...

    @decoder1_spi_timeout.setter
    def decoder1_spi_timeout(self, _value: float) -> None: ...

    @property
    def decoder1_spi_polarity(self) -> PosNegType:
        """Control the SPI clock polarity (CPOL) for decoder 1 (NEG or POS)."""
        ...

    @decoder1_spi_polarity.setter
    def decoder1_spi_polarity(self, _value: PosNegType) -> None: ...

    @property
    def decoder1_spi_edge(self) -> Literal["RISE", "FALL"]:
        """Control the SPI clock edge (CPHA) for decoder 1 (RISE or FALL)."""
        ...

    @decoder1_spi_edge.setter
    def decoder1_spi_edge(self, _value: Literal["RISE", "FALL"]) -> None: ...

    @property
    def decoder1_spi_endian(self) -> Literal["LSB", "MSB"]:
        """Control the SPI bit order for decoder 1 (LSB or MSB)."""
        ...

    @decoder1_spi_endian.setter
    def decoder1_spi_endian(self, _value: Literal["LSB", "MSB"]) -> None: ...

    @property
    def decoder1_spi_width(self) -> int:
        """Control the SPI data width for decoder 1 (int, 8-32 bits)."""
        ...

    @decoder1_spi_width.setter
    def decoder1_spi_width(self, _value: int) -> None: ...

    @property
    def decoder1_parallel_clock(self) -> ChannelListPlusOffType:
        """Control the parallel decoder 1 clock source."""
        ...

    @decoder1_parallel_clock.setter
    def decoder1_parallel_clock(self, _value: ChannelListPlusOffType) -> None: ...

    @property
    def decoder1_parallel_edge(self) -> Literal["RISE", "FALL", "BOTH"]:
        """Control the clock edge for parallel decoder 1."""
        ...

    @decoder1_parallel_edge.setter
    def decoder1_parallel_edge(self, _value: Literal["RISE", "FALL", "BOTH"]) -> None: ...

    @property
    def decoder1_parallel_width(self) -> int:
        """Control the data width for parallel decoder 1 (int, 1-16 bits)."""
        ...

    @decoder1_parallel_width.setter
    def decoder1_parallel_width(self, _value: int) -> None: ...

    @property
    def decoder1_parallel_polarity(self) -> PosNegType:
        """Control the data polarity for parallel decoder 1 (NEG or POS)."""
        ...

    @decoder1_parallel_polarity.setter
    def decoder1_parallel_polarity(self, _value: PosNegType) -> None: ...

    @property
    def decoder1_parallel_noise_reject(self) -> bool:
        """Control if noise rejection is enabled for parallel decoder 1 (bool)."""
        ...

    @decoder1_parallel_noise_reject.setter
    def decoder1_parallel_noise_reject(self, _value: bool) -> None: ...

    @property
    def decoder1_parallel_nr_time(self) -> float:
        """Control the noise rejection time for parallel decoder 1 in seconds (float)."""
        ...

    @decoder1_parallel_nr_time.setter
    def decoder1_parallel_nr_time(self, _value: float) -> None: ...

    @property
    def decoder1_parallel_clock_compensation(self) -> float:
        """Control the clock compensation for parallel decoder 1 in seconds (float)."""
        ...

    @decoder1_parallel_clock_compensation.setter
    def decoder1_parallel_clock_compensation(self, _value: float) -> None: ...

    @property
    def decoder1_parallel_plot(self) -> bool:
        """Control if analog plot is enabled for parallel decoder 1 (bool)."""
        ...

    @decoder1_parallel_plot.setter
    def decoder1_parallel_plot(self, _value: bool) -> None: ...

    # -- Decoder 2 --

    @property
    def decoder2_mode(self) -> DecoderModeType:
        """Control the protocol decoder 2 mode (PAR, UART, SPI, or IIC)."""
        ...

    @decoder2_mode.setter
    def decoder2_mode(self, _value: DecoderModeType) -> None: ...

    @property
    def decoder2_display(self) -> bool:
        """Control if decoder 2 results are displayed (bool)."""
        ...

    @decoder2_display.setter
    def decoder2_display(self, _value: bool) -> None: ...

    @property
    def decoder2_format(self) -> DecoderFormatType:
        """Control the display format for decoder 2."""
        ...

    @decoder2_format.setter
    def decoder2_format(self, _value: DecoderFormatType) -> None: ...

    @property
    def decoder2_position(self) -> int:
        """Control the vertical position of decoder 2 display (int, 50-350)."""
        ...

    @decoder2_position.setter
    def decoder2_position(self, _value: int) -> None: ...

    @property
    def decoder2_threshold_auto(self) -> bool:
        """Control if automatic threshold detection is enabled for decoder 2 (bool)."""
        ...

    @decoder2_threshold_auto.setter
    def decoder2_threshold_auto(self, _value: bool) -> None: ...

    # ------------------------------------------------------------------
    # Event Table Subsystem
    # ------------------------------------------------------------------

    @property
    def etable1_display(self) -> bool:
        """Control if event table 1 is displayed (bool)."""
        ...

    @etable1_display.setter
    def etable1_display(self, _value: bool) -> None: ...

    @property
    def etable1_format(self) -> EventTableFormatType:
        """Control the event table 1 data format (HEX, ASC, or DEC)."""
        ...

    @etable1_format.setter
    def etable1_format(self, _value: EventTableFormatType) -> None: ...

    @property
    def etable1_view(self) -> Literal["PACK", "DET", "PAYL"]:
        """Control the event table 1 view mode (PACK, DET, or PAYL)."""
        ...

    @etable1_view.setter
    def etable1_view(self, _value: Literal["PACK", "DET", "PAYL"]) -> None: ...

    @property
    def etable1_sort(self) -> Literal["ASC", "DESC"]:
        """Control the event table 1 sort order (ASC or DESC)."""
        ...

    @etable1_sort.setter
    def etable1_sort(self, _value: Literal["ASC", "DESC"]) -> None: ...

    @property
    def etable1_row(self) -> int:
        """Control the current row in event table 1 (int)."""
        ...

    @etable1_row.setter
    def etable1_row(self, _value: int) -> None: ...

    @property
    def etable1_data(self) -> str:
        """Get the event table 1 data as a TMC binary data block (read-only)."""
        ...

    @property
    def etable2_display(self) -> bool:
        """Control if event table 2 is displayed (bool)."""
        ...

    @etable2_display.setter
    def etable2_display(self, _value: bool) -> None: ...

    @property
    def etable2_format(self) -> EventTableFormatType:
        """Control the event table 2 data format (HEX, ASC, or DEC)."""
        ...

    @etable2_format.setter
    def etable2_format(self, _value: EventTableFormatType) -> None: ...

    @property
    def etable2_view(self) -> Literal["PACK", "DET", "PAYL"]:
        """Control the event table 2 view mode (PACK, DET, or PAYL)."""
        ...

    @etable2_view.setter
    def etable2_view(self, _value: Literal["PACK", "DET", "PAYL"]) -> None: ...

    @property
    def etable2_sort(self) -> Literal["ASC", "DESC"]:
        """Control the event table 2 sort order (ASC or DESC)."""
        ...

    @etable2_sort.setter
    def etable2_sort(self, _value: Literal["ASC", "DESC"]) -> None: ...

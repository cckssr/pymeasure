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

from time import sleep
import warnings

import pytest


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "mso_only: tests for MSO models (logic analyzer, digital channels)"
    )
    config.addinivalue_line(
        "markers",
        "optional: tests requiring optional hardware (waveform recorder, source generator)",
    )
    config.addinivalue_line(
        "markers",
        "skip_device_error_check: skip device error check after this test or test class",
    )
    config.addinivalue_line(
        "markers",
        "device_error_warning: treat post-test device errors as warnings instead of failures",
    )


def pytest_addoption(parser):
    parser.addoption(
        "--mso",
        action="store_true",
        default=False,
        help="Run MSO-only tests (logic analyzer, digital channels).",
    )
    parser.addoption(
        "--optional",
        action="store_true",
        default=False,
        help="Run optional hardware tests (waveform record/replay, source generator).",
    )


def pytest_collection_modifyitems(config, items):
    skip_mso = pytest.mark.skip(reason="MSO model required – pass --mso to run")
    skip_optional = pytest.mark.skip(reason="Optional hardware required – pass --optional to run")
    for item in items:
        if "mso_only" in item.keywords and not config.getoption("--mso"):
            item.add_marker(skip_mso)
        if "optional" in item.keywords and not config.getoption("--optional"):
            item.add_marker(skip_optional)


@pytest.fixture(autouse=True)
def clear_device_registers(request):
    """Automatically check for device errors after each test.

    This fixture runs automatically for all tests that use the rigol_ds1000
    fixture. It clears the device error registers before the test runs.
    This fixture runs automatically for all tests. After each test, it checks
    if any errors have occurred on the device and fails the test if an error
    is detected.

    Implements automatic retry on VI_ERROR_TMO (-1073807339) timeout errors.
    """
    # Skip error check wenn marker gesetzt ist
    if request.node.get_closest_marker("skip_device_error_check"):
        yield
        return

    warn_on_device_error = bool(request.node.get_closest_marker("device_error_warning"))

    def _handle_device_error(message: str) -> None:
        if warn_on_device_error:
            warnings.warn(message, UserWarning)
        else:
            pytest.fail(message)

    # Before test runs, clear device registers (only if rigol_ds1000 fixture is used)
    if "rigol_ds1000" in request.fixturenames:
        rigol_ds1000 = request.getfixturevalue("rigol_ds1000")
        try:
            rigol_ds1000.clear_registers()
        except Exception as e:
            pytest.fail(f"Failed to clear device registers: {e}")

    yield

    # After test runs, check for errors (only if rigol_ds1000 fixture is used)
    if "rigol_ds1000" in request.fixturenames:
        rigol_ds1000 = request.getfixturevalue("rigol_ds1000")

        # Retry logic for VI_ERROR_TMO
        max_retries = 3
        retry_count = 0

        while retry_count < max_retries:
            try:
                error_code, error_msg = rigol_ds1000.system_error
                if int(error_code) != 0:
                    _handle_device_error(
                        f"Device error detected after test: [{error_code}] {error_msg}"
                    )
                break  # Success, exit retry loop
            except Exception as e:
                error_str = str(e)
                # VI_ERROR_TMO: -1073807339
                if "-1073807339" in error_str or "VI_ERROR_TMO" in error_str:
                    retry_count += 1
                    if retry_count < max_retries:
                        sleep(0.5)  # Wait before retry
                        continue
                    else:
                        _handle_device_error(
                            f"Device timeout (VI_ERROR_TMO) after {max_retries} retries: {e}"
                        )
                else:
                    _handle_device_error(f"Failed to check device errors: {e}")

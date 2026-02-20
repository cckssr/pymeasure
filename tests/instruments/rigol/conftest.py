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

import pytest


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
def check_device_errors(request):
    """Automatically check for device errors after each test.

    This fixture runs automatically for all tests. After each test, it checks
    if any errors have occurred on the device and fails the test if an error
    is detected.
    """
    yield

    # After test runs, check for errors (only if rigol_ds1000 fixture is used)
    if "rigol_ds1000" in request.fixturenames:
        rigol_ds1000 = request.getfixturevalue("rigol_ds1000")
        try:
            error_code, error_msg = rigol_ds1000.system_error
            if int(error_code) != 0:
                pytest.fail(f"Device error detected after test: [{error_code}] {error_msg}")
        except Exception as e:
            pytest.fail(f"Failed to check device errors: {e}")

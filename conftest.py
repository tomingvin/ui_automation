
# This file MUST be in your project's root directory.
# Pytest automatically discovers this file and uses it to configure the test session.

import pytest
import importlib
import os


# --- Command-line Option ---

def pytest_addoption(parser):
   
    parser.addoption(
        "--matrix",
        action="store",
        default="debug_tests",
        help="Specify the test matrix file to use"
    )

# --- Test Generation Hook ---

def pytest_generate_tests(metafunc):

    # This hook only runs for tests that request the 'test_config' fixture.
    if 'test_config' in metafunc.fixturenames:
        matrix_name = metafunc.config.getoption("--matrix")
        try:
            module_path = f"test_suite.{matrix_name}"
            matrix_module = importlib.import_module(module_path)
            matrix = matrix_module.TEST_MATRIX
        except (ModuleNotFoundError, AttributeError):
            # If matrix file is not found, generate no tests for this function.
            metafunc.parametrize("test_config", [])
            return

        test_name = metafunc.function.__name__

        # Find all configurations in the matrix that match the current test's name.
        valid_configs = [item for item in matrix if item.get('test_name') == test_name]

        # If we found valid configurations, create the tests.
        if valid_configs:
            ids = [
                f"{c.get('user')}-{c.get('device') or 'default'}"
                for c in valid_configs
            ]
            metafunc.parametrize("test_config", valid_configs, indirect=True, ids=ids)
        else:
            # If no valid configs are found, explicitly generate ZERO tests.
            metafunc.parametrize("test_config", [])

# --- Custom Fixture Definitions ---

@pytest.fixture
def test_config(request):
 
    return getattr(request, "param", {})

@pytest.fixture
def browser_context_args(browser_context_args, playwright, test_config):

    context_args = browser_context_args.copy()
    device_name = test_config.get("device")

    if device_name:
        context_args.update(playwright.devices[device_name])
    return context_args

@pytest.fixture
def browser_type(playwright, test_config):
    browser_name = test_config.get("browser", "chromium")
    if browser_name not in ["chromium", "firefox", "webkit"]:
        raise ValueError(f"Unsupported browser: {browser_name}")
    return getattr(playwright, browser_name)


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    report_path = getattr(config.option, "htmlpath", None)
    if report_path:
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
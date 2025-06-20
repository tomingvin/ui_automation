# ui_automation

Boilerplate code, UI automation using Playwright and pytest.

## installation

1. pip install pytest-playwright
2. playwright install

## usage

Start tests with for instance pytest tests/ --matrix smoke_tests. If you want to debug/check just one test, make sure it's included in the test-suite "debug_tests" (specified as default in conftest)
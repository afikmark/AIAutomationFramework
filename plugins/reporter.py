from collections.abc import Generator
from pathlib import Path
import os
import pytest
import allure
import re
from allure_commons.types import AttachmentType
from contextlib import contextmanager
from assertpy import assert_that as assertpy_assert_that
from typing import Any, Callable
from dataclasses import dataclass


class TagNames:
    """Centralized tag name constants."""

    UI_TEST = "UI test"
    API_TEST = "API test"
    JIRA_KEY = "Jira key"


class SeverityLevel:
    """Allure severity level constants."""

    BLOCKER = allure.severity_level.BLOCKER
    CRITICAL = allure.severity_level.CRITICAL
    NORMAL = allure.severity_level.NORMAL
    MINOR = allure.severity_level.MINOR
    TRIVIAL = allure.severity_level.TRIVIAL


@dataclass
class FixtureTagRule:
    """Rule for adding tags based on fixtures."""

    fixture_name: str
    tag_name: str


@dataclass
class MarkerTagRule:
    """Rule for adding tags based on pytest markers."""

    marker_name: str
    tag_formatter: Callable[[Any], str]


@dataclass
class MarkerSeverityRule:
    """Rule for setting severity based on pytest markers."""

    marker_name: str
    severity: str


@dataclass
class MarkerLinkRule:
    """Rule for adding links based on pytest markers."""

    marker_name: str
    url_formatter: Callable[[Any], str]
    link_type: str = "issue"


FIXTURE_TAG_RULES = [
    FixtureTagRule(fixture_name="sauce_ui", tag_name=TagNames.UI_TEST),
    FixtureTagRule(fixture_name="pet_store_controller", tag_name=TagNames.API_TEST),
]

MARKER_TAG_RULES = [
    MarkerTagRule(
        marker_name="test_case_key",
        tag_formatter=lambda key: f"{TagNames.JIRA_KEY} - {key}",
    ),
]


MARKER_SEVERITY_RULES = [
    MarkerSeverityRule(marker_name="sanity", severity=SeverityLevel.CRITICAL),
    MarkerSeverityRule(marker_name="smoke", severity=SeverityLevel.BLOCKER),
]


JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
MARKER_LINK_RULES = [
    MarkerLinkRule(
        marker_name="test_case_key",
        url_formatter=lambda key: f"{JIRA_BASE_URL}browse/{key}",
        link_type="issue",
    ),
]


class AllureReporter:
    @contextmanager
    def step(self, message="", *args, **kwargs) -> Generator:
        """Create an Allure step context manager."""
        with allure.step(message):
            yield

    def attach_img(self, screenshot, *args, **kwargs):
        allure.attach.file(
            screenshot, attachment_type=AttachmentType.PNG, name="Screenshot", **kwargs
        )

    def attach_file(self, file, name, *args, **kwargs):
        allure.attach.file(
            file, name="attachment", attachment_type=AttachmentType.WEBM, **kwargs
        )

    def assert_that(self, actual: Any):
        """
        Create an assertion with automatic Allure step.

        Usage:
            reporter.assert_that(page.url).ends_with("/inventory.html")
        """
        return AllureAssertionBuilder(actual)


class AllureAssertionBuilder:
    """Wrapper around assertpy that creates Allure steps for assertions."""

    def __init__(self, actual: Any):
        self._actual = actual
        self._assertpy = assertpy_assert_that(actual)

    def __getattr__(self, name: str):
        """Intercept assertion calls to wrap them in Allure steps."""
        original_method = getattr(self._assertpy, name)

        def wrapper(*args, **kwargs):
            """Wrap assertion method to add Allure step."""
            step_name = self._make_step_name(name, *args)

            with allure.step(step_name):
                original_method(*args, **kwargs)
                return self  # Return self for chaining

        return wrapper

    def _make_step_name(self, method_name: str, *args) -> str:
        """Generate readable step name from assertion."""

        actual_str = self._format_value(self._actual)

        readable_method = method_name.replace("_", " ")

        if args:
            expected_str = self._format_value(args[0])
            return f"Assert that {actual_str} {readable_method} {expected_str}"
        else:
            return f"Assert that {actual_str} {readable_method}"

    def _format_value(self, value: Any) -> str:
        """Format a value for display."""
        if isinstance(value, str):
            if len(value) > 50:  # Truncate long allure step strings
                return f"'{value[:47]}...'"
            return f"'{value}'"
        return str(value)


def _resolve_test_directory(test_path_str: str) -> Path:
    """
    Resolve test path to its containing directory.

    Args:
        test_path_str: Test path from command line (can be file, dir, or node ID)

    Returns:
        Path to directory containing the test
    """
    # Handle test node IDs (e.g., "path/to/test.py::test_function")
    if "::" in test_path_str:
        test_path_str = test_path_str.split("::")[0]

    path = Path(test_path_str)

    if path.is_dir():
        return path

    return path.parent


def _extract_steps_from_docstring(docstring: str | None) -> list[str]:
    """
    Extract steps from test function docstring.

    Args:
        docstring: The test function's docstring

    Returns:
        List of step descriptions
    """
    if not docstring:
        return []

    # Find the "Steps:" section in the docstring
    steps_pattern = r"Steps:\s*\n((?:\s+\d+\).+\n?)+)"
    match = re.search(steps_pattern, docstring)

    if not match:
        return []

    steps_section = match.group(1)

    # Extract individual steps (lines starting with number and parenthesis)
    step_pattern = r"\s+\d+\)\s*(.+)"
    steps = re.findall(step_pattern, steps_section)

    return steps


def _extract_description_from_docstring(docstring: str | None) -> str:
    """
    Extract description from test function docstring, excluding Args and Steps sections.

    Args:
        docstring: The test function's docstring

    Returns:
        Clean description text without Args and Steps sections
    """
    if not docstring:
        return ""

    description = docstring.strip()

    args_pattern = r"\n\s*Args:.*"
    description = re.sub(args_pattern, "", description, flags=re.DOTALL)

    steps_pattern = r"\n\s*Steps:.*"
    description = re.sub(steps_pattern, "", description, flags=re.DOTALL)

    return description.strip()


def _create_environment_properties(allure_dir: Path, config) -> None:
    """
    Create environment.properties file for Allure report with complete info.

    Args:
        allure_dir: Path to allure-results directory
        config: Pytest config object (contains browser info if available)
    """
    import sys
    import platform

    env_file = allure_dir / "environment.properties"

    browser_info = getattr(config, "_browser_info", {})
    browser_name = browser_info.get("name", "Chromium")
    browser_version = browser_info.get("version", "Unknown")
    headless_mode = browser_info.get("headless", "true")

    env_info = {
        "Browser": browser_name,
        "Browser.Version": browser_version,
        "Headless.Mode": headless_mode,
        "Python.Version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "Platform": platform.system(),
        "Platform.Release": platform.release(),
        "Test.Framework": "pytest",
        "Automation.Framework": "Playwright",
    }

    with open(env_file, "w") as f:
        for key, value in env_info.items():
            f.write(f"{key}={value}\n")


def pytest_configure(config):
    """
    Pytest hook that runs during configuration phase.
    Sets the Allure results directory based on the test file location.
    """
    test_paths = config.option.file_or_dir

    if test_paths:
        test_dir = _resolve_test_directory(str(test_paths[0]))
        allure_dir = test_dir / "allure-results"
    else:
        allure_dir = Path(config.rootpath) / "allure-results"

    if not getattr(config.option, "allure_report_dir", None):
        config.option.allure_report_dir = str(allure_dir)
        allure_dir.mkdir(parents=True, exist_ok=True)
        print(f"\n📊 Allure results will be saved to: {allure_dir}")


def pytest_sessionfinish(session, exitstatus):
    """
    Pytest hook that runs after all tests are finished.
    Creates environment.properties with complete info including browser details.
    """
    allure_dir = getattr(session.config.option, "allure_report_dir", None)

    if allure_dir:
        _create_environment_properties(Path(allure_dir), session.config)


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_call(item):
    """
    Hook that wraps the actual test execution.
    Adds suite, title, description, steps, parameter descriptions, and dynamic metadata.
    """

    if hasattr(item, "_allure_suite") and item._allure_suite:
        allure.dynamic.suite(item._allure_suite)

    if hasattr(item, "_allure_title"):
        allure.dynamic.title(item._allure_title)

    if hasattr(item, "_allure_description") and item._allure_description:
        allure.dynamic.description(item._allure_description)

    # Add parameter descriptions for parametrized tests
    if hasattr(item, "callspec"):
        for param_name, param_value in item.callspec.params.items():
            allure.dynamic.parameter(param_name, param_value)

    if hasattr(item, "_allure_steps") and item._allure_steps:
        for step_description in item._allure_steps:
            with allure.step(step_description):
                pass

    _add_dynamic_metadata(item)

    yield


def _add_dynamic_metadata(item):
    """
    Add dynamic tags, severity, and links based on fixtures and markers using configured rules.

    Rules are defined in:
    - FIXTURE_TAG_RULES: Fixture-based tags
    - MARKER_TAG_RULES: Marker-based tags
    - MARKER_SEVERITY_RULES: Marker-based severity levels
    - MARKER_LINK_RULES: Marker-based links (e.g., Jira issues)

    To add new metadata, simply add new rules to these configurations.
    """

    if hasattr(item, "fixturenames"):
        for rule in FIXTURE_TAG_RULES:
            if rule.fixture_name in item.fixturenames:
                allure.dynamic.tag(rule.tag_name)

    for rule in MARKER_TAG_RULES:
        marker = item.get_closest_marker(rule.marker_name)
        if marker and marker.args:
            tag_value = rule.tag_formatter(marker.args[0])
            allure.dynamic.tag(tag_value)

    for rule in MARKER_SEVERITY_RULES:
        marker = item.get_closest_marker(rule.marker_name)
        if marker:
            allure.dynamic.severity(rule.severity)

    for rule in MARKER_LINK_RULES:
        marker = item.get_closest_marker(rule.marker_name)
        if marker and marker.args:
            url = rule.url_formatter(marker.args[0])
            allure.dynamic.link(url, link_type=rule.link_type, name=marker.args[0])


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture test execution outcome.
    Captures screenshot and network errors on failure before fixtures are torn down.
    """
    outcome = yield
    rep = outcome.get_result()

    setattr(item, f"rep_{rep.when}", rep)

    if rep.when == "call" and rep.failed:
        try:
            page = None
            if hasattr(item, "funcargs"):
                page = item.funcargs.get("page")
                if not page:
                    sauce_ui = item.funcargs.get("sauce_ui")
                    if sauce_ui and hasattr(sauce_ui, "page"):
                        page = sauce_ui.page

            if page:
                screenshot_bytes = page.screenshot()
                allure.attach(
                    screenshot_bytes,
                    name="failure_screenshot",
                    attachment_type=allure.attachment_type.PNG,
                )

            if hasattr(item, "_network_errors") and item._network_errors:
                import json

                errors_json = json.dumps(item._network_errors, indent=2)
                allure.attach(
                    errors_json,
                    name="network_errors",
                    attachment_type=allure.attachment_type.JSON,
                    extension="json",
                )
        except Exception as e:
            print(f"Error attaching failure artifacts to Allure: {e}")


def pytest_collection_modifyitems(config, items):
    """
    Modify test items after collection to add Allure metadata.
    """
    for item in items:
        test_module = item.module
        suite_name = getattr(test_module, "TEST_SUITE_NAME", None)

        test_case_name = item.name.replace("test_", "").replace("_", " ").title()

        docstring = item.function.__doc__
        steps = _extract_steps_from_docstring(docstring)
        description = _extract_description_from_docstring(docstring)

        item._allure_suite = suite_name
        item._allure_title = test_case_name
        item._allure_steps = steps
        item._allure_description = description


reporter = AllureReporter()

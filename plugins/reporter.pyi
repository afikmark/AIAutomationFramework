"""
Type stub file for reporter module.
Provides IDE autocomplete for assertpy methods via types-assertpy.
"""

from typing import Any
from collections.abc import Generator
from contextlib import AbstractContextManager
from assertpy.assertpy import AssertionBuilder

class AllureReporter:
    """Allure reporting utilities with step management and assertions."""

    def step(
        self, message: str = "", *args: Any, **kwargs: Any
    ) -> AbstractContextManager[None]:
        """Create an Allure step context manager."""
        ...

    def attach_img(self, screenshot: str | bytes, *args: Any, **kwargs: Any) -> None:
        """Attach a screenshot to the Allure report."""
        ...

    def attach_file(self, file: str, name: str, *args: Any, **kwargs: Any) -> None:
        """Attach a file to the Allure report."""
        ...

    def assert_that(self, actual: Any) -> AllureAssertionBuilder:
        """
        Create an assertion with automatic Allure step.

        Usage:
            reporter.assert_that(page.url).ends_with("/inventory.html")
            reporter.assert_that(value).is_equal_to(10)
        """
        ...

class AllureAssertionBuilder(AssertionBuilder):
    """
    Assertion builder with Allure step reporting.

    Inherits all assertpy methods from AssertionBuilder (via types-assertpy).
    All methods automatically wrap assertions in Allure steps.
    """

    def __init__(self, actual: Any) -> None: ...

# Global reporter instance
reporter: AllureReporter

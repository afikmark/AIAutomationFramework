"""
Xray Test Management MCP Server
Provides tools for interacting with Xray via GraphQL API
"""

from fastmcp import FastMCP
from mcp.types import TextContent
from pathlib import Path
import sys
import json
from typing import Optional
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(BASE_DIR.parent))

from plugins.xray import XrayClient

mcp = FastMCP("XrayTestManagement")

load_dotenv()
client_id = os.getenv("XRAY_CLIENT_ID")
client_secret = os.getenv("XRAY_CLIENT_SECRET")


@mcp.tool()
def xray_get_test(test_key: str) -> str:
    """
    Get test details by Jira issue key.

    Args:
        test_key: Jira test issue key (e.g., "DEV-13")

    Returns:
        JSON string with test details including test type, steps, and metadata
    """
    xray = XrayClient(client_id=client_id, client_secret=client_secret)
    result = xray.get_test_by_key(test_key)
    return json.dumps(result, indent=2)


@mcp.tool()
def xray_get_tests_by_label(label: str, limit: int = 100) -> str:
    """
    Get all tests with a specific label.

    Args:
        label: Label to filter tests by (e.g., "TestPlan-DEV-12")
        limit: Maximum number of results to return (default: 100)

    Returns:
        JSON string with list of tests matching the label
    """
    xray = XrayClient(client_id=client_id, client_secret=client_secret)
    result = xray.get_tests_by_label(label, limit)
    return json.dumps(result, indent=2)


@mcp.tool()
def xray_get_test_plan(plan_key: str) -> str:
    """
    Get test plan details by Jira issue key.

    Args:
        plan_key: Jira test plan key (e.g., "DEV-12")

    Returns:
        JSON string with test plan details including associated tests
    """
    xray = XrayClient(client_id=client_id, client_secret=client_secret)
    result = xray.get_test_plan_by_key(plan_key)
    return json.dumps(result, indent=2)


@mcp.tool()
def xray_add_tests_to_plan(test_plan_id: str, test_issue_ids: str) -> str:
    """
    Add tests to a test plan.

    Args:
        test_plan_id: Test plan issue ID (e.g., "10085")
        test_issue_ids: Comma-separated list of test issue IDs (e.g., "10086,10087,10088")

    Returns:
        JSON string with result of the operation
    """
    xray = XrayClient(client_id=client_id, client_secret=client_secret)
    test_ids = [tid.strip() for tid in test_issue_ids.split(",")]
    result = xray.add_tests_to_test_plan(test_plan_id, test_ids)
    return json.dumps(result, indent=2)


@mcp.tool()
def xray_remove_tests_from_plan(test_plan_id: str, test_issue_ids: str) -> str:
    """
    Remove tests from a test plan.

    Args:
        test_plan_id: Test plan issue ID (e.g., "10085")
        test_issue_ids: Comma-separated list of test issue IDs to remove

    Returns:
        JSON string with result of the operation
    """
    xray = XrayClient(client_id=client_id, client_secret=client_secret)
    test_ids = [tid.strip() for tid in test_issue_ids.split(",")]
    result = xray.remove_tests_from_test_plan(test_plan_id, test_ids)
    return json.dumps(result, indent=2)


@mcp.tool()
def xray_update_test_type(issue_id: str, test_type: str) -> str:
    """
    Update the test type for a test issue.

    Args:
        issue_id: Test issue ID (e.g., "10086")
        test_type: Test type name (e.g., "Manual", "Cucumber", "Generic", "Automated[Generic]")

    Returns:
        JSON string with updated test details
    """
    xray = XrayClient(client_id=client_id, client_secret=client_secret)
    result = xray.update_test_type(issue_id, test_type)
    return json.dumps(result, indent=2)


@mcp.tool()
def xray_update_unstructured_test_definition(issue_id: str, unstructured: str) -> str:
    """
    Update unstructured test definition for a test issue.

    Args:
        issue_id: Test issue ID (e.g., "10086")
        unstructured: Unstructured test definition content (generic test description)

    Returns:
        JSON string with updated test definition details
    """
    xray = XrayClient(client_id=client_id, client_secret=client_secret)
    result = xray.update_unstructured_test_definition(issue_id, unstructured)
    return json.dumps(result, indent=2)


@mcp.tool()
def xray_get_test_execution(execution_id: str) -> str:
    """
    Get test execution details.

    Args:
        execution_id: Test execution issue ID

    Returns:
        JSON string with test execution details including test runs
    """
    xray = XrayClient(client_id=client_id, client_secret=client_secret)
    result = xray.get_test_execution(execution_id)
    return json.dumps(result, indent=2)


@mcp.tool()
def xray_create_test_execution(
    project_key: str,
    summary: str,
    test_plan_key: Optional[str] = None,
    test_environments: Optional[str] = None,
) -> str:
    """
    Create a new test execution.

    Args:
        project_key: Jira project key (e.g., "DEV")
        summary: Summary/title for the test execution
        test_plan_key: Optional test plan key to associate with (e.g., "DEV-12")
        test_environments: Optional comma-separated list of test environments

    Returns:
        JSON string with created test execution details
    """
    xray = XrayClient(client_id=client_id, client_secret=client_secret)
    envs = (
        [e.strip() for e in test_environments.split(",")] if test_environments else None
    )
    result = xray.create_test_execution(project_key, summary, test_plan_key, envs)
    return json.dumps(result, indent=2)


@mcp.tool()
def xray_update_test_run_status(
    test_run_id: str, status: str, comment: Optional[str] = None
) -> str:
    """
    Update test run status.

    Args:
        test_run_id: Test run ID
        status: Status to set - one of: "PASS", "FAIL", "TODO", "EXECUTING"
        comment: Optional comment to add with the status update

    Returns:
        JSON string with updated test run details
    """
    xray = XrayClient(client_id=client_id, client_secret=client_secret)
    result = xray.update_test_run_status(test_run_id, status, comment)
    return json.dumps(result, indent=2)


@mcp.tool()
def xray_search_tests(jql: str, limit: int = 100) -> str:
    """
    Search for tests using JQL query.

    Args:
        jql: JQL query string (e.g., "project = DEV AND type = Test")
        limit: Maximum number of results to return (default: 100)

    Returns:
        JSON string with list of tests matching the query
    """
    xray = XrayClient(client_id=client_id, client_secret=client_secret)
    result = xray.search_tests(jql, limit)
    return json.dumps(result, indent=2)


@mcp.tool()
def xray_search_test_plans(jql: str, limit: int = 100) -> str:
    """
    Search for test plans using JQL query.

    Args:
        jql: JQL query string (e.g., "project = DEV AND type = 'Test Plan'")
        limit: Maximum number of results to return (default: 100)

    Returns:
        JSON string with list of test plans matching the query
    """
    xray = XrayClient(client_id=client_id, client_secret=client_secret)
    result = xray.search_test_plans(jql, limit)
    return json.dumps(result, indent=2)


@mcp.resource(
    uri="xray://test/{test_key}",
    name="XrayTestDetails",
    description="Get detailed information about a specific Xray test by its Jira key",
)
def get_test_resource(test_key: str) -> str:
    """
    Resource for accessing test details.

    Args:
        test_key: Jira test key (e.g., "DEV-13")

    Returns:
        Formatted test details
    """
    xray = XrayClient(client_id=client_id, client_secret=client_secret)
    result = xray.get_test_by_key(test_key)

    if not result:
        return f"Test not found: {test_key}"

    jira_data = result.get("jira", {})
    test_type = result.get("testType", {})

    output = f"""# Test: {jira_data.get('key', 'N/A')}

**Summary:** {jira_data.get('summary', 'N/A')}

**Type:** {test_type.get('name', 'N/A')} ({test_type.get('kind', 'N/A')})

**Description:**
{jira_data.get('description', 'No description available')}

**Labels:** {', '.join(jira_data.get('labels', []))}

**Issue ID:** {result.get('issueId', 'N/A')}
"""
    return output


@mcp.resource(
    uri="xray://testplan/{plan_key}",
    name="XrayTestPlanDetails",
    description="Get detailed information about a specific Xray test plan by its Jira key",
)
def get_test_plan_resource(plan_key: str) -> str:
    """
    Resource for accessing test plan details.

    Args:
        plan_key: Jira test plan key (e.g., "DEV-12")

    Returns:
        Formatted test plan details
    """
    xray = XrayClient(client_id=client_id, client_secret=client_secret)
    result = xray.get_test_plan_by_key(plan_key)

    if not result:
        return f"Test plan not found: {plan_key}"

    jira_data = result.get("jira", {})
    tests = result.get("tests", {})
    test_list = tests.get("results", [])

    output = f"""# Test Plan: {jira_data.get('key', 'N/A')}

**Summary:** {jira_data.get('summary', 'N/A')}

**Description:**
{jira_data.get('description', 'No description available')}

**Total Tests:** {tests.get('total', 0)}

**Associated Tests:**
"""
    for test in test_list:
        test_jira = test.get("jira", {})
        output += (
            f"- {test_jira.get('key', 'N/A')}: {test_jira.get('summary', 'N/A')}\n"
        )

    return output


if __name__ == "__main__":
    mcp.run(transport="stdio")

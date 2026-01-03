"""
Xray GraphQL API Client
Documentation: https://us.xray.cloud.getxray.app/doc/graphql/
"""

import os
import requests
import json
from typing import Dict, List, Optional, Any
from datetime import datetime


class XrayClient:
    """Client for interacting with Xray Test Management via GraphQL API"""

    def __init__(
        self, client_id: Optional[str] = None, client_secret: Optional[str] = None
    ):
        """
        Initialize Xray client with authentication credentials

        Args:
            client_id: Xray API client ID (defaults to XRAY_CLIENT_ID env var)
            client_secret: Xray API client secret (defaults to XRAY_CLIENT_SECRET env var)
        """
        self.client_id = client_id or os.getenv("XRAY_CLIENT_ID")
        self.client_secret = client_secret or os.getenv("XRAY_CLIENT_SECRET")

        if not self.client_id or not self.client_secret:
            raise ValueError(
                "Xray credentials not provided. Set XRAY_CLIENT_ID and XRAY_CLIENT_SECRET"
            )

        self.graphql_url = "https://xray.cloud.getxray.app/api/v2/graphql"
        self.auth_url = "https://xray.cloud.getxray.app/api/v2/authenticate"
        self.token: Optional[str] = None
        self._authenticate()

    def _authenticate(self) -> None:
        """Authenticate with Xray API and obtain bearer token"""
        try:
            response = requests.post(
                self.auth_url,
                json={"client_id": self.client_id, "client_secret": self.client_secret},
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()
            json_response = response.json()
            self.token = (
                json_response
                if isinstance(json_response, str)
                else response.text.strip('"')
            )
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to authenticate with Xray: {str(e)}")

    def _execute_query(self, query: str, variables: Optional[Dict] = None) -> Dict:
        """
        Execute a GraphQL query against Xray API

        Args:
            query: GraphQL query string
            variables: Optional variables for the query

        Returns:
            Response data from the API
        """
        if not self.token:
            self._authenticate()

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

        payload: Dict[str, Any] = {"query": query}
        if variables:
            payload["variables"] = variables

        try:
            response = requests.post(self.graphql_url, json=payload, headers=headers)
            response.raise_for_status()
            result = response.json()

            if "errors" in result:
                raise Exception(
                    f"GraphQL errors: {json.dumps(result['errors'], indent=2)}"
                )

            data: Dict[Any, Any] = result.get("data", {})
            return data
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to execute query: {str(e)}")

    # Test Operations

    def get_test(self, issue_id: str) -> Dict:
        """
        Get test details by issue ID

        Args:
            issue_id: Jira issue ID (e.g., "10123")

        Returns:
            Test details including steps, type, etc.
        """
        query = """
        query GetTest($issueId: String!) {
            getTest(issueId: $issueId) {
                issueId
                jira(fields: ["key", "summary", "description"])
                testType {
                    name
                    kind
                }
                steps {
                    id
                    data
                    action
                    result
                    attachments {
                        id
                        filename
                    }
                }
            }
        }
        """
        return self._execute_query(query, {"issueId": issue_id})

    def get_test_by_key(self, test_key: str) -> Dict:
        """
        Get test details by Jira issue key

        Args:
            test_key: Jira issue key (e.g., "DEV-13")

        Returns:
            Test details
        """
        query = """
        query GetTests($jql: String!, $limit: Int!) {
            getTests(jql: $jql, limit: $limit) {
                total
                results {
                    issueId
                    jira(fields: ["key", "summary", "description", "labels"])
                    testType {
                        name
                        kind
                    }
                    steps {
                        id
                        data
                        action
                        result
                    }
                }
            }
        }
        """
        jql = f'key = "{test_key}"'
        result = self._execute_query(query, {"jql": jql, "limit": 1})

        if result.get("getTests", {}).get("results"):
            test_result: Dict[Any, Any] = result["getTests"]["results"][0]
            return test_result
        return {}

    def get_tests_by_label(self, label: str, limit: int = 100) -> List[Dict]:
        """
        Get tests by label

        Args:
            label: Label to filter by (e.g., "TestPlan-DEV-12")
            limit: Maximum number of results

        Returns:
            List of tests with the specified label
        """
        query = """
        query GetTests($jql: String!, $limit: Int!) {
            getTests(jql: $jql, limit: $limit) {
                total
                results {
                    issueId
                    jira(fields: ["key", "summary", "description", "labels"])
                    testType {
                        name
                        kind
                    }
                }
            }
        }
        """
        jql = f'labels = "{label}" AND type = Test'
        result = self._execute_query(query, {"jql": jql, "limit": limit})
        tests: List[Dict[Any, Any]] = result.get("getTests", {}).get("results", [])
        return tests

    # Test Plan Operations

    def get_test_plan(self, issue_id: str) -> Dict:
        """
        Get test plan details

        Args:
            issue_id: Test plan issue ID

        Returns:
            Test plan details including associated tests
        """
        query = """
        query GetTestPlan($issueId: String!) {
            getTestPlan(issueId: $issueId) {
                issueId
                jira(fields: ["key", "summary", "description"])
                tests(limit: 100) {
                    total
                    results {
                        issueId
                        jira(fields: ["key", "summary"])
                        testType {
                            name
                        }
                    }
                }
            }
        }
        """
        return self._execute_query(query, {"issueId": issue_id})

    def get_test_plan_by_key(self, plan_key: str) -> Dict:
        """
        Get test plan by Jira key

        Args:
            plan_key: Test plan Jira key (e.g., "DEV-12")

        Returns:
            Test plan details
        """
        query = """
        query GetTestPlans($jql: String!, $limit: Int!) {
            getTestPlans(jql: $jql, limit: $limit) {
                total
                results {
                    issueId
                    jira(fields: ["key", "summary", "description"])
                    tests(limit: 100) {
                        total
                        results {
                            issueId
                            jira(fields: ["key", "summary"])
                        }
                    }
                }
            }
        }
        """
        jql = f'key = "{plan_key}"'
        result = self._execute_query(query, {"jql": jql, "limit": 1})

        if result.get("getTestPlans", {}).get("results"):
            plan_result: Dict[Any, Any] = result["getTestPlans"]["results"][0]
            return plan_result
        return {}

    def add_tests_to_test_plan(
        self, test_plan_id: str, test_issue_ids: List[str]
    ) -> Dict:
        """
        Add tests to a test plan

        Args:
            test_plan_id: Test plan issue ID
            test_issue_ids: List of test issue IDs to add

        Returns:
            Result of the operation
        """
        query = """
        mutation AddTestsToTestPlan($issueId: String!, $testIssueIds: [String]!) {
            addTestsToTestPlan(issueId: $issueId, testIssueIds: $testIssueIds) {
                addedTests
                warning
            }
        }
        """
        return self._execute_query(
            query, {"issueId": test_plan_id, "testIssueIds": test_issue_ids}
        )

    def remove_tests_from_test_plan(
        self, test_plan_id: str, test_issue_ids: List[str]
    ) -> Dict:
        """
        Remove tests from a test plan

        Args:
            test_plan_id: Test plan issue ID
            test_issue_ids: List of test issue IDs to remove

        Returns:
            Result of the operation
        """
        query = """
        mutation RemoveTestsFromTestPlan($issueId: String!, $testIssueIds: [String]!) {
            removeTestsFromTestPlan(issueId: $issueId, testIssueIds: $testIssueIds) {
                removedTests
                warning
            }
        }
        """
        return self._execute_query(
            query, {"issueId": test_plan_id, "testIssueIds": test_issue_ids}
        )

    # Test Execution Operations

    def get_test_execution(self, issue_id: str) -> Dict:
        """
        Get test execution details

        Args:
            issue_id: Test execution issue ID

        Returns:
            Test execution details
        """
        query = """
        query GetTestExecution($issueId: String!) {
            getTestExecution(issueId: $issueId) {
                issueId
                jira(fields: ["key", "summary", "description"])
                testRuns(limit: 100) {
                    total
                    results {
                        id
                        status {
                            name
                            color
                        }
                        test {
                            issueId
                            jira(fields: ["key", "summary"])
                        }
                        startedOn
                        finishedOn
                    }
                }
            }
        }
        """
        return self._execute_query(query, {"issueId": issue_id})

    def create_test_execution(
        self,
        project_key: str,
        summary: str,
        test_plan_key: Optional[str] = None,
        test_environments: Optional[List[str]] = None,
    ) -> Dict:
        """
        Create a new test execution

        Args:
            project_key: Jira project key
            summary: Summary for the test execution
            test_plan_key: Optional test plan key to associate with
            test_environments: Optional list of test environments

        Returns:
            Created test execution details
        """
        fields: Dict[str, Any] = {
            "project": {"key": project_key},
            "summary": summary,
            "issuetype": {"name": "Test Execution"},
        }

        if test_plan_key:
            fields["customfield_testplan"] = [test_plan_key]

        if test_environments:
            fields["customfield_testenvironments"] = test_environments

        query = """
        mutation CreateTestExecution($fields: JSON!) {
            createTestExecution(testExecution: {fields: $fields}) {
                testExecution {
                    issueId
                    jira(fields: ["key"])
                }
                warnings
            }
        }
        """
        return self._execute_query(query, {"fields": fields})

    def update_test_run_status(
        self, test_run_id: str, status: str, comment: Optional[str] = None
    ) -> Dict:
        """
        Update test run status

        Args:
            test_run_id: Test run ID
            status: Status to set (e.g., "PASS", "FAIL", "TODO", "EXECUTING")
            comment: Optional comment

        Returns:
            Updated test run details
        """
        query = """
        mutation UpdateTestRunStatus($id: String!, $status: String!, $comment: String) {
            updateTestRunStatus(id: $id, status: $status, comment: $comment) {
                id
                status {
                    name
                }
            }
        }
        """
        variables = {"id": test_run_id, "status": status}
        if comment:
            variables["comment"] = comment

        return self._execute_query(query, variables)

    def update_test_type(self, issue_id: str, test_type: str) -> Dict:
        """
        Update test type for a test issue

        Args:
            issue_id: Test issue ID
            test_type: Test type name (e.g., "Manual", "Cucumber", "Generic", "Automated")

        Returns:
            Updated test details
        """
        query = """
        mutation UpdateTestType($issueId: String!, $testTypeName: String!) {
            updateTestType(issueId: $issueId, testType: { name: $testTypeName }) {
                issueId
                jira(fields: ["key"])
                testType {
                    name
                    kind
                }
            }
        }
        """
        return self._execute_query(
            query, {"issueId": issue_id, "testTypeName": test_type}
        )

    def update_unstructured_test_definition(
        self, issue_id: str, unstructured: str
    ) -> Dict:
        """
        Update unstructured test definition

        Args:
            issue_id: Test issue ID
            unstructured: Unstructured test definition content

        Returns:
            Updated test definition details
        """
        query = """
        mutation UpdateUnstructuredTestDefinition($issueId: String!, $unstructured: String!) {
            updateUnstructuredTestDefinition(issueId: $issueId, unstructured: $unstructured) {
                issueId
                unstructured
            }
        }
        """
        return self._execute_query(
            query, {"issueId": issue_id, "unstructured": unstructured}
        )

    # Search Operations

    def search_tests(self, jql: str, limit: int = 100) -> List[Dict]:
        """
        Search for tests using JQL

        Args:
            jql: JQL query string
            limit: Maximum number of results

        Returns:
            List of tests matching the query
        """
        query = """
        query GetTests($jql: String!, $limit: Int!) {
            getTests(jql: $jql, limit: $limit) {
                total
                results {
                    issueId
                    jira(fields: ["key", "summary", "description", "labels", "status"])
                    testType {
                        name
                        kind
                    }
                }
            }
        }
        """
        result = self._execute_query(query, {"jql": jql, "limit": limit})
        tests: List[Dict[Any, Any]] = result.get("getTests", {}).get("results", [])
        return tests

    def search_test_plans(self, jql: str, limit: int = 100) -> List[Dict]:
        """
        Search for test plans using JQL

        Args:
            jql: JQL query string
            limit: Maximum number of results

        Returns:
            List of test plans matching the query
        """
        query = """
        query GetTestPlans($jql: String!, $limit: Int!) {
            getTestPlans(jql: $jql, limit: $limit) {
                total
                results {
                    issueId
                    jira(fields: ["key", "summary", "description", "status"])
                }
            }
        }
        """
        result = self._execute_query(query, {"jql": jql, "limit": limit})
        plans: List[Dict[Any, Any]] = result.get("getTestPlans", {}).get("results", [])
        return plans

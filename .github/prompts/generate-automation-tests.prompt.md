---
agent: Test Generation Agent
---
## Web Test Workflow:

STEP 1: Gather Context
  ✓ Discover feature documentation - confluence page linked from the user
  ✓ Retrieve architecture guidelines 

STEP 2: Check Existing Code
  ✓ check if page object exists
  ✓ Verify required methods are implemented
  ✓ Check existing test files to avoid duplication

STEP 3: 
✓ Gather Test cases from Jira to understand scenarios to be automated
✓ Identify test steps and expected results
✓ Determine fixture requirements:
  - Use `sauce_ui` for unauthenticated tests (login, logout)
  - Use `logged_in_user` for authenticated tests (cart, inventory, checkout)

STEP 4: Discover Real Selectors (for NEW page objects only)
  ⚠️ DO NOT HALLUCINATE SELECTORS!
    ✓ Use Chrome DevTools MCP to explore the live application (https://www.saucedemo.com/)
  ✅ Use snapshot UIDs and attributes to generate accurate locators
  ❌ Never invent selector values

STEP 5: Generate Test Code
    ✓ Follow architecture guidelines
    ✓ Follow existing code patterns
    ✓ Add TEST_SUITE_NAME constant at module level
    ✓ Use structured docstrings with description and Steps: section
    ✓ Use reporter.assert_that() for all assertions (creates automatic Allure steps)

STEP 6: Write and Verify
  ✓ Write the test code to appropriate files
  ✓ Use correct fixture (sauce_ui or logged_in_user)
  ✓ Add pytest markers for severity and Jira linking:
    - @pytest.mark.sanity (automatic CRITICAL severity)
    - @pytest.mark.test_case_key("JIRA-KEY") (automatic Jira link + tag)
  ✓ Write descriptive test function names (auto-converted to Allure titles)
  ✓ Include structured docstring with:
    - Description (first paragraph)
    - Steps: section with numbered steps (1) Step name)
  ✓ Use reporter.assert_that() for assertions, not plain assert
  ✓ Activate venv before running tests
  ✓ Run tests with Allure reporting: `uv run pytest tests/ --alluredir=allure-results`
  ✓ Fix any failures before finishing

Example Test Structure:
```python
from plugins.reporter import reporter

TEST_SUITE_NAME = "Feature Name Tests"

@pytest.mark.sanity
@pytest.mark.test_case_key("DEV-123")
def test_specific_scenario(logged_in_user):
    """Brief description of what the test validates.
    
    Detailed explanation if needed.
    
    Steps:
        1) First action
        2) Second action
        3) Verify expected result
    """
    # Test implementation using reporter.assert_that()
    logged_in_user.page_object.perform_action()
    reporter.assert_that(result).is_equal_to(expected)
```

## API Test Workflow:

STEP 1: Gather Context
  ✓ Discover API endpoint documentation - confluence page linked from the user
  ✓ Retrieve architecture guidelines
  ✓ Use Postman MCP server to explore API collections

STEP 2: Check Existing Code
  ✓ Check if controller/schema exists
  ✓ Verify required methods/schemas are implemented
  ✓ Check existing test files to avoid duplication

STEP 3: Generate Test Code
  ✓ Follow architecture guidelines
  ✓ Follow existing code patterns
  ✓ Use appropriate schemas and controllers
  ✓ Include proper assertions and error handling
  ✓ Test both success and error scenarios
  ✓ Validate response schemas
  ✓ Check status codes and error messages

STEP 4: Write and Verify
  ✓ Write the test code to appropriate files
  ✓ Activate venv before running tests
  ✓ Fix any failures before finishing

## Architecture Guidelines docs:
contexts/architecture-guidelines.md
## Feature Documentation:
confluence page linked from the user 
## Existing Codebase:
repository root directory
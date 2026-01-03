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
✓ Gether Test cases from Jira to understand scenarios to be automated
✓ Identify test steps and expected results

STEP 4: Discover Real Selectors (for NEW page objects only)
  ⚠️ DO NOT HALLUCINATE SELECTORS!
    ✓ Use Chrome DevTools MCP to explore the live application (https://www.saucedemo.com/)
  ✅ Use snapshot UIDs and attributes to generate accurate locators
  ❌ Never invent selector values

STEP 5: Generate Test Code
    ✓ Follow architecture guidelines
    ✓ Follow existing code patterns

STEP 6: Write and Verify
  ✓ write the test code to appropriate files
  ✓ Activate venv before running tests
  ✓ Fix any failures before finishing
  ✓ Add test_case_key marker with the Jira Test Case Key to each test

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
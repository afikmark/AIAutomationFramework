from fastmcp import FastMCP
from fastmcp.prompts import PromptMessage
from mcp.types import TextContent
from pathlib import Path
import sys


BASE_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(BASE_DIR.parent))


mcp = FastMCP("AutomationTestServer")


@mcp.prompt(
    name="GenerateTestRequest",
    title="Generate Test Request",
    description="Generates a test request for a given feature. You have access to all registered MCP servers including Chrome DevTools.",
    meta={"servers": "chrome-devtools"},
)
def generate_test_request(query: str) -> PromptMessage:
    """Create a request template to generate pytest-playwright tests for a feature."""
    content = f"""You are an expert Python QA engineer with access to multiple MCP servers.
Generate concise, correct pytest-playwright tests for this repository following its conventions.

📋 WORKFLOW:

STEP 1: Gather Context
  ✓ Discover feature documentation
  ✓ Retrieve architecture guidelines 

STEP 2: Check Existing Code
  ✓ check if page object exists
  ✓ Verify required methods are implemented
  ✓ Check existing test files to avoid duplication

STEP 3: Discover Real Selectors (for NEW page objects only)
  ⚠️ DO NOT HALLUCINATE SELECTORS!
    ✓ Use Chrome DevTools MCP to explore the live application (https://www.saucedemo.com/)
  ✅ Use snapshot UIDs and attributes to generate accurate locators
  ❌ Never invent selector values

STEP 4: Generate Test Code
    ✓ Follow architecture guidelines
    ✓ Follow existing code patterns
  

STEP 5: Write and Verify
  ✓ write the test code to appropriate files
  ✓ Activate venv before running tests
  ✓ Fix any failures before finishing

⚙️ RULES:

Context Retrieval:
  ✓ ALWAYS use get_test_context for documentation (NOT read_file for context docs)

Code Quality:
  ✓ Do not delete existing tests
  ✓ Do not duplicate tests
  ✓ Follow existing code patterns

Selector Strategy:
  ✓ Prefer accessible selectors (get_by_role, get_by_label, get_by_text)
  ✓ Use data-test-id attributes when available
  ✓ Validate selectors with Chrome DevTools before using
  ✓ Never hallucinate selector values

🎯 USER REQUEST:
{query}

Remember: You have access to ALL registered MCP servers.
"""
    return PromptMessage(role="user", content=TextContent(type="text", text=content))


@mcp.resource(
    uri="context://feature/{feature_name}",
    name="FeatureDocumentation",
    description="Pre-loaded feature documentation ready for test generation.",
)
def get_feature_documentation(feature_name: str) -> str:
    """
    Get feature documentation from pre-loaded context files.

    Available features:
    - saucedemo_login_page
    - saucedemo_inventory_page
    - saucedemo_cart_page
    - saucedemo_checkout_page
    - saucedemo_payment_page
    - saudedemo_hamburger_menu
    """
    file_path = (
        BASE_DIR.parent
        / "contexts"
        / "product_context_docs"
        / f"saucedemo_{feature_name}.md"
    )
    if not file_path.exists():
        return f"# Feature documentation not found for: {feature_name}"
    return file_path.read_text(encoding="utf-8")


@mcp.resource(
    uri="context://guideline/{guideline_name}",
    name="GuidelineDocumentation",
    description="Pre-loaded guideline documentation for test generation.",
)
def get_guideline_documentation(guideline_name: str) -> str:
    """
    Get guideline documentation from pre-loaded context files.

    Available guidelines:
    - test_generation
    - test_organization
    - page_object_model
    - fixtures
    - component_pattern
    - selector_discovery
    """
    file_path = (
        BASE_DIR.parent
        / "contexts"
        / "architecture_context_docs"
        / f"{guideline_name}.md"
    )
    if not file_path.exists():
        return f"# Guideline documentation not found for: {guideline_name}"
    return file_path.read_text(encoding="utf-8")


if __name__ == "__main__":
    mcp.run(transport="stdio")

from fastmcp import FastMCP
from pathlib import Path
import sys


BASE_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(BASE_DIR.parent))


mcp = FastMCP("AutomationTestContextServer")


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


@mcp.resource(
    uri="context://api/{api_name}",
    name="ApiDocumentation",
    description="Pre-loaded API documentation ready for test generation.",
)
def get_api_documentation(api_name: str) -> str:
    """
    Get API documentation from pre-loaded context files.

    Available APIs:
    - pet_store (overview)
    - pet_store_authorization
    - pet_store_pet
    - pet_store_store
    - pet_store_user
    """
    file_path = BASE_DIR.parent / "contexts" / "product_context_docs" / f"{api_name}.md"
    if not file_path.exists():
        return f"# API documentation not found for: {api_name}"
    return file_path.read_text(encoding="utf-8")


@mcp.tool()
def get_architecture_guidelines(guideline_name: str) -> str:
    """
    Fetch architecture guideline documentation for test creation.

    Args:
        guideline_name: Name of the guideline document

    Available guidelines:
    - test_generation: Guidelines for generating test code
    - test_organization: How to organize test files and structure
    - page_object_model: Page Object Model pattern implementation
    - fixtures: Pytest fixtures and setup/teardown patterns
    - component_pattern: Component pattern for reusable UI elements
    - selector_discovery: How to discover and validate selectors

    Returns:
        The guideline documentation content
    """
    file_path = (
        BASE_DIR.parent
        / "contexts"
        / "architecture_context_docs"
        / f"{guideline_name}.md"
    )
    if not file_path.exists():
        return f"# Guideline documentation not found for: {guideline_name}\n\nAvailable guidelines: test_generation, test_organization, page_object_model, fixtures, component_pattern, selector_discovery"
    return file_path.read_text(encoding="utf-8")


@mcp.tool()
def get_feature_context(feature_name: str) -> str:
    """
    Fetch feature documentation for test creation.

    Args:
        feature_name: Name of the feature (without 'saucedemo_' prefix for web features)

    Available web features:
    - login_page: Login page functionality
    - inventory_page: Product inventory/listing page
    - cart_page: Shopping cart page
    - checkout_page: Checkout flow
    - payment_page: Payment processing
    - hamburger_menu: Navigation menu component

    Available API features (use full name):
    - pet_store: Pet Store API overview
    - pet_store_authorization: Authentication endpoints
    - pet_store_pet: Pet management endpoints
    - pet_store_store: Store/order endpoints
    - pet_store_user: User management endpoints

    Returns:
        The feature documentation content
    """
    # Try saucedemo web feature first
    web_path = (
        BASE_DIR.parent
        / "contexts"
        / "product_context_docs"
        / f"saucedemo_{feature_name}.md"
    )
    if web_path.exists():
        return web_path.read_text(encoding="utf-8")

    # Try API feature
    api_path = (
        BASE_DIR.parent / "contexts" / "product_context_docs" / f"{feature_name}.md"
    )
    if api_path.exists():
        return api_path.read_text(encoding="utf-8")

    return f"# Feature documentation not found for: {feature_name}\n\nTry: login_page, inventory_page, cart_page, checkout_page, hamburger_menu (for web) or pet_store, pet_store_pet, pet_store_user (for API)"


@mcp.tool()
def list_available_contexts() -> dict:
    """
    List all available feature and guideline documentation.

    Returns:
        Dictionary with available web features, API features, and architecture guidelines
    """
    return {
        "web_features": [
            "login_page",
            "inventory_page",
            "cart_page",
            "checkout_page",
            "payment_page",
            "hamburger_menu",
        ],
        "api_features": [
            "pet_store",
            "pet_store_authorization",
            "pet_store_pet",
            "pet_store_store",
            "pet_store_user",
        ],
        "architecture_guidelines": [
            "test_generation",
            "test_organization",
            "page_object_model",
            "fixtures",
            "component_pattern",
            "selector_discovery",
        ],
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")

from mcp.server.fastmcp import FastMCP
from mcp.types import PromptMessage, TextContent
from pathlib import Path
import sys
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
import hashlib
import asyncio


BASE_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(BASE_DIR.parent))

from rag_engine.rag import Rag

mcp = FastMCP("AutomationTestServer")


@mcp.prompt(
    name="GenerateTestRequest",
    description="Generates a test request for a given feature. You have access to all registered MCP servers including Chrome DevTools.",
)
def generate_test_request(query: str) -> PromptMessage:
    """Create a request template to generate pytest-playwright tests for a feature."""
    content = f"""You are an expert Python QA engineer with access to multiple MCP servers.
Generate concise, correct pytest-playwright tests for this repository following its conventions.

🔧 AVAILABLE MCP TOOLS FROM MULTIPLE SERVERS:

1. **Test Context Tools** (automation_generator_mcp):
   - get_test_context(feature, guidelines, n_results_per_query) → Returns focused contexts
   - create_chunks(elements, separators, content_type) → Create document chunks
   - rag_query(chunks, question, n_results) → Query RAG system

2. **Chrome DevTools Tools** (chrome-devtools MCP):
   - list_pages() → List all open browser pages
   - new_page(url) → Open a new page with URL
   - navigate_page(type, url) → Navigate to URL or back/forward
   - take_snapshot(verbose) → Get page structure with element UIDs
   - click(uid) → Click an element by UID
   - fill(uid, value) → Fill input/textarea by UID
   - evaluate_script(function, args) → Run JavaScript on page
   - get_console_message(msgid) → Get console messages
   - list_network_requests() → List network requests
   
3. **VS Code Tools** (built-in):
   - read_file(filePath) → Read file contents
   - replace_string_in_file(filePath, oldString, newString) → Edit files
   - create_file(filePath, content) → Create new files
   - run_in_terminal(command, explanation, isBackground) → Run terminal commands

📋 WORKFLOW:

STEP 1: Gather Context
  ✓ Call get_test_context(feature="<feature_name>") to retrieve:
    - Feature behavior and user actions
    - Test generation patterns
    - Fixture usage examples
    - Page Object Model examples

STEP 2: Check Existing Code
  ✓ Use read_file() to check if page object exists
  ✓ Verify required methods are implemented
  ✓ Check existing test files to avoid duplication

STEP 3: Discover Real Selectors (for NEW page objects only)
  ⚠️ DO NOT HALLUCINATE SELECTORS!
  
  If page object needs new selectors:
    a) new_page("https://www.saucedemo.com") OR navigate_page(type="url", url="...")
    b) take_snapshot() to get page structure with UIDs
    c) Identify elements and their attributes from snapshot
    d) Use Playwright locators (get_by_role, get_by_label, get_by_text)
    e) Optionally use evaluate_script() to test JavaScript selectors
  
  ✅ Use snapshot UIDs and attributes to generate accurate locators
  ❌ Never invent selector values

STEP 4: Generate Test Code
  ✓ Follow pytest conventions
  ✓ Use fixtures (sauce_ui) from conftest.py
  ✓ Use @pytest.mark.parametrize for data-driven tests
  ✓ Add descriptive assertions
  ✓ Follow Page Object Model pattern

STEP 5: Write and Verify
  ✓ Use create_file() or replace_string_in_file() to write tests
  ✓ Use run_in_terminal() to run: pytest <test_file> -v

⚙️ RULES:

Context Retrieval:
  ✓ ALWAYS use get_test_context for documentation (NOT read_file for context docs)
  ✓ Only read_file for verifying code structure
  ✓ Prefer get_test_context over manual chunking

Code Quality:
  ✓ Do not delete existing tests
  ✓ Do not duplicate tests
  ✓ Follow existing code patterns
  ✓ Use proper error handling

Selector Strategy:
  ✓ Prefer accessible selectors (get_by_role, get_by_label, get_by_text)
  ✓ Use data-test-id attributes when available
  ✓ Validate selectors with Chrome DevTools before using
  ✓ Never hallucinate selector values

Testing:
  ✓ Activate venv before running tests: source .venv/bin/activate
  ✓ Run tests to verify they work
  ✓ Fix any failures before finishing

🎯 USER REQUEST:
{query}

Remember: You have access to ALL registered MCP servers. Use Chrome DevTools to discover real selectors, not imagined ones!
"""
    return PromptMessage(role="user", content=TextContent(type="text", text=content))


# Cache for RAG instances to avoid recreating vector DBs
_rag_cache: dict[str, Rag] = {}


def _get_content_hash(content: str) -> str:
    """Generate hash of content for caching."""
    return hashlib.md5(content.encode()).hexdigest()[:16]


def _load_feature_doc(feature_name: str) -> str:
    """Load feature documentation from file."""
    file_path = (
        BASE_DIR.parent
        / "contexts"
        / "product_context_docs"
        / f"saucedemo_{feature_name}.md"
    )
    if not file_path.exists():
        return f"# Feature documentation not found for: {feature_name}"
    return file_path.read_text(encoding="utf-8")


def _load_guideline_doc(guideline_name: str) -> str:
    """Load guideline documentation from file."""
    file_path = (
        BASE_DIR.parent
        / "contexts"
        / "architecture_context_docs"
        / f"{guideline_name}.md"
    )
    if not file_path.exists():
        return f"# Guideline documentation not found for: {guideline_name}"
    return file_path.read_text(encoding="utf-8")


@mcp.tool(
    "create_chunks",
    description="Creates a document and splits it into smaller chunks for embedding with adaptive sizing.",
)
def create_chunks(
    elements: list[str],
    separators: list[str] | None = None,
    content_type: str = "documentation",
) -> list[Document]:
    """
    Split text into smaller chunks for embedding with adaptive chunk sizing.

    Args:
        elements: List of text content to chunk
        separators: List of separators for splitting (default: markdown-optimized)
        content_type: Type of content - "code", "api_reference", or "documentation"

    Returns:
        List of Document chunks
    """
    # Adaptive chunk sizing based on content type
    if content_type == "code":
        chunk_size, overlap = 1200, 180  # Code needs more context
    elif content_type == "api_reference":
        chunk_size, overlap = 800, 120  # API docs can be smaller
    else:
        chunk_size, overlap = 1000, 150  # Default for mixed content

    if separators is None:
        separators = ["\n\n## ", "\n\n### ", "\n\n", "\n", " ", ""]

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        separators=separators,
    )
    doc = Document(page_content="\n".join(elements))
    chunks = text_splitter.split_documents([doc])
    return chunks


@mcp.tool(
    "rag_query",
    description="Queries the RAG system with a user question and returns relevant information. Uses caching for efficiency.",
)
def rag_query(
    chunks: list[Document],
    question: str,
    n_results: int = 5,
    force_recreate: bool = False,
    persist: bool = True,
) -> str:
    """
    Queries the RAG system with a user question and returns relevant information.

    Args:
        chunks: Document chunks to search
        question: Query question
        n_results: Number of results to return (default: 5 for better coverage)
        force_recreate: Force recreation of vector DB (default: False for caching)
        persist: Persist vector DB to disk (default: True for reuse)

    Returns:
        Concatenated relevant context from top matches
    """
    # Generate cache key from chunks content
    content = "".join([chunk.page_content for chunk in chunks])
    cache_key = _get_content_hash(content)

    # Check cache first
    if cache_key in _rag_cache and not force_recreate:
        rag = _rag_cache[cache_key]
        print(f"Using cached RAG instance: {cache_key}")
    else:
        # Create new RAG instance
        db_path = str(BASE_DIR / "rag_db" / cache_key)
        rag = Rag(
            db_path=db_path,
            chunks=chunks,
            embeddings=OllamaEmbeddings(model="llama3"),
            force_recreate=force_recreate,
            persist=persist,
        )
        # Cache for reuse
        if persist:
            _rag_cache[cache_key] = rag

    results = rag.query_rag(query=question, n_results=n_results)
    return results


@mcp.tool(
    "get_test_context",
    description="Efficient single-call context retrieval. Combines multiple documents into a single RAG instance and returns focused contexts for test generation.",
)
def get_test_context(
    feature: str,
    guidelines: list[str] | None = None,
    n_results_per_query: int = 5,
) -> dict[str, str]:
    """
    Efficient single-call context retrieval for test generation.
    Combines multiple documents into a single RAG instance for optimal performance.

    Args:
        feature: Feature name to generate tests for (e.g., "saucedemo_inventory_page")
        guidelines: List of guideline names to include (default: ["test_generation", "fixtures", "page_object_model"])
        n_results_per_query: Number of results per query (default: 5)

    Returns:
        Dictionary with focused contexts:
        - feature_behavior: Feature-specific behavior and actions
        - test_patterns: Test generation patterns and best practices
        - fixture_usage: Fixture usage examples and patterns
        - pom_examples: Page Object Model examples and locators
    """
    # Default guidelines
    if guidelines is None:
        guidelines = ["test_generation", "fixtures", "page_object_model"]

    # Load all documents
    docs_content = [_load_feature_doc(feature)] + [
        _load_guideline_doc(g) for g in guidelines
    ]

    # Single chunking with optimal settings for documentation
    chunks = create_chunks(docs_content, content_type="documentation")

    # Generate cache key for this specific combination
    content = "".join(docs_content)
    cache_key = _get_content_hash(content)

    # Check cache or create new RAG
    if cache_key in _rag_cache:
        rag = _rag_cache[cache_key]
        print(f"Using cached RAG instance for test context: {cache_key}")
    else:
        db_path = str(BASE_DIR / "rag_db" / cache_key)
        rag = Rag(
            db_path=db_path,
            chunks=chunks,
            embeddings=OllamaEmbeddings(model="llama3"),
            force_recreate=False,
            persist=True,
        )
        _rag_cache[cache_key] = rag

    # Multiple focused queries against SAME vector DB
    return {
        "feature_behavior": rag.query_rag(
            f"{feature} user actions behavior sorting adding removing items",
            n_results=n_results_per_query,
        ),
        "test_patterns": rag.query_rag(
            "pytest function-based tests parametrize fixture usage assert",
            n_results=max(n_results_per_query - 1, 1),
        ),
        "fixture_usage": rag.query_rag(
            "sauce_ui fixture page objects access methods navigate",
            n_results=max(n_results_per_query - 2, 1),
        ),
        "pom_examples": rag.query_rag(
            "page object methods locators get_by_role click fill",
            n_results=max(n_results_per_query - 2, 1),
        ),
    }


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
    return _load_feature_doc(feature_name)


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
    return _load_guideline_doc(guideline_name)


@mcp.resource(
    uri="mcp://available-servers",
    name="AvailableMCPServers",
    description="Lists all MCP servers configured in this workspace and their capabilities.",
)
def get_available_mcp_servers() -> str:
    """
    Returns information about all MCP servers configured in the workspace.
    This helps AI assistants discover and use tools from multiple servers.
    """
    return """
# Available MCP Servers

This workspace has multiple MCP servers registered in `.vscode/mcp.json`:

## 1. automation_generator_mcp (This Server)
**Purpose**: Test generation with RAG-based context retrieval

**Tools**:
- `create_chunks(elements, separators, content_type)`: Split text into chunks for embedding
- `rag_query(chunks, question, n_results)`: Query RAG system for relevant information
- `get_test_context(feature, guidelines, n_results_per_query)`: Efficient single-call context retrieval

**Prompts**:
- `GenerateTestRequest(query)`: Main prompt for test generation with multi-server support

**Resources**:
- `context://feature/{feature_name}`: Feature documentation
- `context://guideline/{guideline_name}`: Testing guidelines

## 2. chrome-devtools
**Purpose**: Browser automation and inspection

**Tool Prefix**: `mcp_chrome-devtoo_` or `mcp_chromedevtool_`

**Common Tools**:
- `list_pages()`: List browser pages
- `new_page(url)`: Open new page
- `navigate_page(type, url)`: Navigate to URL
- `take_snapshot(verbose)`: Get page structure with UIDs
- `click(uid)`: Click element
- `fill(uid, value)`: Fill input
- `evaluate_script(function, args)`: Run JavaScript
- `list_network_requests()`: List network requests
- `list_console_messages()`: Get console messages

**Use Cases**:
- Discover real DOM selectors
- Inspect page structure
- Validate element existence
- Debug web applications

## How to Use Multiple Servers

When using the `GenerateTestRequest` prompt, Copilot automatically has access to ALL tools from ALL servers.

**Example Workflow**:
1. Use `get_test_context` to get test patterns (automation_generator_mcp)
2. Use `new_page` + `take_snapshot` to discover selectors (chrome-devtools)
3. Use built-in VS Code tools to write/edit files
4. Use `run_in_terminal` to execute tests

**Important**: Tool names are prefixed by their server:
- automation_generator_mcp tools: `mcp_automation_ge_<tool_name>`
- chrome-devtools tools: `mcp_chromedevtool_<tool_name>` or `mcp_chrome-devtoo_<tool_name>`
"""


if __name__ == "__main__":
    mcp.run(transport="stdio")

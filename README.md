# AI-Driven Test Automation Framework

> An end-to-end AI-powered test automation framework featuring agentic workflows, custom MCP servers, and GitHub Copilot integration for intelligent test generation, management, and code review

[![Python](https://img.shields.io/badge/Python-3.12%2B-blue.svg)](https://www.python.org/downloads/)
[![Playwright](https://img.shields.io/badge/Playwright-Latest-green.svg)](https://playwright.dev/)
[![Pytest](https://img.shields.io/badge/Pytest-9.0%2B-orange.svg)](https://pytest.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![MCP](https://img.shields.io/badge/MCP-Enabled-brightgreen.svg)](https://modelcontextprotocol.io/)
[![Build Status](http://192.168.1.216:8080/job/automation-pipeline/job/main/badge/icon)](http://192.168.1.216:8080/job/automation-pipeline/job/main/)
[![Build Status](http://192.168.1.216:8080/buildStatus/icon?job=automation-pipeline%2Fmain)](http://192.168.1.216:8080/job/automation-pipeline/job/main/)

---

## 🎯 Overview

This project demonstrates a complete AI-driven test automation workflow, from test design through deployment. By integrating Model Context Protocol (MCP) servers, GitHub Copilot Agents, and custom prompts, it enables AI assistants to generate production-ready tests following project-specific architecture patterns and best practices.

### 🚀 Complete AI-Agentic Workflow

**📋 Test Design** → **📊 Test Management** → **🤖 Test Generation** → **🔍 Code Review** → **🚀 Deployment**

1. **📋 Test Design** - Define test requirements and scenarios using AI agents
2. **📊 Test Management** - Create and manage test cases in Jira & Xray via GraphQL API
3. **🤖 Test Generation** - AI-powered test creation using architecture guidelines and feature docs
4. **🔍 Code Review** - Automated review following best practices and conventions
5. **🚀 Deployment** - CI/CD ready with proper git workflows and conventional commits

---

## ✨ Key Features

### 🔌 Custom MCP Servers

#### 1. **Test Context Server**
Provides AI agents with access to:
- Architecture guidelines (Page Object Model, fixtures, component patterns)
- Feature documentation (UI and API specifications)
- Test generation templates and best practices

#### 2. **Xray Test Management Server**
Integrates with Jira/Xray via GraphQL:
- Create and manage test cases
- Execute test runs and update test status (PASS/FAIL/TODO/EXECUTING)
- Link tests to test plans and executions
- Query test metadata and coverage
- Retrieve test execution details and results

### 🤖 GitHub Copilot Integration

- **Custom Agents**: Specialized AI agents for different automation tasks
- **Custom Prompts**: Pre-configured prompts for common workflows (test generation, code review, git operations)
- **Context-Aware**: Agents understand your project's architecture patterns

### 🎭 Test Automation Stack

- **UI Testing**: Playwright with Page Object Model
- **API Testing**: RESTful API testing with Pydantic validation
- **Test Management**: Pytest with Xray integration
- **Browser Support**: Chromium, Firefox, WebKit
- **📊 Reporting**: Allure reports with rich test documentation
- **🔐 Authentication**: Reusable auth state for faster test execution
- **⚙️ Configuration**: Flexible base URL configuration via CLI and environment variables

### 🆕 Recent Enhancements

#### Allure Reporting Integration
- **Rich HTML Reports**: Interactive test execution reports with screenshots, logs, and attachments
- **Network Tracking**: Automatic capture of failed network requests (400+ status codes)
- **Screenshot Capture**: Automatic screenshots on test failure
- **Custom Metadata**: Test case keys, severity, and suite information
- **Generate & View**: `uv run pytest --alluredir=allure-results && allure serve allure-results`

#### Authentication State Management
- **Reusable Auth State**: Login once per test session, reuse across all authenticated tests
- **Faster Execution**: Skip redundant login steps, reducing test execution time by ~70%
- **Headless Auth Creation**: Authentication state always created in headless mode for stability
- **Fixture-Based**: Simple `logged_in_user` fixture provides authenticated browser context
- **Auto-Cleanup**: Auth state automatically recreated when session changes

#### Base URL Configuration
- **CLI Override**: `--base-url` flag to run tests against different environments
- **Environment Variable**: Set `BASE_URL` in `.env` for default configuration
- **Per-Test Flexibility**: Configure base URL per test suite or test
- **Example**: `uv run pytest --base-url=https://staging.example.com tests/`


---

## 🛠️ Tech Stack

### Core Technologies

| Technology | Purpose | Version |
|------------|---------|---------|
| **Python** | Primary language | 3.12+ |
| **Playwright** | Browser automation | Latest |
| **Pytest** | Testing framework | 9.0+ |
| **Pydantic** | Data validation | Latest |
| **Requests** | HTTP client | Latest |
| **Allure-Pytest** | Test reporting | 2.15.3 |

### MCP & AI Integration

| Component | Purpose |
|-----------|---------|
| **MCP Servers** | Context provision for AI agents |
| **GitHub Copilot** | AI-powered code generation |
| **Custom Agents** | Specialized automation assistants |

### Test Management

| Tool | Purpose |
|------|---------|
| **Jira** | Test case management |
| **Xray** | Test execution & reporting |
| **GraphQL** | API integration |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.12 or higher (managed via [uv](https://docs.astral.sh/uv/))
- Git
- Visual Studio Code (for GitHub Copilot integration)

### Installation

#### **Linux / macOS**

```bash
# Clone the repository
git clone https://github.com/afikmark/AIAutomationFramework.git
cd AIAutomationFramework

# Install dependencies and create virtual environment with uv
uv sync --python 3.12

# Install Playwright browsers
uv run playwright install
```

#### **Windows**

```powershell
# Clone the repository
git clone https://github.com/afikmark/AIAutomationFramework.git
cd AIAutomationFramework

# Install dependencies and create virtual environment with uv
uv sync --python 3.12

# Install Playwright browsers
uv run playwright install
```

---

## ⚙️ Configuration

### 1. Environment Setup

Create a `.env` file in the root directory based on `.env.example`:

```bash
# Copy the example file and update with your credentials
cp .env.example .env
```

Then edit `.env` with your actual credentials:
- `JIRA_TOKEN` - Your Jira API token for authentication
- `XRAY_CLIENT_ID` - Xray Cloud client ID (if using Xray Cloud)
- `XRAY_CLIENT_SECRET` - Xray Cloud client secret
- `POSTMAN_API_KEY` - Postman API key for collection management
- `PET_STORE_API_KEY` - Pet Store API key (if required)
- `BASE_URL` - Default base URL for UI tests (optional)

### 2. MCP Server Configuration for VS Code & GitHub Copilot

The project includes two custom MCP servers that enable GitHub Copilot to:
- Generate tests using project-specific architecture guidelines
- Manage test cases in Jira/Xray
- Follow Page Object Model patterns
- Handle test execution results

#### **Configure VS Code MCP Settings**

Create or update `.vscode/mcp.json` in your workspace:

```json
{
  "servers": {
    "test-context-server": {
      "type": "stdio",
      "command": "/absolute/path/to/AIAutomationFramework/.venv/bin/python",
      "args": [
        "/absolute/path/to/AIAutomationFramework/mcp_server/test_context_server.py"
      ],
      "description": "Provides architecture guidelines and feature documentation for test generation"
    },
    "xray-server": {
      "type": "stdio",
      "command": "/absolute/path/to/AIAutomationFramework/.venv/bin/python",
      "args": [
        "/absolute/path/to/AIAutomationFramework/mcp_server/xray_server.py"
      ],
      "env": {
        "JIRA_BASE_URL": "https://your-domain.atlassian.net",
        "JIRA_EMAIL": "your-email@example.com",
        "JIRA_API_TOKEN": "your_api_token"
      },
      "description": "Xray test management operations via GraphQL API"
    },
    "chrome-devtools": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@latest"],
      "description": "Chrome DevTools for element selector discovery"
    }
  }
}
```

**Important**: 
- Replace `/absolute/path/to/AIAutomationFramework` with your actual project path
- **Linux/macOS**: Use `.venv/bin/python`
- **Windows**: Use `.venv\Scripts\python.exe`
- Update Xray credentials in the `env` section

#### **Available MCP Tools**

**Test Context Server:**
- `get_architecture_guidelines` - Retrieve test patterns (Page Object Model, fixtures, components)
- `get_feature_context` - Get feature documentation for UI/API endpoints
- `list_available_contexts` - List all available documentation

**Xray Server:**
- `xray_create_test_execution` - Create new test execution in Xray
- `xray_get_test_execution` - Retrieve test execution details
- `xray_update_test_run_status` - Update test result (PASS/FAIL/TODO/EXECUTING)
- `xray_get_test` - Get test case details
- `xray_get_test_plan` - Retrieve test plan information
- Additional tools for test management (see [xray_server.py](mcp_server/xray_server.py))

---

## 📖 Usage

### 🤖 AI-Powered Test Generation Workflow

The framework provides intelligent test generation through GitHub Copilot Agents with custom prompts and MCP context.

#### **Step 1: Choose an Agent**

Select a GitHub Copilot Agent from `.github/agents/`:
- **Jira QA Agent** - For test design and Jira integration
- **Test Generation Agent** - For creating tests with architecture patterns
- **Code Review Agent** - For reviewing code against best practices
- **Git Operations Agent** - For managing git workflows

#### **Step 2: Use Custom Prompts**

Reference prompt files in your conversation with the agent:

**Example: Test Design with Jira QA Agent**
```
@jira-qa-agent
Generate test scenarios for the checkout page feature

#file:test-design.prompt.md
```

**Example: Generate Tests**
```
@test-generation-agent
Create comprehensive tests for the Cart Page following architecture guidelines

#file:test-generation.prompt.md
```

**Example: Code Review**
```
@code-review-agent
Review the test files in tests/sauce_ui/ directory

#file:code-review.prompt.md
```

**Example: Git Operations**
```
@git-operations-agent
Stage and commit the new test files with conventional commit message

#file:git-operations.prompt.md
```

#### **Step 3: AI Agent Workflow**

The agent will automatically:
1. Load the referenced prompt instructions
2. Access relevant context via MCP servers (guidelines, feature docs)
3. Generate or review code following project patterns
4. Execute tests to validate functionality
5. Update Xray test results (if configured)

### 🎯 Complete Example: End-to-End Test Creation

**1. Design Tests (Jira QA Agent)**
```
@jira-qa-agent
I need to create test cases for user login functionality including:
- Valid credentials
- Invalid credentials  
- Locked out users
- Performance glitch scenario

Create test cases in Jira project DEV and add to test plan DEV-10

#file:test-design.prompt.md
```

**2. Generate Tests (Test Generation Agent)**
```
@test-generation-agent
Generate pytest tests for the login page test cases we just created in Jira.
Follow Page Object Model pattern and use the logged_in_user fixture where appropriate.

#file:test-generation.prompt.md
```

**3. Review Code (Code Review Agent)**  
```
@code-review-agent
Review the newly generated login page tests for:
- Architecture compliance
- Best practices
- Test coverage

#file:code-review.prompt.md
```

**4. Commit Changes (Git Agent)**
```
@git-operations-agent
Create a feature branch, stage the test files, and commit with proper conventional commit message

#file:git-operations.prompt.md
```

### 🧪 Running Tests Locally

```bash
# Run all tests
uv run pytest

# Run specific test suite
uv run pytest tests/sauce_ui/
uv run pytest tests/pet_store_api/

# Run with specific markers
uv run pytest -m sanity

# Run with Allure reporting
uv run pytest tests/ --alluredir=allure-results

# Generate and view Allure report
allure serve allure-results

# Run tests with custom base URL
uv run pytest --base-url=https://staging.saucedemo.com tests/sauce_ui/

# Run in headed mode (visible browser)
uv run pytest --headed tests/sauce_ui/

# Run specific test with Xray integration
uv run pytest tests/sauce_ui/test_cart_page.py::test_cart_page_loads -v

# Run tests and update Xray results (when configured)
uv run pytest --xray-execution-id=DEV-123
```

### 📊 Test Management with Xray

The Xray MCP server enables seamless integration with Jira/Xray:

```python
# Example: Using Xray in your workflow
# 1. Create test execution
# 2. Run tests
# 3. Update test results via MCP

# Copilot can help automate this:
"""
@workspace Create a test execution for sprint 23 and run all cart page tests,
then update the test results in Xray
"""
```

---

## 🔧 Advanced Configuration

### Custom Pytest Markers

Register custom markers in `pytest.ini`:

```ini
[pytest]
markers =
    sanity: Quick smoke tests
    regression: Full regression suite
    test_case_key: Xray test case identifier
```

### Xray Integration

Tests can be linked to Xray test cases:

```python
@pytest.mark.test_case_key("DEV-51")
def test_cart_page_loads(logged_in_user):
    """Test cart page loads successfully."""
    # Test execution will be linked to DEV-51 in Xray
```

### Allure Report Customization

Customize Allure reports in tests:

```python
import allure

@allure.feature("Shopping Cart")
@allure.story("Cart Management")
@allure.severity(allure.severity_level.CRITICAL)
def test_add_to_cart(logged_in_user):
    """Test adding products to cart."""
    with allure.step("Navigate to inventory page"):
        # Test steps...
        pass
```

---

## 🤝 Contributing

### Development Workflow

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/new-test-suite
   ```

2. **Generate Tests with AI**
   ```
   @workspace Generate tests for checkout page following architecture guidelines
   ```

3. **Run Tests Locally**
   ```bash
   uv run pytest tests/sauce_ui/test_checkout_page.py -v
   ```

4. **Code Review with AI**
   ```
   Follow instructions in @code-review.prompt.md
   Review the new checkout page tests
   ```

5. **Commit with Conventional Commits**
   ```bash
   git add tests/sauce_ui/test_checkout_page.py
   git commit -m "test(checkout): add comprehensive checkout page tests

   - Add 8 new test scenarios for checkout flow
   - Cover happy path and error scenarios
   - Link to Xray test cases DEV-100 through DEV-107"
   ```

6. **Push and Create PR**
   ```bash
   git push -u origin feature/new-test-suite
   ```

---

## 📚 Documentation

- **Architecture Guidelines**: See `contexts/architecture_context_docs/`
- **Feature Specifications**: See `contexts/product_context_docs/`
- **Custom Agents**: See `.github/agents/`
- **Custom Prompts**: See `.github/prompts/`

---


## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [Playwright](https://playwright.dev/) - Reliable browser automation
- [Pytest](https://pytest.org/) - Testing framework
- [Model Context Protocol](https://modelcontextprotocol.io/) - AI context integration
- [GitHub Copilot](https://github.com/features/copilot) - AI-powered development
- [Xray for Jira](https://www.getxray.app/) - Test management
- [Allure Framework](https://allurereport.org/) - Test reporting
- [SauceDemo](https://www.saucedemo.com/) - Test application
- [Pet Store API](https://petstore.swagger.io/) - API testing endpoint
- [Chrome DevTools MCP](https://github.com/modelcontextprotocol/servers/tree/main/src/chrome-devtools) - Element selector discovery

---

## 📬 Contact

Afik Mark - [@afikmark](https://github.com/afikmark)

Project Link: [https://github.com/afikmark/AIAutomationFramework](https://github.com/afikmark/AIAutomationFramework)

---

## 🔮 Roadmap

### Current Features
- ✅ Page Object Model implementation
- ✅ Custom MCP servers (Test Context & Xray)
- ✅ GitHub Copilot agents and prompts
- ✅ Xray/Jira integration via GraphQL
- ✅ AI-powered test generation
- ✅ Comprehensive test coverage (UI & API)
- ✅ Pytest fixtures and markers
- ✅ Allure reporting with rich test documentation
- ✅ Authentication state reuse for faster execution
- ✅ Flexible base URL configuration

### Planned Features
- [ ] CI/CD pipeline templates (GitHub Actions)
- [ ] Advanced reporting dashboard
- [ ] Test data management utilities
- [ ] Visual regression testing
- [ ] Performance testing integration
- [ ] Parallel test execution (pytest-xdist)
- [ ] Docker containerization

---


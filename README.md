# AI-Driven Automation Infrastructure

> An intelligent automation testing infrastructure that leverages AI capabilities including Agentic AI workflows, RAG (Retrieval-Augmented Generation), and MCP (Model Context Protocol) servers generate automated tests

[![Python](https://img.shields.io/badge/Python-3.12%2B-blue.svg)](https://www.python.org/downloads/)
[![Playwright](https://img.shields.io/badge/Playwright-Latest-green.svg)](https://playwright.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🎯 Overview

This project represents a next-generation automation testing infrastructure that combines traditional test automation with cutting-edge AI technologies. It automatically identifies UI elements using natural language, and leverages intelligent caching strategies for optimal performance.


### Key Features

- **🔌 MCP Server Integration**: Model Context Protocol server for AI-powered test generation and management
- **🎭 Playwright Integration**: Reliable cross-browser automation
- **⚡ Smart Caching**: Multi-level caching for optimal performance
---

## 🛠️ Tech Stack

### Core Technologies

| Technology | Purpose | Version |
|------------|---------|---------|
| **Python** | Primary language | 3.12+ |
| **Playwright** | Browser automation | Latest |
| **LangChain** | AI orchestration | Latest |
| **Ollama** | Local LLM inference | Latest |
| **Chroma** | Vector database | Latest |
| **Tenacity** | Retry logic | 9.1.2 |


### AI & ML Stack

- **LLM**: Llama 3.1 (8B parameter model)
- **Embeddings**: Ollama embeddings (llama3)
- **RAG**: LangChain + Chroma for semantic search

### Testing & Development

- **Pytest**: Testing framework
- **Pydantic**: Data validation
- **Python-dotenv**: Environment management

---

## 🚀 Quick Start

### Prerequisites

- Python 3.12 or higher (managed via [uv](https://docs.astral.sh/uv/))
- [Ollama](https://ollama.ai/) installed and running
- Git

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

# Pull required Ollama models
ollama pull llama3.1:8b
ollama pull llama3
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

# Pull required Ollama models
ollama pull llama3.1:8b
ollama pull llama3
```

---

## ⚙️ Configuration

### 1. Environment Setup

Create a `.env` file in the root directory:

```bash
# Optional: API keys if using external LLMs
# OPENAI_API_KEY=your_key_here
# ANTHROPIC_API_KEY=your_key_here
# GOOGLE_API_KEY=your_key_here
```

###  MCP Server Configuration for VS Code & GitHub Copilot

The project includes a Model Context Protocol (MCP) server that enables GitHub Copilot to generate tests using project-specific guidelines and feature documentation.

#### **Step 1: Configure VS Code MCP Settings**

Create or update `.vscode/mcp.json` in your workspace:

```json
{
  "servers": {
    "automation_generator_mcp": {
      "type": "stdio",
      "command": "{WORKSPACE}/AIAutomationFramework/.venv/bin/python",
      "args": [
        "{WORKSPACE}/AIAutomationFramework/mcp_server/test_generation_server.py"
      ]
    },
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@latest"]
    }
  },
  "inputs": []
}

```

**Important**: Update the paths to match your actual workspace location:
- **Linux/macOS**: Use `.venv/bin/python`
- **Windows**: Use `.venv\Scripts\python.exe`

#### **Step 2: Start the MCP Server**

The MCP server will automatically start when GitHub Copilot initializes. You can also start it manually:

```bash
# Linux/macOS
source .venv/bin/activate
python mcp_server/test_generation_server.py

# Windows
.venv\Scripts\activate
python mcp_server\test_generation_server.py
```

#### **Step 3: Verify MCP Server is Running**

Check the Copilot MCP status in VS Code:
1. Open VS Code Command Palette (`Ctrl+Shift+P` or `Cmd+Shift+P`)
2. Search for "MCP: Show Server Status"
3. Verify that `automation_generator_mcp` is listed and running

---

## 📖 Usage

## 🤖 Test Generator Usage

This project provides AI-powered test generators via the MCP server, enabling you to generate both Playwright UI tests and API tests using project-specific guidelines and documentation directly from VS Code with GitHub Copilot.

### How to Use the Test Generator

1. **Start the MCP Server**

   ```bash
   # Linux/macOS
   uv run python mcp_server/test_generation_server.py

   # Windows
   uv run python mcp_server\test_generation_server.py
   ```

2. **Configure VS Code for MCP**
   - Ensure `.vscode/mcp.json` is set up as described in the Configuration section.

### Generating Web UI Tests

3. **Generate UI Tests with Copilot**
   - In a Copilot chat, use the predefined prompt:
   ```
   /mcp.automation_generator_mcp.GenerateWebTestRequest 
   ```
   - Give an input like:
      ```Generate tests for the Cart Page```

4. **The IDE will ask for the user query:**
![prompt_command](https://github.com/user-attachments/assets/5b6b7e77-ccad-4662-b835-dfae2f9193f9)

5. **It will then**:
    * Read relevant documentation about the product/feature
      <img width="746" height="422" alt="reading_context" src="https://github.com/user-attachments/assets/c3aee725-6a1b-486c-8697-44887909e53e" />
    * Read relevant documentation about the areas that need to be modified
      <img width="746" height="422" alt="reading_context" src="https://github.com/user-attachments/assets/9dd3eae3-0441-4f97-9c8b-51351a6aac98" />  
    * Follow custom guidelines and design patterns on how to generate tests and POM
    * Generate Page Object if missing:
      <img width="775" height="1203" alt="tests_with_page_object_creation" src="https://github.com/user-attachments/assets/f5c43d59-3c47-453c-8e38-9ae14c045647" />
    * Implement the new tests
    * Execute them until success
      <img width="752" height="543" alt="completed" src="https://github.com/user-attachments/assets/1ccb4a14-424d-4c21-92d9-2f1530c8bf8d" />

### Generating API Tests

3. **Generate API Tests with Copilot**
   - In a Copilot chat, use the predefined prompt:
   ```
   /mcp.automation_generator_mcp.GenerateApiTestRequest
   ```
   - Give an input like:
      ```Generate tests for the Pet Store user creation endpoint```

4. **The MCP server will**:
   * Retrieve API endpoint documentation (Pet Store user, pet, store endpoints)
   * Load API testing guidelines and patterns
   * Check existing controllers and schemas
   * Generate Pydantic request/response models if needed
   * Create controller methods for the endpoint
   * Generate pytest tests with proper assertions
   * Use the `pet_cleanup` fixture for test isolation
   * Run tests and fix any issues

5. **Example Generated Structure**:
   ```
   core/
     controllers/pet_store_controller.py  # API client with typed methods
     schemas/pet_store_pet.py             # Pydantic models
   tests/
     pet_store_api/
       conftest.py                        # Cleanup fixtures
       test_pet_store_pet.py              # Generated tests
   ```

7. **Review and Run Generated Tests**
   - Review the generated test code

#### Best Practices
* Always review generated code before committing
* Use specific prompts for best results (mention feature and guideline)
* Run tests after generation to ensure they pass
* For API tests, the cleanup fixture automatically removes test data


### Running Tests

```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/test_login_page.py

# Run with verbose output
uv run pytest -v -s

# Run specific test
uv run pytest tests/test_login_page.py::test_login_with_valid_credentials -v

```

### MCP Server

The project includes an MCP server for test generation:

```bash
# Start the MCP server
uv run python mcp_server/test_generation_server.py
```

### Using the MCP Server with GitHub Copilot

The MCP server exposes several tools that GitHub Copilot can use to generate tests intelligently using your project's guidelines and documentation.


#### **How to Use MCP with Copilot**

**4. Ask Copilot to generate tests:**
```
@workspace Generate a test for the login page using the page object model guidelines
```

Copilot will:
- Retrieve the login page feature description
- Retrieve the page object model guidelines
- Generate test code following the guidelines
- Optionally write the test to `tests/test_<feature>.py`


## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [Playwright](https://playwright.dev/) - Reliable browser automation
- [LangChain](https://www.langchain.com/) - AI orchestration framework
- [Ollama](https://ollama.ai/) - Local LLM inference
- [Chroma](https://www.trychroma.com/) - Vector database
- [SauceDemo](https://www.saucedemo.com/) - Test application
- [Chrome Dev Tools MCP] (https://github.com/mcp/chromedevtools/chrome-devtools-mcp) - MCP server for detecting locators

---

## 📬 Contact

Afik Mark - [@afikmark](https://github.com/afikmark)

Project Link: [https://github.com/afikmark/AIAutomationFramework](https://github.com/afikmark/AIAutomationFramework)

---

## 🔮 Future Roadmap

- [ ] Support documentation fetching via Jira MCP
- [ ] CI/CD pipeline templates
- [ ] Reporting and Logging capabilities
---

**Made with ❤️ and 🤖 AI**

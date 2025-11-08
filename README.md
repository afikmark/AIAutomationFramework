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

- Python 3.12 or higher
- [Ollama](https://ollama.ai/) installed and running
- Git

### Installation

#### **Linux / macOS**

```bash
# Clone the repository
git clone https://github.com/afikmark/AIAutomationFramework.git
cd AIAutomationFramework

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install

# Pull required Ollama models
ollama pull llama3.1:8b
ollama pull llama3
```

#### **Windows**

```powershell
# Clone the repository
git clone https://github.com/afikmark/AIAutomationFramework.git
cd AIAutomationFramework

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install

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

This project provides an AI-powered test generator via the MCP server, enabling you to generate Playwright tests using project-specific guidelines and feature documentation directly from VS Code with GitHub Copilot.

### How to Use the Test Generator

1. **Start the MCP Server**

   ```bash
   # Linux/macOS
   source .venv/bin/activate
   python mcp_server/test_generation_server.py

   # Windows
   .venv\Scripts\activate
   python mcp_server\test_generation_server.py
   ```

2. **Configure VS Code for MCP**
   - Ensure `.vscode/mcp.json` is set up as described in the Configuration section.

3. **Generate Tests with Copilot**
   - In a Copilot chat, use predefined prompt:
   ```
   /mcp.automation_generator_mcp.GenerateTestRequest 
   ```
   vscode will ask your for the user query, input something like:
   `generate test for the cart page`

4. **Review and Run Generated Tests**
   - Review the generated test code
   - Run with `pytest` to verify correctness

#### Best Practices
* Always review generated code before committing
* Use specific prompts for best results (mention feature and guideline)
* Run tests after generation to ensure they pass


### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_login_page.py

# Run with verbose output
pytest -v -s

# Run specific test
pytest tests/test_login_page.py::test_login_with_valid_credentials -v

```

### MCP Server

The project includes an MCP server for test generation:

```bash
# Start the MCP server
python mcp_server/test_generation_server.py
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

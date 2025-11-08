"""
Global variables and constants for the PlaywrightSelfHealing project.

This module provides centralized access to project paths and configuration.
"""

from pathlib import Path
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Project root directory - the base directory of the entire project
PROJECT_ROOT = Path(__file__).resolve().parent

# Common directories
CONTEXTS_DIR = PROJECT_ROOT / "contexts"
PRODUCT_CONTEXTS_DIR = CONTEXTS_DIR / "product_context_docs"
ARCHITECTURE_CONTEXTS_DIR = CONTEXTS_DIR / "architecture_context_docs"
TESTS_DIR = PROJECT_ROOT / "tests"
PAGES_DIR = PROJECT_ROOT / "core" / "web" / "pages"

IS_MODEL_LOCAL: bool = os.getenv("IS_MODEL_LOCAL") == "true"

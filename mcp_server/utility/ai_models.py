from langchain_google_genai import ChatGoogleGenerativeAI
from google.genai.types import GenerateContentConfig
from langchain_core.language_models import BaseChatModel
from langchain_ollama import ChatOllama
from pydantic import BaseModel


class GeminiModels:
    """Class for Gemini model constants."""

    GEMINI_2_0_FLASH: str = "gemini-2.0-flash-exp"
    GEMINI_2_5_PRO: str = "gemini-2.5-pro"


class OllamaModels:
    """Class for Ollama model constants."""

    GPT_OSS_20B: str = "gpt-oss:20b"


class OllamaConfig(BaseModel):
    """Config for Ollama model parameters."""

    temperature: float = 0.1
    num_predict: int = 1024
    top_p: float = 0.5
    top_k: int = 40
    stop: list[str] | None = None


class GeminiConfig(BaseModel):
    """Config for Gemini model parameters."""

    temperature: float = 0.1
    num_predict: int = 4000
    top_p: float = 0.5
    top_k: int = 40
    stop: list[str] | None = None

    def to_generate_content_config(self) -> GenerateContentConfig:
        """Convert to GenerateContentConfig for Gemini API."""
        return GenerateContentConfig(
            temperature=self.temperature,
            max_output_tokens=self.num_predict,
            top_p=self.top_p,
            top_k=self.top_k,
            stop_sequences=self.stop,
        )


class OllamaChatModel:
    def __init__(self, model: str, config: OllamaConfig | None = None):
        self.model = model
        self.config = config or OllamaConfig()
        self._client = ChatOllama(model="gpt-oss:20b", temperature=0)

    @property
    def client(self) -> ChatOllama:
        return self._client


class GeminiChatModel:
    def __init__(self, model: str, config: dict | None = None):
        from dotenv import load_dotenv
        import os
        import getpass

        load_dotenv()

        if "GOOGLE_API_KEY" not in os.environ:
            os.environ["GOOGLE_API_KEY"] = getpass.getpass(
                "Enter your Google AI API key: "
            )
        llm = ChatGoogleGenerativeAI(
            model=model,
            temperature=0.1,
            max_tokens=1024,
            timeout=None,
            max_retries=2,
            # other params...
        )
        config = config or GeminiConfig().model_dump()
        # self._client = ChatGoogleGenerativeAI(**config, model=model)
        self._client = llm

    @property
    def client(self) -> ChatGoogleGenerativeAI:
        return self._client


class AIModel:
    """AI Model wrapper to select between local and remote models."""

    @classmethod
    def get_model(
        cls, is_local: bool, local_model: str = "", remote_model: str = ""
    ) -> BaseChatModel:
        if is_local:
            return OllamaChatModel(model=local_model or OllamaModels.GPT_OSS_20B).client
        else:
            return GeminiChatModel(
                model=remote_model or GeminiModels.GEMINI_2_5_PRO
            ).client

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    # Database
    DB_USER: str | None = None
    DB_PASSWORD: str | None = None
    DB_HOST: str | None = None
    DB_NAME: str | None = None
    DB_PORT: int | None = None

    # General
    APP_NAME: str | None = None
    FRONTEND_BASE_URL: str | None = None

    # Security
    BACKEND_CORS_ORIGIN: str | None = None

    # OpenAI
    OPENAI_API_KEY: str | None = None
    OPENAI_MODEL: str | None = None
    OPENAI_EMBEDDING_MODEL: str | None = None
    PROMPT_TEMPLATE: str = (
        "Eres un asistente experto en materia tributaria y legal. Con base únicamente en la información proporcionada a continuación, responde de forma clara, precisa y profesional. Si no cuentas con suficiente información para responder, indícalo con transparencia. {context}\n\n---\n\nPregunta:\n{question}\n\n---\n\nRespuesta:"
    )

settings = Settings()

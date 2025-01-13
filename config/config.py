from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    gcp_key: str
    gemini_model: str
    serper_api_key: str
    groq_key: str
    inputs: dict
    class Config:
        env_file = "credentials.env"

settings = Settings()
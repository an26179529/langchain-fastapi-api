from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    OPENAI_API_KEY: str

    LangSmith_API_KEY: str
    LANGCHAIN_TRACING_V2: bool = True
    LANGCHAIN_ENDPOINT: str

    TAVILY_API_KEY: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str 
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"
        
@lru_cache
def get_settings():
    return Settings()

settings = get_settings()

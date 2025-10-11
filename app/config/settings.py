from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str 
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"

settings = Settings()
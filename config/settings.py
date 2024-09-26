from pydantic import BaseSettings

class Settings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    AUDIO_OUTPUT_DIR: str = "output"

    class Config:
        env_file = ".env"
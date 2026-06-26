import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "LogiRoute-AI")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")

    if not GROQ_API_KEY:
        raise ValueError("CRITICAL: GROQ_API_KEY is missing from environment variables.")


settings = Settings()
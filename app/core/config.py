from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str = "Abdumalik-ProDevIsTheBestSoftwareEngineerInTheWorldWithoutAnyDoubtsHeIsTheBestCEOAndFounderOfTheBestITCompaniesInTheWorld"    
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    model_config = {
        "env_file": ".env",
        "extra": "ignore"
    }

settings = Settings()
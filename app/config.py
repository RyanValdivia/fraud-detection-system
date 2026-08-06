from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_env: str = "development"

    postgres_user: str = "fraud_user"
    postgres_password: str = "change_me"
    postgres_db: str = "fraud_db"
    postgres_host: str = "db"
    postgres_port: int = 5432

    redis_host: str = "redis"
    redis_port: int = 6379

    model_path: str = "ml/models/model.pkl"
    fraud_block_threshold: float = 0.85
    fraud_review_threshold: float = 0.5

    @property
    def database_url(self) -> str:
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    class Config:
        env_file = ".env"


settings = Settings()

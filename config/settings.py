from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    app_name: str = "MiMo HR Operations Engine"
    app_version: str = "1.0.0"
    debug: bool = Field(default=False, description="Enable debug mode")
    host: str = "0.0.0.0"
    port: int = 8000
    mimo_api_url: str = Field(
        default="https://api.nousresearch.com/v1",
        description="MiMo LLM API base URL",
    )
    mimo_api_key: str = Field(
        default="",
        description="MiMo LLM API key",
    )
    mimo_model: str = Field(
        default="mimo-v2.5-pro",
        description="MiMo model identifier",
    )
    cors_origins: list[str] = ["*"]
    log_level: str = "INFO"

    model_config = {"env_prefix": "MIMO_HR_", "env_file": ".env"}


settings = Settings()

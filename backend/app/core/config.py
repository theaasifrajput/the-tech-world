from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "The Tech World API"
    environment: str = "local"
    api_v1_prefix: str = "/v1"
    database_url: str = "postgresql+psycopg://ttw:ttw_local_password@localhost:5432/the_tech_world"
    firebase_project_id: str | None = None
    cors_origins: str = "http://localhost:3000"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def cors_origin_list(self) -> list[str]:
        return [item.strip() for item in self.cors_origins.split(",") if item.strip()]


settings = Settings()

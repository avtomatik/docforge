from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    model_config = SettingsConfigDict(env_file=".env")

    # ========================================================================
    # Business Specific
    # ========================================================================
    ACCOUNT_NAME: str
    PARTNER_NAME: str
    PREFIX: str
    REF_PLACEHOLDER: str
    REF_RESERVED: str

    # ========================================================================
    # Templates Archive
    # ========================================================================
    ARCHIVE_NAME: str

    # ========================================================================
    # Specific Excel File Names
    # ========================================================================
    FILE_NAME_PANELS: str

    # ========================================================================
    # Anchor for Multiline `docx-mailmerge` Field
    # ========================================================================
    MERGE_ANCHOR: str

    # ========================================================================
    # Database
    # ========================================================================
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_NAME: str
    DB_PORT: int = 5432

    @property
    def db_url(self) -> str:
        return (
            f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


settings = Settings()

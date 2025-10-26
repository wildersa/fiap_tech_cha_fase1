from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "fiap_tech_cha_fase1"
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    RELOAD: bool = False
    LOG_LEVEL: str = "info"
    # permite apontar para outro módulo/variável app, se quiser:
    APP_IMPORT_PATH: str = "fiap_tech_cha_fase1.app.main:app"

    class Config:
        # procura arquivo .env no diretório atual (onde você rodar o módulo)
        env_file = ".env"
        env_file_encoding = "utf-8"
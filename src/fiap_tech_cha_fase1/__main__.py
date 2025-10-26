from importlib import import_module
from .settings import Settings
import uvicorn

def _get_app(import_path: str):
    module_name, attr = import_path.split(":", 1) if ":" in import_path else (import_path, "app")
    mod = import_module(module_name)
    return getattr(mod, attr)

def main():
    settings = Settings()  # pydantic carrega .env conforme seu settings.py
    app = _get_app(settings.APP_IMPORT_PATH)
    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        log_level=settings.LOG_LEVEL,
    )

if __name__ == "__main__":
    main()
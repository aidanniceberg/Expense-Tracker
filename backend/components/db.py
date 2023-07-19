from sqlalchemy import create_engine

from components.settings import get_settings

SETTINGS = get_settings()

def generate_connection_string() -> str:
    return f"{SETTINGS.db_config.dialect}+{SETTINGS.db_config.driver}://{SETTINGS.db_config.username}:{SETTINGS.db_config.password}@{SETTINGS.db_config.host}:{SETTINGS.db_config.port}/{SETTINGS.db_config.database}"


def get_engine():
    return create_engine(generate_connection_string())

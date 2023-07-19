from pydantic import BaseModel


class DBConfig(BaseModel):
    dialect: str = ""
    driver: str = ""
    username: str = ""
    password: str = ""
    host: str = ""
    port: str = ""
    database: str = ""


class Settings(BaseModel):
    db_config: DBConfig


def get_settings():
    return Settings(
        db_config=DBConfig(
            dialect="mysql",
            driver="mysqlconnector",
            username="root",
            password="root",
            host="db",
            port="3306",
            database="expense_tracker",
        )
    )

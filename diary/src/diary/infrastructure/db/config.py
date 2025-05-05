from pydantic import BaseModel, Field


class PGConfig(BaseModel):
    host: str = Field(alias="PG_HOST")
    port: int = Field(alias="PG_PORT")
    login: str = Field(alias="PG_LOGIN")
    password: str = Field(alias="PG_PASSWORD")
    database: str = Field(alias="PG_DATABASE")
    echo: bool = Field(alias="PG_ECHO", default=False)

    @property
    def uri(self) -> str:
        return f"postgresql+asyncpg://{self.login}:{self.password}@{self.host}:{self.port}/{self.database}"

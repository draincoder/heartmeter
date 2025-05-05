from pydantic import BaseModel, Field


class LogConfig(BaseModel):
    level: str = Field(alias="LOG_LEVEL", default="INFO")
    filepath: str = Field(alias="LOG_FILEPATH", default="app.log")

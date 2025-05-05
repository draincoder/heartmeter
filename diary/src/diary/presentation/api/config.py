from pydantic import BaseModel, Field


class APIConfig(BaseModel):
    host: str = Field(alias="API_HOST", default="127.0.0.1")
    port: int = Field(alias="API_PORT", default=8080)

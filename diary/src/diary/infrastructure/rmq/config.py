from pydantic import BaseModel, Field


class RMQConfig(BaseModel):
    host: str = Field(alias="RMQ_HOST")
    port: int = Field(alias="RMQ_PORT")
    user: str = Field(alias="RMQ_USER")
    password: str = Field(alias="RMQ_PASSWORD")

    @property
    def url(self) -> str:
        return f"amqp://{self.user}:{self.password}@{self.host}:{self.port}/"

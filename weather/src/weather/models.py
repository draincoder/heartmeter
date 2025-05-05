from pydantic import BaseModel


class Weather(BaseModel):
    temperature: int
    condition: str
    pressure: int

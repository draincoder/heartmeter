from fastapi import FastAPI, Query, HTTPException
import datetime

from starlette import status

from .models import Weather
from .generator import generate_weather_by_date

app = FastAPI()


@app.get("/weather", tags=["Weather"])
def get_weather(date: str = Query(description="Date in format YYYY-MM-DD")) -> Weather:
    try:
        datetime.date.fromisoformat(date)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Use format YYYY-MM-DD for date",
        )

    return generate_weather_by_date(date)

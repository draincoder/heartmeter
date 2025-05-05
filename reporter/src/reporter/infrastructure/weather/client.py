import datetime

import aiohttp

from reporter.application.dto import Weather
from reporter.application.interfaces import WeatherReader

BAD_STATUS_CODE = 400
OK_STATUS_CODE = 200


class WeatherError(Exception): ...


class AiohttpWeatherClient(WeatherReader):
    def __init__(self, base_url: str) -> None:
        self._url = f"{base_url}/weather"

    async def get(self, date: datetime.date) -> Weather:
        params = {"date": date.isoformat()}
        async with aiohttp.ClientSession() as session, session.get(self._url, params=params) as resp:
            if resp.status == BAD_STATUS_CODE:
                detail = await resp.json()
                raise WeatherError(f"Invalid request: {detail.get('detail')}")

            if resp.status != OK_STATUS_CODE:
                raise WeatherError(f"Failed to fetch weather: HTTP {resp.status}")

            data = await resp.json()
            return Weather(temperature=data["temperature"], pressure=data["pressure"])

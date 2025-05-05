import hashlib
import random

from .models import Weather

WEATHER_CONDITIONS = ["Sunny", "Cloudy", "Rainy", "Snowy", "Windy", "Stormy"]


def generate_weather_by_date(date_str: str) -> Weather:
    hash_seed = int(hashlib.sha256(date_str.encode()).hexdigest(), 16)
    random.seed(hash_seed)

    temperature = random.randint(-10, 35)
    pressure = random.randint(650, 780)
    condition = random.choice(WEATHER_CONDITIONS)

    return Weather(temperature=temperature, pressure=pressure, condition=condition)

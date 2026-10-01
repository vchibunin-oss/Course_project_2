from abc import ABC, abstractmethod

import requests


class BaseAPI(ABC):
    """Абстрактный класс для работы с внешними API."""

    @abstractmethod
    def get_country_coordinates(self, country: str):
        """Получает координаты страны."""
        pass

    @abstractmethod
    def get_aeroplanes(self, country: str):
        """Получает информацию о самолетах."""
        pass


class AeroplanesAPI(BaseAPI):
    """Класс для работы с Nominatim и OpenSky API."""

    NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
    OPENSKY_URL = "https://opensky-network.org/api/states/all"

    def __init__(self):
        self.aeroplanes = []

    def get_country_coordinates(self, country: str):
        """Получает bounding box страны через Nominatim."""

        params = {
            "q": country,
            "format": "jsonv2",
            "limit": 1,
            "featureType": "country",
        }

        headers = {
            "User-Agent": "CourseProject2/1.0",
        }

        response = requests.get(
            self.NOMINATIM_URL,
            params=params,
            headers=headers,
            timeout=10,
        )
        response.raise_for_status()

        data = response.json()

        if not data:
            raise ValueError(f"Страна не найдена: {country}")

        return data[0]["boundingbox"]

    def get_aeroplanes(self, country: str):
        """Получает самолеты в воздушном пространстве страны."""

        bounding_box = self.get_country_coordinates(country)

        lamin = float(bounding_box[0])
        lamax = float(bounding_box[1])
        lomin = float(bounding_box[2])
        lomax = float(bounding_box[3])

        params = {
            "lamin": lamin,
            "lomin": lomin,
            "lamax": lamax,
            "lomax": lomax,
        }

        response = requests.get(
            self.OPENSKY_URL,
            params=params,
            timeout=10,
        )
        response.raise_for_status()

        data = response.json()

        self.aeroplanes = data.get("states") or []

        return self.aeroplanes

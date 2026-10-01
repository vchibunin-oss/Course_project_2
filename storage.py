import json
from abc import ABC, abstractmethod

from models import Aeroplane


class BaseStorage(ABC):
    """Абстрактный класс для работы с хранилищем самолетов."""

    @abstractmethod
    def add_aeroplane(self, aeroplane: Aeroplane):
        """Добавляет самолет в хранилище."""
        pass

    @abstractmethod
    def get_aeroplanes(self, **criteria):
        """Получает самолеты по заданным критериям."""
        pass

    @abstractmethod
    def delete_aeroplane(self, aeroplane: Aeroplane):
        """Удаляет самолет из хранилища."""
        pass


class JSONSaver(BaseStorage):
    """Хранилище самолетов в JSON-файле."""

    def __init__(self, file_path: str):
        self.file_path = file_path

    def _load_data(self):
        """Загружает данные из JSON-файла."""

        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def _save_data(self, data):
        """Сохраняет данные в JSON-файл."""

        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=4,
            )

    def add_aeroplane(self, aeroplane: Aeroplane):
        """Добавляет самолет в JSON-файл."""

        data = self._load_data()

        data.append(
            {
                "icao24": aeroplane.icao24,
                "callsign": aeroplane.callsign,
                "origin_country": aeroplane.origin_country,
                "longitude": aeroplane.longitude,
                "latitude": aeroplane.latitude,
                "altitude": aeroplane.altitude,
                "velocity": aeroplane.velocity,
            }
        )

        self._save_data(data)

    def get_aeroplanes(self, **criteria):
        """Возвращает самолеты, соответствующие критериям."""

        data = self._load_data()

        result = []

        for item in data:
            if all(item.get(key) == value for key, value in criteria.items()):
                result.append(Aeroplane(**item))

        return result

    def delete_aeroplane(self, aeroplane: Aeroplane):
        """Удаляет самолет из JSON-файла."""

        data = self._load_data()

        data = [item for item in data if item.get("icao24")
                != aeroplane.icao24]

        self._save_data(data)

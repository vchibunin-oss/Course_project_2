from dataclasses import dataclass


@dataclass
class Aeroplane:
    """Модель самолета."""

    icao24: str
    callsign: str
    origin_country: str
    longitude: float
    latitude: float
    altitude: float
    velocity: float

    def __post_init__(self):
        """Проверяет корректность данных самолета."""

        if not self.icao24:
            raise ValueError("ICAO24 не может быть пустым")

        if not self.callsign:
            raise ValueError("Позывной не может быть пустым")

        if not self.origin_country:
            raise ValueError("Страна регистрации не может быть пустой")

        if self.altitude < 0:
            raise ValueError("Высота не может быть отрицательной")

        if self.velocity < 0:
            raise ValueError("Скорость не может быть отрицательной")

    def __lt__(self, other):
        """Сравнивает самолеты по скорости."""

        if not isinstance(other, Aeroplane):
            return NotImplemented

        return self.velocity < other.velocity

    def compare_altitude(self, other):
        """Сравнивает самолеты по высоте."""

        if not isinstance(other, Aeroplane):
            raise TypeError("Сравнивать можно только самолеты")

        return self.altitude < other.altitude

    @classmethod
    def from_opensky(cls, data):
        """Создает объект Aeroplane из ответа OpenSky."""

        return cls(
            icao24=data[0],
            callsign=data[1].strip(),
            origin_country=data[2],
            longitude=float(data[5]),
            latitude=float(data[6]),
            altitude=float(data[7]),
            velocity=float(data[9]),
        )

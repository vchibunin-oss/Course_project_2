from models import Aeroplane


def filter_aeroplanes(
    aeroplanes: list[Aeroplane],
    countries: list[str],
) -> list[Aeroplane]:
    """Фильтрует самолеты по стране регистрации."""

    countries = {country.lower() for country in countries}

    return [
        aeroplane
        for aeroplane in aeroplanes
        if aeroplane.origin_country.lower() in countries
    ]


def sort_aeroplanes(
    aeroplanes: list[Aeroplane],
) -> list[Aeroplane]:
    """Сортирует самолеты по высоте от большей к меньшей."""

    return sorted(
        aeroplanes,
        key=lambda aeroplane: aeroplane.altitude,
        reverse=True,
    )


def get_top_aeroplanes(
    aeroplanes: list[Aeroplane],
    top_n: int,
) -> list[Aeroplane]:
    """Возвращает TOP N самолетов по высоте."""

    if top_n <= 0:
        raise ValueError("Количество самолетов должно быть больше нуля")

    return sort_aeroplanes(aeroplanes)[:top_n]


def get_aeroplanes_by_altitude(
    aeroplanes: list[Aeroplane],
    altitude_range: str,
) -> list[Aeroplane]:
    """Возвращает самолеты, находящиеся в указанном диапазоне высот."""

    try:
        minimum, maximum = map(
            float,
            altitude_range.split("-"),
        )
    except ValueError as error:
        raise ValueError(
            "Диапазон высот должен быть указан в формате: 1000 - 5000"
        ) from error

    if minimum > maximum:
        raise ValueError(
            "Минимальная высота не может быть больше максимальной")

    return [
        aeroplane
        for aeroplane in aeroplanes
        if minimum <= aeroplane.altitude <= maximum
    ]

from api import AeroplanesAPI
from models import Aeroplane
from storage import JSONSaver
from utils import (filter_aeroplanes, get_aeroplanes_by_altitude,
                   get_top_aeroplanes)


def print_aeroplane(aeroplane: Aeroplane) -> None:
    """Выводит информацию о самолете."""

    print(
        f"ICAO24: {aeroplane.icao24}\n"
        f"Позывной: {aeroplane.callsign or 'Нет данных'}\n"
        f"Страна регистрации: {aeroplane.origin_country}\n"
        f"Координаты: {aeroplane.latitude}, {aeroplane.longitude}\n"
        f"Высота: {aeroplane.altitude:.0f} м\n"
        f"Скорость: {aeroplane.velocity:.2f} м/с"
    )


def load_aeroplanes(api: AeroplanesAPI, country: str) -> list[Aeroplane]:
    """Получает самолеты из API и преобразует их в объекты Aeroplane."""

    raw_aeroplanes = api.get_aeroplanes(country)

    aeroplanes = []

    for data in raw_aeroplanes:
        try:
            aeroplane = Aeroplane.from_opensky(data)
            aeroplanes.append(aeroplane)
        except (TypeError, ValueError, IndexError):
            continue

    return aeroplanes


def save_aeroplanes(
    storage: JSONSaver,
    aeroplanes: list[Aeroplane],
) -> None:
    """Сохраняет самолеты в JSON."""

    for aeroplane in aeroplanes:
        storage.add_aeroplane(aeroplane)


def show_top_aeroplanes(aeroplanes: list[Aeroplane]) -> None:
    """Выводит TOP N самолетов по высоте."""

    while True:
        try:
            top_n = int(input("Сколько самолетов показать? "))

            top_aeroplanes = get_top_aeroplanes(
                aeroplanes,
                top_n,
            )
            break

        except ValueError as error:
            print(f"Ошибка: {error}")

    print("\nTOP самолетов по высоте:\n")

    for number, aeroplane in enumerate(
        top_aeroplanes,
        start=1,
    ):
        print(f"--- Самолет №{number} ---")
        print_aeroplane(aeroplane)
        print()


def show_by_country(aeroplanes: list[Aeroplane]) -> None:
    """Выводит самолеты по стране регистрации."""

    country = input("Введите страну регистрации самолета: ").strip()

    result = filter_aeroplanes(
        aeroplanes,
        [country],
    )

    if not result:
        print("\nСамолеты этой страны не найдены.")
        return

    print(f"\nСамолеты страны {country}:\n")

    for aeroplane in result:
        print_aeroplane(aeroplane)
        print()


def show_by_altitude(aeroplanes: list[Aeroplane]) -> None:
    """Выводит самолеты в диапазоне высот."""

    altitude_range = input(
        "Введите диапазон высот, например 1000 - 5000: ").strip()

    try:
        result = get_aeroplanes_by_altitude(
            aeroplanes,
            altitude_range,
        )
    except ValueError as error:
        print(f"Ошибка: {error}")
        return

    if not result:
        print("\nСамолеты в этом диапазоне не найдены.")
        return

    print("\nСамолеты в указанном диапазоне:\n")

    for aeroplane in result:
        print_aeroplane(aeroplane)
        print()


def main() -> None:
    """Запускает консольное приложение."""

    api = AeroplanesAPI()
    storage = JSONSaver("data/aeroplanes.json")

    print("=== ТРЕКЕР САМОЛЕТОВ ===")

    country = input("Введите страну для поиска самолетов: ").strip()

    if not country:
        print("Страна не может быть пустой.")
        return

    try:
        print("\nПолучаем данные из OpenSky...")

        aeroplanes = load_aeroplanes(
            api,
            country,
        )

        if not aeroplanes:
            print("Самолеты не найдены.")
            return

        print(f"\nНайдено самолетов: {len(aeroplanes)}")

        save_aeroplanes(
            storage,
            aeroplanes,
        )

        while True:
            print(
                "\n=== МЕНЮ ===\n"
                "1. Показать TOP самолетов по высоте\n"
                "2. Найти самолеты по стране регистрации\n"
                "3. Найти самолеты по диапазону высот\n"
                "4. Выход"
            )

            choice = input("Выберите действие: ").strip()

            if choice == "1":
                show_top_aeroplanes(aeroplanes)

            elif choice == "2":
                show_by_country(aeroplanes)

            elif choice == "3":
                show_by_altitude(aeroplanes)

            elif choice == "4":
                print("Программа завершена.")
                break

            else:
                print("Неверный выбор. Введите число от 1 до 4.")

    except (ValueError, KeyError, IndexError) as error:
        print(f"Ошибка обработки данных: {error}")

    except Exception as error:
        print(f"Произошла ошибка: {error}")


if __name__ == "__main__":
    main()

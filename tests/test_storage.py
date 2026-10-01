from models import Aeroplane
from storage import JSONSaver


def create_aeroplane():
    return Aeroplane(
        icao24="abc123",
        callsign="TEST123",
        origin_country="Spain",
        longitude=-3.7,
        latitude=40.4,
        altitude=10000.0,
        velocity=250.0,
    )


def test_add_and_get_aeroplane(tmp_path):
    file_path = tmp_path / "aeroplanes.json"
    storage = JSONSaver(str(file_path))

    aeroplane = create_aeroplane()

    storage.add_aeroplane(aeroplane)

    result = storage.get_aeroplanes(
        icao24="abc123",
    )

    assert len(result) == 1
    assert result[0].icao24 == "abc123"
    assert result[0].callsign == "TEST123"


def test_delete_aeroplane(tmp_path):
    file_path = tmp_path / "aeroplanes.json"
    storage = JSONSaver(str(file_path))

    aeroplane = create_aeroplane()

    storage.add_aeroplane(aeroplane)
    storage.delete_aeroplane(aeroplane)

    result = storage.get_aeroplanes()

    assert result == []


def test_get_aeroplanes_by_criteria(tmp_path):
    file_path = tmp_path / "aeroplanes.json"
    storage = JSONSaver(str(file_path))

    first = create_aeroplane()

    second = Aeroplane(
        icao24="def456",
        callsign="TEST456",
        origin_country="Canada",
        longitude=-5.0,
        latitude=45.0,
        altitude=12000.0,
        velocity=300.0,
    )

    storage.add_aeroplane(first)
    storage.add_aeroplane(second)

    result = storage.get_aeroplanes(
        origin_country="Canada",
    )

    assert len(result) == 1
    assert result[0].icao24 == "def456"


def test_empty_storage(tmp_path):
    file_path = tmp_path / "aeroplanes.json"
    storage = JSONSaver(str(file_path))

    result = storage.get_aeroplanes()

    assert result == []

import pytest

from models import Aeroplane


def test_aeroplane_creation():
    aeroplane = Aeroplane(
        icao24="abc123",
        callsign="TEST123",
        origin_country="Spain",
        longitude=-3.7,
        latitude=40.4,
        altitude=10000.0,
        velocity=250.0,
    )

    assert aeroplane.icao24 == "abc123"
    assert aeroplane.callsign == "TEST123"
    assert aeroplane.origin_country == "Spain"
    assert aeroplane.altitude == 10000.0
    assert aeroplane.velocity == 250.0


def test_aeroplane_validation():
    with pytest.raises(ValueError):
        Aeroplane(
            icao24="",
            callsign="TEST123",
            origin_country="Spain",
            longitude=0,
            latitude=0,
            altitude=10000,
            velocity=250,
        )

    with pytest.raises(ValueError):
        Aeroplane(
            icao24="abc123",
            callsign="TEST123",
            origin_country="Spain",
            longitude=0,
            latitude=0,
            altitude=-100,
            velocity=250,
        )


def test_compare_by_speed():
    first = Aeroplane(
        "abc123",
        "TEST1",
        "Spain",
        0,
        0,
        10000,
        200,
    )

    second = Aeroplane(
        "abc456",
        "TEST2",
        "Spain",
        0,
        0,
        10000,
        300,
    )

    assert first < second


def test_compare_by_altitude():
    first = Aeroplane(
        "abc123",
        "TEST1",
        "Spain",
        0,
        0,
        10000,
        200,
    )

    second = Aeroplane(
        "abc456",
        "TEST2",
        "Spain",
        0,
        0,
        12000,
        200,
    )

    assert first.compare_altitude(second)


def test_from_opensky():
    data = [
        "abc123",
        "TEST123  ",
        "Spain",
        1234567890,
        1234567890,
        -3.7,
        40.4,
        10000,
        False,
        250,
        180,
        90,
        None,
        10000,
        None,
        False,
        0,
    ]

    aeroplane = Aeroplane.from_opensky(data)

    assert aeroplane.icao24 == "abc123"
    assert aeroplane.callsign == "TEST123"
    assert aeroplane.origin_country == "Spain"
    assert aeroplane.longitude == -3.7
    assert aeroplane.latitude == 40.4
    assert aeroplane.altitude == 10000
    assert aeroplane.velocity == 250

from unittest.mock import Mock

import pytest

from main import (load_aeroplanes, print_aeroplane, save_aeroplanes,
                  show_by_altitude, show_by_country, show_top_aeroplanes)
from models import Aeroplane


@pytest.fixture
def aeroplane():
    return Aeroplane(
        icao24="abc123",
        callsign="TEST123",
        origin_country="Spain",
        longitude=-3.7,
        latitude=40.4,
        altitude=10000.0,
        velocity=250.0,
    )


@pytest.fixture
def aeroplanes():
    return [
        Aeroplane(
            "abc123",
            "TEST1",
            "Spain",
            0,
            0,
            10000,
            200,
        ),
        Aeroplane(
            "abc456",
            "TEST2",
            "Canada",
            0,
            0,
            12000,
            300,
        ),
    ]


def test_print_aeroplane(aeroplane, capsys):
    print_aeroplane(aeroplane)

    output = capsys.readouterr().out

    assert "abc123" in output
    assert "TEST123" in output
    assert "Spain" in output
    assert "10000" in output
    assert "250.00" in output


def test_load_aeroplanes():
    api = Mock()

    api.get_aeroplanes.return_value = [
        [
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
    ]

    result = load_aeroplanes(api, "Spain")

    assert len(result) == 1
    assert result[0].icao24 == "abc123"
    assert result[0].callsign == "TEST123"


def test_load_aeroplanes_skips_invalid_data():
    api = Mock()

    api.get_aeroplanes.return_value = [
        ["invalid"],
    ]

    result = load_aeroplanes(api, "Spain")

    assert result == []


def test_save_aeroplanes(aeroplane):
    storage = Mock()

    save_aeroplanes(
        storage,
        [aeroplane],
    )

    storage.add_aeroplane.assert_called_once_with(aeroplane)


def test_show_top_aeroplanes(aeroplanes, monkeypatch, capsys):
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "1",
    )

    show_top_aeroplanes(aeroplanes)

    output = capsys.readouterr().out

    assert "TOP самолетов по высоте" in output
    assert "TEST2" in output


def test_show_top_aeroplanes_invalid_input(
    aeroplanes,
    monkeypatch,
    capsys,
):
    answers = iter(["wrong", "1"])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(answers),
    )

    show_top_aeroplanes(aeroplanes)

    output = capsys.readouterr().out

    assert "Ошибка" in output


def test_show_by_country(aeroplanes, monkeypatch, capsys):
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "Canada",
    )

    show_by_country(aeroplanes)

    output = capsys.readouterr().out

    assert "TEST2" in output
    assert "Canada" in output


def test_show_by_country_not_found(
    aeroplanes,
    monkeypatch,
    capsys,
):
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "Germany",
    )

    show_by_country(aeroplanes)

    output = capsys.readouterr().out

    assert "не найдены" in output


def test_show_by_altitude(aeroplanes, monkeypatch, capsys):
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "9000 - 11000",
    )

    show_by_altitude(aeroplanes)

    output = capsys.readouterr().out

    assert "TEST1" in output
    assert "TEST2" not in output


def test_show_by_altitude_invalid_input(
    aeroplanes,
    monkeypatch,
    capsys,
):
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "wrong",
    )

    show_by_altitude(aeroplanes)

    output = capsys.readouterr().out

    assert "Ошибка" in output

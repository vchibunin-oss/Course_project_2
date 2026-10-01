from unittest.mock import Mock, patch

import pytest

from api import AeroplanesAPI


def test_get_country_coordinates():
    api = AeroplanesAPI()

    response = Mock()
    response.json.return_value = [
        {
            "boundingbox": [
                "40.0",
                "45.0",
                "-5.0",
                "0.0",
            ]
        }
    ]

    with patch("api.requests.get", return_value=response):
        result = api.get_country_coordinates("Spain")

    assert result == [
        "40.0",
        "45.0",
        "-5.0",
        "0.0",
    ]


def test_get_country_coordinates_country_not_found():
    api = AeroplanesAPI()

    response = Mock()
    response.json.return_value = []

    with patch("api.requests.get", return_value=response):
        with pytest.raises(ValueError):
            api.get_country_coordinates("UnknownCountry")


def test_get_aeroplanes():
    api = AeroplanesAPI()

    bounding_box_response = Mock()
    bounding_box_response.json.return_value = [
        {
            "boundingbox": [
                "40.0",
                "45.0",
                "-5.0",
                "0.0",
            ]
        }
    ]

    opensky_response = Mock()
    opensky_response.json.return_value = {
        "states": [
            [
                "abc123",
                "TEST123",
                "Spain",
                1234567890,
                1234567890,
                -3.0,
                42.0,
                10000.0,
                False,
                250.0,
                180.0,
                90.0,
                None,
                10000.0,
                None,
                False,
                0,
            ]
        ]
    }

    with patch(
        "api.requests.get",
        side_effect=[
            bounding_box_response,
            opensky_response,
        ],
    ):
        result = api.get_aeroplanes("Spain")

    assert len(result) == 1
    assert result[0][0] == "abc123"
    assert result[0][1] == "TEST123"
    assert result[0][2] == "Spain"


def test_get_aeroplanes_empty_states():
    api = AeroplanesAPI()

    bounding_box_response = Mock()
    bounding_box_response.json.return_value = [
        {
            "boundingbox": [
                "40.0",
                "45.0",
                "-5.0",
                "0.0",
            ]
        }
    ]

    opensky_response = Mock()
    opensky_response.json.return_value = {"states": None}

    with patch(
        "api.requests.get",
        side_effect=[
            bounding_box_response,
            opensky_response,
        ],
    ):
        result = api.get_aeroplanes("Spain")

    assert result == []

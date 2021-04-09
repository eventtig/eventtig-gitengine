import pytest

from eventtig.event import Event
from eventtig.exceptions import EndIsBeforeStartException


def test_start_1():
    event = Event()
    event.load_from_yaml_data(
        "id",
        {"start": "2021-01-03 07:08", "end": "2021-01-03 08:08"},
        "events/id/event.yaml",
    )
    assert event.start_year == 2021
    assert event.start_month == 1
    assert event.start_day == 3
    assert event.start_hour == 7
    assert event.start_minute == 8


def test_start_and_end_same_1():
    event = Event()
    event.load_from_yaml_data(
        "id",
        {"start": "2021-01-03 07:08", "end": "2021-01-03 07:08"},
        "events/id/event.yaml",
    )
    assert event.start_year == 2021
    assert event.start_month == 1
    assert event.start_day == 3
    assert event.start_hour == 7
    assert event.start_minute == 8
    assert event.end_year == 2021
    assert event.end_month == 1
    assert event.end_day == 3
    assert event.end_hour == 7
    assert event.end_minute == 8


def test_start_end_no_padding_1():
    event = Event()
    event.load_from_yaml_data(
        "id",
        {"start": "2021-01-03 7:8", "end": "2021-01-03 8:8"},
        "events/id/event.yaml",
    )
    assert event.start_year == 2021
    assert event.start_month == 1
    assert event.start_day == 3
    assert event.start_hour == 7
    assert event.start_minute == 8


def test_start_with_no_end_1():
    event = Event()
    event.load_from_yaml_data(
        "id", {"start": "2021-01-03 07:08"}, "events/id/event.yaml"
    )
    assert event.start_year == 2021
    assert event.start_month == 1
    assert event.start_day == 3
    assert event.start_hour == 7
    assert event.start_minute == 8
    # End just the same as the start
    assert event.end_year == 2021
    assert event.end_month == 1
    assert event.end_day == 3
    assert event.end_hour == 7
    assert event.end_minute == 8


def test_end_is_before_start_1():
    event = Event()
    with pytest.raises(EndIsBeforeStartException):
        event.load_from_yaml_data(
            "id",
            {"start": "2021-01-03 7:8", "end": "2021-01-03 7:7"},
            "events/id/event.yaml",
        )

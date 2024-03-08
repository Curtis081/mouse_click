import pytest

import datetime
from mouse_click import is_time_in_range, get_time_from_user, get_validated_time_range, get_delay_time


def test_is_time_in_range():
    start = datetime.time(8, 0)
    end = datetime.time(18, 0)
    current_time = datetime.time(12, 30)
    assert is_time_in_range(start, end, current_time) is True
    assert is_time_in_range(end, start, current_time) is False

    current_time = datetime.time(7, 59)
    assert is_time_in_range(start, end, current_time) is False
    current_time = datetime.time(8, 0)
    assert is_time_in_range(start, end, current_time) is True
    current_time = datetime.time(18, 0)
    assert is_time_in_range(start, end, current_time) is True
    current_time = datetime.time(18, 1)
    assert is_time_in_range(start, end, current_time) is False


def test_get_time_from_user(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: '10:30')
    assert get_time_from_user("Enter a time (HH:MM): ") == datetime.time(10, 30)


def test_get_validated_time_range(monkeypatch):
    start_time = datetime.time(9, 0)
    end_time = datetime.time(18, 0)
    responses = iter([start_time.strftime("%H:%M"), end_time.strftime("%H:%M")])
    monkeypatch.setattr('builtins.input', lambda msg: next(responses))
    start, end = get_validated_time_range("Enter start time (HH:MM): ", "Enter end time (HH:MM): ",
                                          default_start_time=datetime.time(8, 0),
                                          default_end_time=datetime.time(18, 0))
    assert start == start_time
    assert end == end_time


def test_get_validated_time_range_press_d(monkeypatch):
    default_start_time = datetime.time(8, 0)
    default_end_time = datetime.time(18, 0)
    responses = iter(["d", "d"])
    monkeypatch.setattr('builtins.input', lambda msg: next(responses))
    start, end = get_validated_time_range("Enter start time (HH:MM): ", "Enter end time (HH:MM): ",
                                          default_start_time=default_start_time,
                                          default_end_time=default_end_time)
    assert start == default_start_time
    assert end == default_end_time


def test_get_validated_time_range_press_d_d(monkeypatch):
    default_start_time = datetime.time(8, 0)
    default_end_time = datetime.time(18, 0)
    responses = iter(["x", "d", "y", "d"])
    monkeypatch.setattr('builtins.input', lambda msg: next(responses))
    start, end = get_validated_time_range("Enter start time (HH:MM): ", "Enter end time (HH:MM): ",
                                          default_start_time=default_start_time,
                                          default_end_time=default_end_time)
    assert start == default_start_time
    assert end == default_end_time


def test_get_validated_time_range_press_raise_error(monkeypatch):
    with pytest.raises(StopIteration):
        default_start_time = datetime.time(8, 0)
        default_end_time = datetime.time(18, 0)
        responses = iter(["x", "d", "y"])
        monkeypatch.setattr('builtins.input', lambda msg: next(responses))
        start, end = get_validated_time_range("Enter start time (HH:MM): ",
                                              "Enter end time (HH:MM): ",
                                              default_start_time=default_start_time,
                                              default_end_time=default_end_time)


def test_get_delay_time(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: '120')
    assert get_delay_time("Enter delay time (seconds): ") == 120

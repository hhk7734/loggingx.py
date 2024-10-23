from datetime import datetime, timezone

from .json import _json_dumps, _orjson_dumps

dump_cases = [
    (datetime(2024, 1, 1, 0, 0, 0, 0, tzinfo=timezone.utc), "2024-01-01T00:00:00+00:00"),
]


def test_json_dumps() -> None:
    for input, expected in dump_cases:
        assert _json_dumps({"a": input}) == f'{{"a": "{expected}"}}'


def test_orjson_dumps() -> None:
    for input, expected in dump_cases:
        assert _orjson_dumps({"a": input}) == f'{{"a":"{expected}"}}'


def test_dumps() -> None:
    assert 0

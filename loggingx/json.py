import json
from datetime import datetime
from typing import Any

try:
    import orjson

    orjson_imported = True
except ImportError:
    orjson_imported = False


def _default(obj: Any) -> str:
    if isinstance(obj, datetime):
        return obj.isoformat(sep="T")

    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


def _orjson_dumps(obj: Any) -> str:
    return orjson.dumps(obj, default=_default).decode()


def _json_dumps(obj: Any) -> str:
    # Set ensure_ascii to False to output the message as it is typed.
    return json.dumps(obj, ensure_ascii=False, default=_default)


if orjson_imported:
    dumps = _orjson_dumps
else:
    dumps = _json_dumps

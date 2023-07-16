from contextlib import contextmanager
from contextvars import ContextVar
from typing import Any, Generator

_ctx = ContextVar[dict[str, Any]]("ctxLoggerContext", default={})


@contextmanager
def addFields(reset: bool = True, **fields: Any) -> Generator[None, Any, None]:
    token = _ctx.set({**_ctx.get(), **fields})
    try:
        yield
    finally:
        if reset:
            _ctx.reset(token)


def getFields() -> dict[str, Any]:
    return _ctx.get()

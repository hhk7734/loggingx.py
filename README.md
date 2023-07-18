## loggingx.py

### Context

:warning: `ctxlogger.setCtxRecord()` sets `logging._srcfile = None` and uses the `inspect` module to get the stack frame directly.

```python
import logging

from loggingx import ctxlogger
from loggingx.formatter import JSONFormatter

handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logging.basicConfig(level=logging.INFO, handlers=[handler])
ctxlogger.setCtxRecord()


def A() -> None:
    logging.info("A")
    with ctxlogger.addFields(A="a"):
        B()


def B() -> None:
    logging.info("B")
    with ctxlogger.addFields(B="b"):
        C()


def C() -> None:
    logging.info("C")


if __name__ == "__main__":
    A()
```

```json
{"time": 1689680850.3346911, "level": "info", "caller": "loggingx.py/main.py:13", "msg": "A"}
{"time": 1689680850.3349278, "level": "info", "caller": "loggingx.py/main.py:19", "msg": "B", "A": "a"}
{"time": 1689680850.3351411, "level": "info", "caller": "loggingx.py/main.py:25", "msg": "C", "A": "a", "B": "b"}
```

### JSONFormatter

```python
import logging

from loggingx.formatter import JSONFormatter

handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logging.basicConfig(level=logging.INFO, handlers=[handler])

if __name__ == "__main__":
    logging.info("test", extra={"test": "test"})
```

```json
{"time": 1689680910.3116627, "level": "info", "caller": "loggingx.py/main.py:10", "msg": "test", "test": "test"}
```
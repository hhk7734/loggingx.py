## loggingx.py

`loggingx` is a drop-in replacement for Python's built-in `logging` module. Even better, once you've imported `loggingx`, you don't need to modify your existing `logging` module.

```shell
python3 -m pip install loggingx-py
```

### Additional Format

- https://docs.python.org/3/library/logging.html#logrecord-attributes

| Attribute name | Format | Description |
| --- | --- | --- |
| caller | %(caller)s | Caller(`<pathname>:<lineno>`) |
| ctxFields | %(ctxFields)s | Context fields |


### Context

```python
import loggingx

loggingx.basicConfig(
    level=loggingx.INFO,
    format="%(asctime)s\t%(levelname)s\t%(caller)s\t%(message)s\t%(ctxFields)s",
)


def A() -> None:
    loggingx.info("A")
    with loggingx.addFields(A="a"):
        B()


def B() -> None:
    loggingx.info("B")
    with loggingx.addFields(B="b"):
        C()


def C() -> None:
    loggingx.info("C")


if __name__ == "__main__":
    A()
```

```shell
2023-07-19 01:15:33,981 INFO    loggingx.py/main.py:10  A       {}
2023-07-19 01:15:33,981 INFO    loggingx.py/main.py:16  B       {'A': 'a'}
2023-07-19 01:15:33,982 INFO    loggingx.py/main.py:22  C       {'A': 'a', 'B': 'b'}
```

### JSONFormatter

```python
import loggingx

handler = loggingx.StreamHandler()
handler.setFormatter(loggingx.JSONFormatter())
loggingx.basicConfig(level=loggingx.INFO, handlers=[handler])

if __name__ == "__main__":
    with loggingx.addFields(ctx="ctx"):
        loggingx.info("test", extra={"extra": "extra"})
```

```json
{"time": 1689697694.9980711, "level": "info", "caller": "loggingx.py/main.py:9", "msg": "test", "ctx": "ctx", "extra": "extra"}
```

### With `logging`

```python
import logging

import loggingx

# handler = loggingx.StreamHandler()
handler = logging.StreamHandler()
handler.setFormatter(loggingx.JSONFormatter())

# loggingx.basicConfig(level=loggingx.INFO, handlers=[handler])
logging.basicConfig(level=logging.INFO, handlers=[handler])

if __name__ == "__main__":
    with loggingx.addFields(ctx="ctx"):
        # loggingx.info("test", extra={"extra": "extra"})
        logging.info("test", extra={"extra": "extra"})
```
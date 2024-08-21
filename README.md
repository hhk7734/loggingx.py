![license](https://img.shields.io/github/license/hhk7734/loggingx.py)
![pypi](https://img.shields.io/pypi/v/loggingx-py)
![language](https://img.shields.io/github/languages/top/hhk7734/loggingx.py)

# loggingx.py

`loggingx` is a drop-in replacement for Python's built-in `logging` module. Even better, once you've imported `loggingx`, you don't need to modify your existing `logging` module.

```shell
python3 -m pip install loggingx-py
```

## Additional Format

- https://docs.python.org/3/library/logging.html#logrecord-attributes

| Attribute name | Format        | Description                   |
| -------------- | ------------- | ----------------------------- |
| caller         | %(caller)s    | Caller(`<pathname>:<lineno>`) |
| ctxFields      | %(ctxFields)s | Context fields                |

## Optimization

| Configuration                | Description                                                    |
| ---------------------------- | -------------------------------------------------------------- |
| `logging.logThreads`         | If `False`, Record will not collect `thread` and `threadName`. |
| `logging.logProcesses`       | If `False`, Record will not collect `process`.                 |
| `logging.logMultiprocessing` | If `False`, Record will not collect `processName`.             |


## Context

```python
import loggingx as logging

handler = logging.StreamHandler()
handler.setFormatter(logging.ConsoleFormatter())
logging.basicConfig(level=logging.INFO, handlers=[handler])


def A() -> None:
    logging.info("A")
    with logging.addFields(A="a"):
        B()


def B() -> None:
    logging.info("B")
    with logging.addFields(B="b"):
        C()


def C() -> None:
    logging.info("C")


if __name__ == "__main__":
    A()
```

```shell
2024-08-22T02:46:38.257+09:00 INFO   main.py:9  A {}
2024-08-22T02:46:38.257+09:00 INFO   main.py:15 B {"A": "a"}
2024-08-22T02:46:38.258+09:00 INFO   main.py:21 C {"A": "a", "B": "b"}
```

## Formatter

### JSONFormatter

```python
import loggingx as logging

handler = logging.StreamHandler()
# handler.setFormatter(logging.JSONFormatter())
handler.setFormatter(logging.JSONFormatter(logging.Information.THREAD_NAME))
logging.basicConfig(level=logging.INFO, handlers=[handler])

if __name__ == "__main__":
    with logging.addFields(ctx="ctx"):
        logging.info("test", extra={"extra": "extra"})
```

```json
{
  "time": 1689697694.9980711,
  "level": "info",
  "caller": "main.py:10",
  "msg": "test",
  "ctx": "ctx",
  "thread_name": "MainThread",
  "extra": "extra"
}
```

### ConsoleFormatter

```python
import loggingx as logging

handler = logging.StreamHandler()
handler.setFormatter(logging.ConsoleFormatter())
logging.basicConfig(level=logging.INFO, handlers=[handler])

if __name__ == "__main__":
    with logging.addFields(ctx="ctx"):
        logging.info("test", extra={"extra": "extra"})
```

```shell
2024-08-22T02:48:17.868+09:00 INFO   main.py:9  test {"ctx": "ctx", "extra": "extra"}
```

## With `logging`

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

## jq

```shell
alias log2jq="jq -rRC --unbuffered '. as \$line | try fromjson catch \$line' | sed 's/\\\\n/\\n/g; s/\\\\t/\\t/g'"
```

```shell
python3 <path> 2>&1 | log2jq
```

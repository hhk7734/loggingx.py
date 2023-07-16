## loggingx.py

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
{"time": 1689518912.4938014, "level": "info", "msg": "test", "caller": "loggingx.py/test.py:10", "test": "test"}
```
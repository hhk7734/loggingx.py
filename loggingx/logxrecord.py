import inspect
import json
import logging
from logging import LogRecord

from loggingx.ctxlogger import getFields


class LogxRecord(LogRecord):
    def __init__(
        self, name, level, pathname, lineno, msg, args, exc_info, func=None, sinfo=None, **kwargs
    ):
        frames = inspect.getouterframes(inspect.currentframe())
        depth = 4
        while frames[depth].filename.endswith("logging/__init__.py"):
            depth += 1

        frame = frames[depth]
        pathname = frame.filename
        lineno = frame.lineno
        func = frame.function

        # TODO: if stack_info == True, use traceback.print_stack(frame, file=sio)
        sinfo = None

        self.caller = "/".join(pathname.split("/")[-2:]) + f":{lineno}"
        self.logxCtx = getFields()

        super().__init__(name, level, pathname, lineno, msg, args, exc_info, func, sinfo, **kwargs)

    def __repr__(self):
        return json.dumps(self.__dict__, ensure_ascii=False)


def setLogRecordFactoryToLogxRecord():
    logging._srcfile = None  # pylint: disable=protected-access
    logging.setLogRecordFactory(LogxRecord)

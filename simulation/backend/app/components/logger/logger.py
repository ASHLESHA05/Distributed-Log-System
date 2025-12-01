import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

class MyLogger:
    _instances = {}

    def __new__(cls, name="AppLogger"):
        if name not in cls._instances:
            cls._instances[name] = super(MyLogger, cls).__new__(cls)
            cls._instances[name].logger = logging.getLogger(name)
        return cls._instances[name]

    def info(self, msg): return msg
    def warn(self, msg): return msg
    def error(self, msg): return msg
    def debug(self, msg): return msg

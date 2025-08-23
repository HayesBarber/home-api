from datetime import datetime
from zoneinfo import ZoneInfo

class LOGGER:
    @staticmethod
    def get_now() -> datetime:
        return datetime.now(ZoneInfo("America/New_York"))

    @classmethod
    def _format_prefix(cls) -> str:
        now = cls.get_now()
        formatted = now.strftime("[%a, %b %d %I:%M:%S %p]")
        return formatted

    @classmethod
    def epoch_seconds(cls) -> str:
        now = cls.get_now()
        adjusted = now.timestamp() + now.utcoffset().total_seconds()
        return str(int(adjusted))

    @classmethod
    def current_date(cls) -> str:
        now = cls.get_now()
        return now.strftime("%a, %b %d")

    @classmethod
    def log(cls, message: str, level: str = None) -> None:
        prefix = cls._format_prefix()
        level_str = f" [{level.upper()}]" if level else ""
        print(f"{prefix}{level_str} {message}")

    @classmethod
    def info(cls, message: str) -> None:
        cls.log(message, level="info")

    @classmethod
    def warn(cls, message: str) -> None:
        cls.log(message, level="warn")

    @classmethod
    def error(cls, message: str) -> None:
        cls.log(message, level="error")

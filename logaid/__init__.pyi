from typing import Any, Literal, Mapping

LogLevel = Literal["DEBUG", "INFO", "SUCCESS", "WARN", "WARNING", "ERROR", "FATAL", "CRITICAL"]
RotatingWhen = Literal[
    "",
    "day",
    "size",
    "day-size",
    "midnight",
    "S",
    "M",
    "H",
    "D",
    "W0",
    "W1",
    "W2",
    "W3",
    "W4",
    "W5",
    "W6",
]

def debug(*args: Any, **kwargs: Any) -> Any: ...
def info(*args: Any, **kwargs: Any) -> Any: ...
def success(*args: Any, **kwargs: Any) -> Any: ...
def warning(*args: Any, **kwargs: Any) -> Any: ...
def error(*args: Any, **kwargs: Any) -> Any: ...
def fatal(*args: Any, **kwargs: Any) -> Any: ...
def critical(*args: Any, **kwargs: Any) -> Any: ...

def init(
    name: str = ...,
    level: LogLevel = ...,
    filename: str | bool = ...,
    save: bool = ...,
    save_mode: str = ...,
    format: str | bool = ...,
    show: bool = ...,
    print_pro: bool = ...,
    color: Mapping[str, str] = ...,
    rotating: RotatingWhen = ...,
) -> None: ...

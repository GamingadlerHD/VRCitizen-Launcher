import os
import inspect
from datetime import datetime
from colorama import init, Fore, Style


# warn, error, log enum
class LogLevel:
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"

# Initialisiere colorama
init(autoreset=True)


log_dir = "./logs"
os.makedirs(log_dir, exist_ok=True)

log_file_path = os.path.join(log_dir, f"{datetime.now().strftime('%Y-%m-%d')}.log")

def write_to_file(level: str, message: str) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file_path, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] [{level}] {message}\n")

def get_caller_filename() -> str:
    stack = inspect.stack()
    # stack[2] is the caller of log/warn/error
    if len(stack) > 3:
        return os.path.basename(stack[3].filename)
    return ""

def log_message(level: str, message: str, *args, **kwargs) -> None:
    msg = message.format(*args, **kwargs)
    caller = get_caller_filename()
    color = {
        LogLevel.INFO: Fore.WHITE,
        LogLevel.WARNING: Fore.YELLOW,
        LogLevel.ERROR: Fore.RED
    }.get(level, Fore.WHITE)
    prefix = f"{color}[{level}]"
    output_msg = f"{caller}: {msg}" if caller else msg
    print(f"{prefix} {output_msg}{Style.RESET_ALL}")
    write_to_file(level, output_msg)

def log(message: str, *args, **kwargs) -> None:
    log_message(LogLevel.INFO, message, *args, **kwargs)

def error(message: str, *args, **kwargs) -> None:
    log_message(LogLevel.ERROR, message, *args, **kwargs)

def warn(message: str, *args, **kwargs) -> None:
    log_message(LogLevel.WARNING, message, *args, **kwargs)
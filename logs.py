import os
from datetime import datetime
from colorama import init, Fore, Style

# Initialisiere colorama
init(autoreset=True)

log_dir = "./logs"
os.makedirs(log_dir, exist_ok=True)

log_file_path = os.path.join(log_dir, f"{datetime.now().strftime('%Y-%m-%d')}.log")

def write_to_file(level: str, message: str) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file_path, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] [{level}] {message}\n")

def log(message: str, *args, **kwargs) -> None:
    msg = message.format(*args, **kwargs)
    print(f"{Fore.WHITE}[INFO] {msg}{Style.RESET_ALL}")
    write_to_file("INFO", msg)

def warn(message: str, *args, **kwargs) -> None:
    msg = message.format(*args, **kwargs)
    print(f"{Fore.YELLOW}[WARNING] {msg}{Style.RESET_ALL}")
    write_to_file("WARNING", msg)

def error(message: str, *args, **kwargs) -> None:
    msg = message.format(*args, **kwargs)
    print(f"{Fore.RED}[ERROR] {msg}{Style.RESET_ALL}")
    write_to_file("ERROR", msg)

from colorama import init, Fore, Style

init(autoreset=True)

def log(message: str, *args, **kwargs) -> None:
    """
    Print an info message.
    """
    print(f"{Fore.WHITE}[INFO] {message.format(*args, **kwargs)}{Style.RESET_ALL}")

def warn(message: str, *args, **kwargs) -> None:
    """
    Print a warning message.
    """
    print(f"{Fore.YELLOW}[WARNING] {message.format(*args, **kwargs)}{Style.RESET_ALL}")

def error(message: str, *args, **kwargs) -> None:
    """
    Print an error message.
    """
    print(f"{Fore.RED}[ERROR] {message.format(*args, **kwargs)}{Style.RESET_ALL}")
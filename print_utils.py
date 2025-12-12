def text_separator(symbol: str = '-') -> str: return symbol[0] * 80

def text_red(text: str) -> str: return f"\033[91m{text}\033[0m"

def text_green(text: str) -> str: return f"\033[92m{text}\033[0m"

def print_error(text: str): print(text_red(text))

def print_success(text: str): print(text_green(text))

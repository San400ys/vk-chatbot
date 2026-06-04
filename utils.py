import re

def is_positive_number(text: str) -> bool:
    return bool(re.match(r'^\d+(?:[.,]\d+)?$', text.strip()))

def parse_number(text: str) -> float:
    text = text.strip().replace(',', '.')
    return abs(float(text))

def format_currency(amount: float) -> str:
    return f"{amount:,.2f} руб.".replace(',', ' ')

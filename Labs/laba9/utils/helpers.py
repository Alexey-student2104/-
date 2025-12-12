# Вспомогательные функции

import json
from datetime import datetime
from typing import Any, Dict

def json_serial(obj: Any) -> str:
    """JSON сериализатор для объектов datetime"""
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

def format_currency(value: float, currency: str = 'RUB') -> str:
    """Форматирование денежных значений"""
    return f"{value:,.2f} {currency}"

def safe_json_loads(data: str) -> Dict:
    """Безопасная загрузка JSON"""
    try:
        return json.loads(data)
    except:
        return {}
# Декораторы для проверки авторизации и других целей

from functools import wraps
from typing import Callable, Any

def login_required(func: Callable) -> Callable:
    """Декоратор для проверки авторизации пользователя"""
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        # Здесь будет проверка авторизации
        # В текущей реализации проверка делается в обработчике
        return func(*args, **kwargs)
    return wrapper
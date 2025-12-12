import sys
import io
import logging
from functools import wraps
from typing import Callable, Any
import requests
import json
from datetime import datetime


def logger(func: Callable = None, *, handle=sys.stdout) -> Callable:
    """
    Декоратор для логирования вызовов функций.
    
    Args:
        func: Декорируемая функция (если используется как @logger)
        handle: Объект для логирования (sys.stdout, файл, или logging.Logger)
        
    Returns:
        Декорированная функция
    """
    def decorator(original_func: Callable) -> Callable:
        @wraps(original_func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Определяем способ логирования
            is_logger = isinstance(handle, logging.Logger)
            
            # Логируем начало выполнения
            func_name = original_func.__name__
            
            if is_logger:
                handle.info(f"Calling {func_name} with args={args}, kwargs={kwargs}")
            else:
                handle.write(f"INFO: Calling {func_name} with args={args}, kwargs={kwargs}\n")
                if hasattr(handle, 'flush'):
                    handle.flush()
            
            try:
                # Выполняем функцию
                result = original_func(*args, **kwargs)
                
                # Логируем успешное завершение
                if is_logger:
                    handle.info(f"{func_name} returned {result}")
                else:
                    handle.write(f"INFO: {func_name} returned {result}\n")
                    if hasattr(handle, 'flush'):
                        handle.flush()
                
                return result
                
            except Exception as e:
                # Логируем ошибку
                if is_logger:
                    handle.error(f"Function {func_name} raised {type(e).__name__}: {str(e)}")
                else:
                    handle.write(f"ERROR: Function {func_name} raised {type(e).__name__}: {str(e)}\n")
                    if hasattr(handle, 'flush'):
                        handle.flush()
                
                # Пробрасываем исключение дальше
                raise
        
        return wrapper
    
    # Обработка вызова декоратора с аргументами и без
    if func is None:
        return decorator
    else:
        return decorator(func)


def get_currencies(currency_codes: list, url: str = "https://www.cbr-xml-daily.ru/daily_json.js") -> dict:
    """
    Получает курсы валют от API ЦБ РФ.
    
    Args:
        currency_codes: Список кодов валют (например, ['USD', 'EUR'])
        url: URL API ЦБ РФ
        
    Returns:
        Словарь с курсами валют {код: курс}
        
    Raises:
        ConnectionError: Если API недоступен
        ValueError: Если получен некорректный JSON
        KeyError: Если отсутствует ключ "Valute" или валюта
        TypeError: Если курс валюты имеет неверный тип
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        raise ConnectionError(f"Ошибка при запросе к API: {str(e)}")
    
    try:
        data = response.json()
    except json.JSONDecodeError as e:
        raise ValueError(f"Некорректный JSON: {str(e)}")
    
    if "Valute" not in data:
        raise KeyError("Ключ 'Valute' отсутствует в данных API")
    
    valutes = data["Valute"]
    result = {}
    
    for code in currency_codes:
        if code not in valutes:
            raise KeyError(f"Валюта '{code}' отсутствует в данных API")
        
        valute_data = valutes[code]
        if "Value" not in valute_data:
            raise KeyError(f"Ключ 'Value' отсутствует для валюты '{code}'")
        
        value = valute_data["Value"]
        if not isinstance(value, (int, float)):
            raise TypeError(f"Курс валюты '{code}' имеет неверный тип: {type(value)}")
        
        result[code] = value
    
    return result


# Демонстрационная функция для решения квадратных уравнений
def solve_quadratic(a: float, b: float, c: float) -> tuple:
    """
    Решает квадратное уравнение ax^2 + bx + c = 0
    
    Returns:
        Кортеж корней уравнения или None если корней нет
    """
    # Проверка входных данных
    if not all(isinstance(x, (int, float)) for x in (a, b, c)):
        raise TypeError("Коэффициенты должны быть числами")
    
    # Обработка вырожденных случаев
    if a == 0 and b == 0:
        raise ValueError("Уравнение вырождено: a и b равны 0")
    
    if a == 0:
        # Линейное уравнение
        return (-c / b,)
    
    # Вычисление дискриминанта
    D = b**2 - 4*a*c
    
    if D < 0:
        # Дискриминант отрицательный - нет действительных корней
        return None
    elif D == 0:
        x = -b / (2*a)
        return (x,)
    else:
        x1 = (-b + D**0.5) / (2*a)
        x2 = (-b - D**0.5) / (2*a)
        return (x1, x2)


# Настройка файлового логирования
def setup_file_logging(filename: str = "currency.log") -> logging.Logger:
    """Настраивает логирование в файл"""
    logger = logging.getLogger("currency_file")
    logger.setLevel(logging.DEBUG)
    
    # Очищаем существующие обработчики
    logger.handlers.clear()
    
    # Создаем обработчик для файла
    file_handler = logging.FileHandler(filename, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    
    # Форматтер
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    
    return logger


# Основная демонстрация
if __name__ == "__main__":
    # 1. Демонстрация logged_get_currencies (stdout)
    print("== Демонстрация logged_get_currencies (stdout) ==")
    
    # Создаем обернутую версию get_currencies
    @logger
    def logged_get_currencies(codes):
        return get_currencies(codes)
    
    try:
        # Попробуем получить реальные курсы
        currencies = logged_get_currencies(['USD', 'EUR'])
        print(f"Курсы: {currencies}")
    except Exception as e:
        # Если нет интернета, используем тестовые данные
        print(f"Не удалось получить реальные курсы: {e}")
        print("Используем тестовые данные...")
        
        @logger
        def logged_get_currencies_test(codes):
            return {'USD': 76.0937, 'EUR': 88.7028}
        
        currencies = logged_get_currencies_test(['USD', 'EUR'])
        print(f"Курсы: {currencies}")
    
    print()
    
    # 2. Демонстрация file_logged_get_currencies (лог в currency.log)
    print("== Демонстрация file_logged_get_currencies (лог в currency.log) ==")
    
    try:
        # Настраиваем логирование в файл
        file_logger = setup_file_logging("currency.log")
        
        @logger(handle=file_logger)
        def file_logged_get_currencies(codes):
            return {'USD': 76.0937, 'EUR': 88.7028}
        
        currencies = file_logged_get_currencies(['USD', 'EUR'])
        print(f"Курсы: {currencies}")
        print("Подробности см. в файле currency.log")
        
        # Закрываем обработчики
        for handler in file_logger.handlers:
            handler.close()
            
    except Exception as e:
        print(f"Ошибка при работе с файловым логированием: {e}")
    
    print()
    
    # 3. Демонстрация solve_quadratic (лог в quadratic.log)
    print("== Демонстрация solve_quadratic (лог в quadratic.log) ==")
    
    # Настраиваем отдельный логгер для квадратных уравнений
    quadratic_logger = logging.getLogger("quadratic")
    quadratic_logger.setLevel(logging.DEBUG)
    quadratic_logger.handlers.clear()
    
    # Создаем обработчик для файла
    quad_file_handler = logging.FileHandler("quadratic.log", encoding='utf-8')
    quad_file_handler.setLevel(logging.DEBUG)
    quad_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    quad_file_handler.setFormatter(quad_formatter)
    quadratic_logger.addHandler(quad_file_handler)
    
    # Обертываем solve_quadratic
    @logger(handle=quadratic_logger)
    def logged_solve_quadratic(a, b, c):
        return solve_quadratic(a, b, c)
    
    # Пример 1: два корня
    roots1 = logged_solve_quadratic(1, -3, 2)
    print(f"Корни x^2 - 3x + 2: {roots1}")
    
    # Пример 2: нет действительных корней
    roots2 = logged_solve_quadratic(1, 0, 1)
    print(f"Корни x^2 + 1 = 0: {roots2}")
    
    # Закрываем обработчики
    for handler in quadratic_logger.handlers:
        handler.close()
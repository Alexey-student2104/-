**Отчёт по лабораторной работе №7**
Декоратор для логирования функций

---

## Цели работы

Разработать параметризуемый декоратор logger, способный логировать вызовы функций в разные источники (консоль, файл, модуль logging), и применить его для логирования функции получения курсов валют с API ЦБ РФ.

---

## 1. Исходный код декоратора `logger`

```python
import sys
import logging
from functools import wraps
from typing import Callable, Any

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
````

Полный код см. в файле `lab7.py`.

---

## 2. Исходный код функции `get_currencies`

```python
import requests
import json

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
        raise ConnectionError(f"API недоступен: {str(e)}")
    
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
```

---

## 3. Демонстрационный пример: решение квадратного уравнения

Функция логирует:

* **INFO** — начало/конец вызова (через декоратор);
* **WARNING** — дискриминант < 0;
* **ERROR / CRITICAL** — некорректные параметры.

```python
import requests
import json

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
        raise ConnectionError(f"API недоступен: {str(e)}")
    
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
```

---

## 4. Примеры логов

### 4.1 Логирование в stdout

*(Скриншот из демонстрации)*

![demo](https://github.com/user-attachments/assets/f7b66ccd-5c81-48cd-99dc-d9bc182f410f)


---

### ✔ 4.2 Логирование в тестах

![tests_log](https://github.com/user-attachments/assets/a44dd05d-fdcb-4a5b-a9c7-d29f6e2fa34f)

---

## 📌 5. Тестирование

Тесты находятся в файле `test7.py`.

### ✔ 5.1 Тесты функции `get_currencies`

Проверяют:

* корректность полученного курса;
* выброс `KeyError` для отсутствующей валюты;
* выброс `ConnectionError` при неверном URL.

```python
import unittest
from unittest.mock import Mock, patch
import lab7
from requests.exceptions import RequestException

class TestGetCurrencies(unittest.TestCase):
    
    def setUp(self):
        self.mock_response_data = {
            "Valute": {
                "USD": {"Value": 93.25},
                "EUR": {"Value": 101.7},
                "JPY": {"Value": 0.625}
            }
        }
    
    @patch('lab7.requests.get')
    def test_get_currencies_success(self, mock_get):
        """Тестирование успешного получения курсов валют"""
        mock_response = Mock()
        mock_response.json.return_value = self.mock_response_data
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = lab7.get_currencies(['USD', 'EUR'])
        self.assertEqual(result, {"USD": 93.25, "EUR": 101.7})
        mock_get.assert_called_once()
    
    @patch('lab7.requests.get')
    def test_get_currencies_nonexistent_currency(self, mock_get):
        """Тестирование с несуществующей валютой"""
        mock_response = Mock()
        mock_response.json.return_value = self.mock_response_data
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        with self.assertRaises(KeyError) as context:
            lab7.get_currencies(['GBP'])
        self.assertIn("Валюта 'GBP' отсутствует", str(context.exception))
    
    @patch('lab7.requests.get')
    def test_get_currencies_connection_error(self, mock_get):
        """Тестирование при недоступном API"""
        mock_get.side_effect = RequestException("Connection failed")
        
        with self.assertRaises(ConnectionError) as context:
            lab7.get_currencies(['USD'])
        self.assertIn("API недоступен", str(context.exception))
    
    @patch('lab7.requests.get')
    def test_get_currencies_invalid_json(self, mock_get):
        """Тестирование при некорректном JSON"""
        import json
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
        mock_get.return_value = mock_response
        
        with self.assertRaises(ValueError) as context:
            lab7.get_currencies(['USD'])
        self.assertIn("Некорректный JSON", str(context.exception))
```

---

### ✔ 5.2 Тестирование декоратора logger через StringIO


```python
import io

class TestLoggerWithStringIO(unittest.TestCase):
    
    def setUp(self):
        self.stream = io.StringIO()
    
    def test_logger_with_stringio(self):
        """Тестирование логирования в StringIO"""
        @lab7.logger(handle=self.stream)
        def multiply(x, y):
            return x * y
        
        result = multiply(4, 5)
        self.assertEqual(result, 20)
        
        logs = self.stream.getvalue()
        self.assertIn("INFO: Calling multiply", logs)
        self.assertIn("INFO: multiply returned 20", logs)
    
    def test_logging_success_with_stream(self):
        """Тестирование логирования успешного вызова"""
        @lab7.logger(handle=self.stream)
        def test_function(x):
            return x * 2
        
        result = test_function(3)
        self.assertEqual(result, 6)
        
        logs = self.stream.getvalue()
        print("\n=== SUCCESS LOGS ===")
        print(logs.strip())
        
        self.assertIn("INFO: Calling test_function", logs)
        self.assertIn("INFO: test_function returned 6", logs)
```

---

### ✔ 5.3 Тест контекстного вызова из задания

```python
class TestStreamWrite(unittest.TestCase):
    """Тестирование с использованием StringIO (контекст из задания)"""
    
    def setUp(self):
        """Настройка перед каждым тестом"""
        self.stream = io.StringIO()
        
        @lab7.logger(handle=self.stream)
        def wrapped():
            return lab7.get_currencies(['USD'], url="https://invalid")
        
        self.wrapped = wrapped
    
    @patch('lab7.requests.get')
    def test_logging_error(self, mock_get):
        """Тестирование логирования ошибки (тест из задания)"""
        # Настраиваем мок для выброса исключения
        mock_get.side_effect = RequestException("Connection failed")
        
        # Проверяем, что исключение пробрасывается
        with self.assertRaises(ConnectionError):
            self.wrapped()
        
        # Получаем логи
        logs = self.stream.getvalue()
        
        # Проверяем наличие ошибки в логах (как в задании)
        self.assertIn("ERROR", logs)
        self.assertIn("ConnectionError", logs)
        
        # Дополнительные проверки (из задания)
        self.assertRegex(logs, "ERROR")
        print("\n=== STREAM LOGS (контекстный тест) ===")
        print(logs.strip())
    
    @patch('lab7.requests.get')
    def test_logging_success(self, mock_get):
        """Тестирование логирования успешного выполнения"""
        # Настраиваем мок для успешного ответа
        mock_response = Mock()
        mock_response.json.return_value = {
            "Valute": {
                "USD": {"Value": 76.9708}
            }
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Вызываем функцию
        result = self.wrapped()
        
        # Проверяем результат
        self.assertEqual(result, {"USD": 76.9708})
        
        # Проверяем логи
        logs = self.stream.getvalue()
        self.assertIn("INFO: Calling wrapped", logs)
        self.assertIn("INFO: wrapped returned", logs)
        self.assertIn("USD", logs)
    
    def test_stream_io_interface(self):
        """Тестирование работы с интерфейсом файла (StringIO)"""
        # Проверяем что stream поддерживает интерфейс файла
        self.assertTrue(hasattr(self.stream, 'write'))
        self.assertTrue(hasattr(self.stream, 'getvalue'))
        self.assertTrue(hasattr(self.stream, 'flush'))
        
        # Тестовая запись
        test_message = "Test message"
        self.stream.write(test_message)
        self.stream.flush()
        
        # Проверяем запись
        content = self.stream.getvalue()
        self.assertIn(test_message, content)
```

---

### 5.4 Тесты функции solve_quadratic

```python
import unittest
import io
import lab7
from unittest.mock import patch, Mock
from requests.exceptions import RequestException

class TestSolveQuadratic(unittest.TestCase):
    """Тестирование функции solve_quadratic"""
    
    def test_solve_quadratic_two_roots(self):
        """Тестирование с двумя корнями"""
        result = lab7.solve_quadratic(1, -5, 6)
        self.assertEqual(len(result), 2)
        self.assertAlmostEqual(result[0], 3.0)
        self.assertAlmostEqual(result[1], 2.0)
    
    def test_solve_quadratic_one_root(self):
        """Тестирование с одним корнем"""
        result = lab7.solve_quadratic(1, -4, 4)
        self.assertEqual(len(result), 1)
        self.assertAlmostEqual(result[0], 2.0)
    
    def test_solve_quadratic_no_real_roots(self):
        """Тестирование без действительных корней"""
        result = lab7.solve_quadratic(1, 2, 5)
        self.assertIsNone(result)
    
    def test_solve_quadratic_linear_equation(self):
        """Тестирование линейного уравнения"""
        result = lab7.solve_quadratic(0, 2, -6)
        self.assertEqual(len(result), 1)
        self.assertAlmostEqual(result[0], 3.0)
    
    def test_solve_quadratic_invalid_input(self):
        """Тестирование с некорректными данными"""
        with self.assertRaises(TypeError):
            lab7.solve_quadratic("a", 2, 3)
    
    def test_solve_quadratic_degenerate_case(self):
        """Тестирование вырожденного случая"""
        with self.assertRaises(ValueError):
            lab7.solve_quadratic(0, 0, 5)
    
    def test_solve_quadratic_with_logger(self):
        """Тестирование solve_quadratic с декоратором logger"""
        stream = io.StringIO()
        
        @lab7.logger(handle=stream)
        def logged_solve(a, b, c):
            return lab7.solve_quadratic(a, b, c)
        
        # Тест с двумя корнями
        result = logged_solve(1, -3, 2)
        self.assertEqual(len(result), 2)
        
        logs = stream.getvalue()
        self.assertIn("INFO: Calling logged_solve", logs)
        self.assertIn("INFO: logged_solve returned", logs)
        self.assertIn("2.0", logs)  # Проверяем что логи содержат результат
```

---

## 📌 6. Логи в файлах currency.log и quadratic.log

![Uploading currency_log.jpg…]()
![Uploading quadratic_log.jpg…]()

---

## ✔ 7. Вывод

*Выполненные задачи:*
✅ Реализован параметризуемый декоратор logger с поддержкой трёх вариантов логирования

✅ Разработана функция get_currencies для получения курсов валют с обработкой исключений

✅ Создана демонстрационная функция solve_quadratic для решения квадратных уравнений

✅ Реализовано файловое логирование через модуль logging

✅ Написаны комплексные тесты для всех компонентов системы

*Особенности реализации:*
Гибкость декоратора: поддержка stdout, файловых объектов и logging.Logger

Полное логирование: запись начала, успешного завершения и ошибок выполнения

Сохранение сигнатуры: использование functools.wraps для корректной работы декоратора

Обработка ошибок: корректное логирование и проброс исключений

Комплексное тестирование: unit-тесты покрывают все сценарии использования


Все цели работы выполнены.

Мамонтов Алексей (P3120, 504593)

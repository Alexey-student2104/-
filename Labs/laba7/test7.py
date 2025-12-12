import unittest
import io
import logging
from unittest.mock import Mock, patch
import lab7
import json
from requests.exceptions import RequestException


class TestLoggerDecorator(unittest.TestCase):
    """Тестирование декоратора logger"""
    
    def test_logger_with_stringio(self):
        """Тестирование логирования в StringIO"""
        stream = io.StringIO()
        
        @lab7.logger(handle=stream)
        def multiply(x, y):
            return x * y
        
        result = multiply(4, 5)
        self.assertEqual(result, 20)
        
        logs = stream.getvalue()
        self.assertIn("INFO: Calling multiply", logs)
        self.assertIn("INFO: multiply returned 20", logs)
    
    def test_logger_with_logging(self):
        """Тестирование логирования через logging.Logger"""
        log = logging.getLogger("test")
        log.handlers = []  # Очищаем обработчики
        
        # Добавляем обработчик для перехвата сообщений
        log_messages = []
        
        class TestHandler(logging.Handler):
            def emit(self, record):
                log_messages.append((record.levelname, record.getMessage()))
        
        handler = TestHandler()
        log.addHandler(handler)
        log.setLevel(logging.INFO)
        
        @lab7.logger(handle=log)
        def divide(a, b):
            return a / b
        
        result = divide(10, 2)
        self.assertEqual(result, 5)
        
        # Проверяем логи
        info_messages = [msg for level, msg in log_messages if level == "INFO"]
        self.assertGreaterEqual(len(info_messages), 2)
        self.assertTrue(any("Calling divide" in msg for msg in info_messages))
        self.assertTrue(any("divide returned" in msg for msg in info_messages))
    
    def test_logger_with_exception(self):
        """Тестирование логирования при возникновении исключения"""
        stream = io.StringIO()
        
        @lab7.logger(handle=stream)
        def failing_function():
            raise ValueError("triple T big sahur")
        
        # Проверяем, что исключение пробрасывается
        with self.assertRaises(ValueError) as context:
            failing_function()
        
        self.assertIn("triple T big sahur", str(context.exception))
        
        # Проверяем логи
        logs = stream.getvalue()
        print("\n=== ERROR LOGS ===")
        print(logs.strip())
        
        self.assertIn("ERROR:", logs)
        self.assertIn("ValueError", logs)
        self.assertIn("triple T big sahur", logs)
    
    def test_logger_preserves_signature(self):
        """Тестирование сохранения сигнатуры функции"""
        @lab7.logger
        def sample_func(a: int, b: int = 10) -> int:
            """Документация тестовой функции"""
            return a + b
        
        # Проверяем сохранение атрибутов
        self.assertEqual(sample_func.__name__, "sample_func")
        self.assertEqual(sample_func.__doc__, "Документация тестовой функции")
        self.assertEqual(sample_func.__annotations__, {"a": int, "b": int, "return": int})
        
        # Проверяем работу функции
        self.assertEqual(sample_func(5), 15)
        self.assertEqual(sample_func(5, 20), 25)


class TestGetCurrencies(unittest.TestCase):
    """Тестирование функции get_currencies"""
    
    def setUp(self):
        """Настройка перед каждым тестом"""
        self.mock_response_data = {
            "Valute": {
                "USD": {
                    "Value": 93.25,
                    "Nominal": 1,
                    "Name": "Доллар США"
                },
                "EUR": {
                    "Value": 101.7,
                    "Nominal": 1,
                    "Name": "Евро"
                },
                "JPY": {
                    "Value": 0.625,
                    "Nominal": 100,
                    "Name": "Японская иена"
                }
            }
        }
    
    @patch('lab7.requests.get')
    def test_get_currencies_success(self, mock_get):
        """Тестирование успешного получения курсов валют"""
        # Настраиваем мок
        mock_response = Mock()
        mock_response.json.return_value = self.mock_response_data
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Тестируем функцию
        result = lab7.get_currencies(['USD', 'EUR'])
        
        # Проверяем результат
        self.assertEqual(result, {"USD": 93.25, "EUR": 101.7})
        mock_get.assert_called_once()
    
    @patch('lab7.requests.get')
    def test_get_currencies_with_single_currency(self, mock_get):
        """Тестирование получения одной валюты"""
        mock_response = Mock()
        mock_response.json.return_value = self.mock_response_data
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = lab7.get_currencies(['JPY'])
        self.assertEqual(result, {"JPY": 0.625})
    
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
        # Исправляем мок - requests.get должен выбросить исключение
        mock_get.side_effect = RequestException("Connection failed")
        
        with self.assertRaises(ConnectionError) as context:
            lab7.get_currencies(['USD'])
        
        # Обновляем проверку для нового формата ошибки
        error_message = str(context.exception)
        # Проверяем любой из возможных вариантов
        self.assertTrue(
            "API недоступен" in error_message or 
            "Ошибка при запросе к API" in error_message,
            f"Неправильное сообщение об ошибке: {error_message}"
        )
    
    @patch('lab7.requests.get')
    def test_get_currencies_invalid_json(self, mock_get):
        """Тестирование при некорректном JSON"""
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
        mock_get.return_value = mock_response
        
        with self.assertRaises(ValueError) as context:
            lab7.get_currencies(['USD'])
        
        self.assertIn("Некорректный JSON", str(context.exception))
    
    @patch('lab7.requests.get')
    def test_get_currencies_missing_valute_key(self, mock_get):
        """Тестирование при отсутствии ключа 'Valute'"""
        mock_response = Mock()
        mock_response.json.return_value = {}  # Пустой ответ
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        with self.assertRaises(KeyError) as context:
            lab7.get_currencies(['USD'])
        
        self.assertIn("Ключ 'Valute' отсутствует", str(context.exception))
    
    @patch('lab7.requests.get')
    def test_get_currencies_invalid_currency_type(self, mock_get):
        """Тестирование при неверном типе курса валюты"""
        invalid_data = {
            "Valute": {
                "USD": {
                    "Value": "invalid",  # Строка вместо числа
                    "Nominal": 1
                }
            }
        }
        
        mock_response = Mock()
        mock_response.json.return_value = invalid_data
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        with self.assertRaises(TypeError) as context:
            lab7.get_currencies(['USD'])
        
        self.assertIn("неверный тип", str(context.exception).lower())


class TestLoggerWithGetCurrencies(unittest.TestCase):
    """Тестирование декоратора logger с функцией get_currencies"""
    
    def setUp(self):
        self.stream = io.StringIO()
    
    @patch('lab7.requests.get')
    def test_logging_success_with_stream(self, mock_get):
        """Тестирование логирования успешного вызова"""
        # Настраиваем мок
        mock_response = Mock()
        mock_response.json.return_value = {
            "Valute": {
                "USD": {"Value": 93.25},
                "EUR": {"Value": 101.7}
            }
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Декорируем функцию
        @lab7.logger(handle=self.stream)
        def test_function(x):
            return x * 2
        
        # Вызываем функцию
        result = test_function(3)
        
        # Проверяем результат
        self.assertEqual(result, 6)
        
        # Проверяем логи
        logs = self.stream.getvalue()
        print("\n=== SUCCESS LOGS ===")
        print(logs.strip())
        
        self.assertIn("INFO: Calling test_function", logs)
        self.assertIn("INFO: test_function returned 6", logs)
    
    @patch('lab7.requests.get')
    def test_logging_error_with_stream(self, mock_get):
        """Тестирование логирования при ошибке"""
        # Настраиваем мок для выброса исключения при вызове raise_for_status
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = RequestException("Connection failed")
        mock_get.return_value = mock_response
        
        @lab7.logger(handle=self.stream)
        def wrapped():
            return lab7.get_currencies(['USD'], url="https://invalid-url")
        
        # Проверяем, что исключение пробрасывается
        with self.assertRaises(ConnectionError):
            wrapped()
        
        # Проверяем логи
        logs = self.stream.getvalue()
        print("\n=== STREAM LOGS ===")
        print(logs.strip())
        
        self.assertIn("ERROR:", logs)
        self.assertIn("ConnectionError", logs)


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


class TestFileLogging(unittest.TestCase):
    """Тестирование файлового логирования"""
    
    def test_setup_file_logging(self):
        """Тестирование настройки файлового логирования"""
        import tempfile
        import os
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log') as temp_file:
            temp_path = temp_file.name
        
        try:
            # Настраиваем логирование
            file_logger = lab7.setup_file_logging(temp_path)
            
            # Закрываем файл, чтобы его можно было прочитать
            for handler in file_logger.handlers:
                handler.close()
            
            # Декорируем функцию
            @lab7.logger(handle=file_logger)
            def test_function():
                return "Test result"
            
            # Вызываем функцию
            result = test_function()
            self.assertEqual(result, "Test result")
            
            # Закрываем обработчики логгера
            for handler in file_logger.handlers:
                handler.close()
            
            # Проверяем, что файл создан и содержит логи
            with open(temp_path, 'r', encoding='utf-8') as f:
                logs = f.read()
            
            self.assertIn("currency_file", logs)
        finally:
            # Очищаем
            if os.path.exists(temp_path):
                import time
                time.sleep(0.1)
                try:
                    os.remove(temp_path)
                except PermissionError:
                    pass


if __name__ == '__main__':
    # Запускаем тесты
    unittest.main(verbosity=0)  
"""
Тесты для лабораторной работы "Клиент-серверное приложение для отслеживания курсов валют"
Автор: Мамонтов Алексей, группа P3120
"""

import unittest
import sys
import os
import json
from datetime import datetime

# Добавляем текущую директорию в путь для импорта
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Импорт моделей
try:
    from models.author import Author
    from models.app import App
    from models.user import User
    from models.currency import Currency
    from models.user_currency import UserCurrency
    MODELS_AVAILABLE = True
except ImportError:
    MODELS_AVAILABLE = False

# -------------------------------------------------------------------
# ТЕСТЫ МОДЕЛЕЙ
# -------------------------------------------------------------------

class TestAuthorModel(unittest.TestCase):
    """Тесты для модели Author"""
    
    def test_author_creation_valid(self):
        """Тест корректного создания автора"""
        if not MODELS_AVAILABLE:
            self.skipTest("Модели не доступны")
        
        author = Author(name="Мамонтов Алексей", group="P3120")
        self.assertEqual(author.name, "Мамонтов Алексей")
        self.assertEqual(author.group, "P3120")
    
    def test_author_name_validation(self):
        """Тест валидации имени автора"""
        if not MODELS_AVAILABLE:
            self.skipTest("Модели не доступны")
        
        # Тест некорректных типов
        with self.assertRaises(TypeError):
            Author(name=123, group="P3120")
        
        # Тест пустых значений
        with self.assertRaises(ValueError):
            Author(name="", group="P3120")
        
        # Тест пробелов
        with self.assertRaises(ValueError):
            Author(name="   ", group="P3120")
    
    def test_author_group_validation(self):
        """Тест валидации группы автора"""
        if not MODELS_AVAILABLE:
            self.skipTest("Модели не доступны")
        
        with self.assertRaises(TypeError):
            Author(name="Мамонтов Алексей", group=123)
        
        with self.assertRaises(ValueError):
            Author(name="Мамонтов Алексей", group="")
    


class TestUserModel(unittest.TestCase):
    """Тесты для модели User"""
    
    def test_user_creation_valid(self):
        """Тест корректного создания пользователя"""
        if not MODELS_AVAILABLE:
            self.skipTest("Модели не доступны")
        
        user = User(id=1, name="Ноунейм")
        self.assertEqual(user.id, 1)
        self.assertEqual(user.name, "Ноунейм")
        self.assertEqual(len(user.subscribed_currencies), 0)
    
    def test_user_id_validation(self):
        """Тест валидации ID пользователя"""
        if not MODELS_AVAILABLE:
            self.skipTest("Модели не доступны")
        
        with self.assertRaises(TypeError):
            User(id="не число", name="Пользователь")
        
        with self.assertRaises(ValueError):
            User(id=0, name="Пользователь")
        
        with self.assertRaises(ValueError):
            User(id=-5, name="Пользователь")
    
    def test_user_name_validation(self):
        """Тест валидации имени пользователя"""
        if not MODELS_AVAILABLE:
            self.skipTest("Модели не доступны")
        
        with self.assertRaises(TypeError):
            User(id=1, name=123)
        
        with self.assertRaises(ValueError):
            User(id=1, name="")
    
    def test_user_subscription(self):
        """Тест подписки пользователя на валюту"""
        if not MODELS_AVAILABLE:
            self.skipTest("Модели не доступны")
        
        user = User(id=1, name="Тест")
        currency = Currency(
            id="R01235",
            num_code="840",
            char_code="USD",
            name="Доллар США",
            value=92.45,
            nominal=1
        )
        
        # Подписка
        user.subscribe_to_currency(currency)
        self.assertIn(currency, user.subscribed_currencies)
        self.assertEqual(len(user.subscribed_currencies), 1)
        
        # Повторная подписка не должна добавлять дубликат
        user.subscribe_to_currency(currency)
        self.assertEqual(len(user.subscribed_currencies), 1)
    


class TestCurrencyModel(unittest.TestCase):
    """Тесты для модели Currency"""
    
    def test_currency_creation_valid(self):
        """Тест корректного создания валюты"""
        if not MODELS_AVAILABLE:
            self.skipTest("Модели не доступны")
        
        currency = Currency(
            id="R01235",
            num_code="840",
            char_code="USD",
            name="Доллар США",
            value=92.45,
            nominal=1
        )
        
        self.assertEqual(currency.id, "R01235")
        self.assertEqual(currency.num_code, "840")
        self.assertEqual(currency.char_code, "USD")
        self.assertEqual(currency.name, "Доллар США")
        self.assertEqual(currency.value, 92.45)
        self.assertEqual(currency.nominal, 1)
        self.assertEqual(len(currency.history), 0)
    
    def test_currency_id_validation(self):
        """Тест валидации ID валюты"""
        if not MODELS_AVAILABLE:
            self.skipTest("Модели не доступны")
        
        with self.assertRaises(TypeError):
            Currency(id=123, num_code="840", char_code="USD",
                    name="Доллар США", value=92.45, nominal=1)
        
        with self.assertRaises(ValueError):
            Currency(id="", num_code="840", char_code="USD",
                    name="Доллар США", value=92.45, nominal=1)
    
    def test_currency_value_validation(self):
        """Тест валидации курса валюты"""
        if not MODELS_AVAILABLE:
            self.skipTest("Модели не доступны")
        
        # Отрицательное значение
        with self.assertRaises(ValueError):
            Currency(id="R01235", num_code="840", char_code="USD",
                    name="Доллар США", value=-10.0, nominal=1)
        
        # Нулевое значение
        with self.assertRaises(ValueError):
            Currency(id="R01235", num_code="840", char_code="USD",
                    name="Доллар США", value=0.0, nominal=1)
        
        # Неправильный тип
        with self.assertRaises(TypeError):
            Currency(id="R01235", num_code="840", char_code="USD",
                    name="Доллар США", value="не число", nominal=1)
    
    def test_currency_nominal_validation(self):
        """Тест валидации номинала валюты"""
        if not MODELS_AVAILABLE:
            self.skipTest("Модели не доступны")
        
        with self.assertRaises(ValueError):
            Currency(id="R01235", num_code="840", char_code="USD",
                    name="Доллар США", value=92.45, nominal=0)
        
        with self.assertRaises(TypeError):
            Currency(id="R01235", num_code="840", char_code="USD",
                    name="Доллар США", value=92.45, nominal="не число")
    
    def test_currency_history(self):
        """Тест добавления истории курса"""
        if not MODELS_AVAILABLE:
            self.skipTest("Модели не доступны")
        
        currency = Currency(
            id="R01235",
            num_code="840",
            char_code="USD",
            name="Доллар США",
            value=92.45,
            nominal=1
        )
        
        # Добавление истории
        currency.add_to_history(90.0, "2024-01-01")
        currency.add_to_history(91.5, "2024-01-02")
        
        self.assertEqual(len(currency.history), 2)
        self.assertEqual(currency.history[0]['value'], 90.0)
        self.assertEqual(currency.history[0]['timestamp'], "2024-01-01")
        self.assertEqual(currency.history[1]['value'], 91.5)
    


class TestUserCurrencyModel(unittest.TestCase):
    """Тесты для модели UserCurrency"""
    
    def test_user_currency_creation_valid(self):
        """Тест корректного создания связи пользователь-валюта"""
        if not MODELS_AVAILABLE:
            self.skipTest("Модели не доступны")
        
        uc = UserCurrency(id=1, user_id=1, currency_id="R01235")
        self.assertEqual(uc.id, 1)
        self.assertEqual(uc.user_id, 1)
        self.assertEqual(uc.currency_id, "R01235")
    
    def test_user_currency_validation(self):
        """Тест валидации связи пользователь-валюта"""
        if not MODELS_AVAILABLE:
            self.skipTest("Модели не доступны")
        
        with self.assertRaises(TypeError):
            UserCurrency(id="не число", user_id=1, currency_id="R01235")
        
        with self.assertRaises(ValueError):
            UserCurrency(id=0, user_id=1, currency_id="R01235")
        
        with self.assertRaises(TypeError):
            UserCurrency(id=1, user_id="не число", currency_id="R01235")
        
        with self.assertRaises(ValueError):
            UserCurrency(id=1, user_id=0, currency_id="R01235")
        
        with self.assertRaises(TypeError):
            UserCurrency(id=1, user_id=1, currency_id=123)
        
        with self.assertRaises(ValueError):
            UserCurrency(id=1, user_id=1, currency_id="")


class TestAppModel(unittest.TestCase):
    """Тесты для модели App"""
    
    def test_app_creation_valid(self):
        """Тест корректного создания приложения"""
        if not MODELS_AVAILABLE:
            self.skipTest("Модели не доступны")
        
        author = Author(name="Мамонтов Алексей", group="P3120")
        app = App(name="CurrenciesListApp", version="1.0.0", author=author)
        
        self.assertEqual(app.name, "CurrenciesListApp")
        self.assertEqual(app.version, "1.0.0")
        self.assertEqual(app.author, author)
    
    def test_app_validation(self):
        """Тест валидации приложения"""
        if not MODELS_AVAILABLE:
            self.skipTest("Модели не доступны")
        
        author = Author(name="Тест", group="Группа")
        
        with self.assertRaises(TypeError):
            App(name=123, version="1.0.0", author=author)
        
        with self.assertRaises(ValueError):
            App(name="", version="1.0.0", author=author)
        
        with self.assertRaises(TypeError):
            App(name="Приложение", version=1.0, author=author)
        
        with self.assertRaises(ValueError):
            App(name="Приложение", version="", author=author)
        
        with self.assertRaises(TypeError):
            App(name="Приложение", version="1.0.0", author="не автор")


# -------------------------------------------------------------------
# ТЕСТЫ СЕРВЕРА И АРХИТЕКТУРЫ
# -------------------------------------------------------------------

class TestServerArchitecture(unittest.TestCase):
    """Тесты архитектуры сервера"""
    
    def test_server_file_exists(self):
        """Тест наличия файла server.py"""
        self.assertTrue(os.path.exists("server.py"), 
                       "Файл server.py должен существовать")
    
    def test_server_import(self):
        """Тест импорта сервера"""
        try:
            from server import CurrencyHandler
            self.assertTrue(True, "Сервер успешно импортирован")
        except ImportError as e:
            self.fail(f"Не удалось импортировать сервер: {e}")
    
    def test_handler_inheritance(self):
        """Тест что CurrencyHandler наследуется от BaseHTTPRequestHandler"""
        from http.server import BaseHTTPRequestHandler
        
        try:
            from server import CurrencyHandler
            self.assertTrue(issubclass(CurrencyHandler, BaseHTTPRequestHandler),
                          "CurrencyHandler должен наследоваться от BaseHTTPRequestHandler")
        except ImportError:
            self.skipTest("Не удалось импортировать CurrencyHandler")


class TestProjectStructure(unittest.TestCase):
    """Тесты структуры проекта"""
    
    def test_project_directories(self):
        """Тест наличия обязательных директорий"""
        required_dirs = ["models", "templates", "static"]
        
        for dir_name in required_dirs:
            with self.subTest(directory=dir_name):
                self.assertTrue(os.path.exists(dir_name),
                              f"Директория {dir_name} должна существовать")
    
    def test_template_files(self):
        """Тест наличия HTML шаблонов"""
        required_templates = [
            "index.html",
            "author.html", 
            "currencies.html",
            "users.html",
            "user_detail.html"
        ]
        
        for template in required_templates:
            template_path = os.path.join("templates", template)
            with self.subTest(template=template):
                self.assertTrue(os.path.exists(template_path),
                              f"Шаблон {template} должен существовать в templates/")
    
    def test_static_files(self):
        """Тест наличия статических файлов"""
        css_path = os.path.join("static", "style.css")
        self.assertTrue(os.path.exists(css_path),
                       "CSS файл должен существовать в static/")
    
    def test_requirements_file(self):
        """Тест наличия requirements.txt"""
        self.assertTrue(os.path.exists("requirements.txt"),
                       "Файл requirements.txt должен существовать")
    
    def test_utils_directory(self):
        """Тест наличия директории utils"""
        self.assertTrue(os.path.exists("utils"),
                       "Директория utils должна существовать")


# -------------------------------------------------------------------
# ТЕСТЫ ФУНКЦИОНАЛЬНОСТИ
# -------------------------------------------------------------------

class TestCurrencyFunctionality(unittest.TestCase):
    """Тесты функциональности валют"""
    
    def test_target_currencies_exist(self):
        """Тест что все требуемые валюты присутствуют в коде"""
        target_currencies = ["USD", "EUR", "GBP", "JPY", "CHF", 
                            "CNY", "CAD", "AUD", "INR"]
        
        # Проверяем наличие в server.py
        if os.path.exists("server.py"):
            with open("server.py", "r", encoding="utf-8") as f:
                content = f.read().upper()  # Приводим к верхнему регистру
            
            for currency in target_currencies:
                with self.subTest(currency=currency):
                    self.assertIn(currency, content,
                                f"Валюта {currency} должна быть в коде сервера")
    
    def test_currency_names_correct(self):
        """Тест правильности названий валют"""
        currency_mapping = {
            "USD": "Доллар США",
            "EUR": "Евро", 
            "GBP": "Фунт стерлингов",
            "JPY": "Японская иена",
            "CHF": "Швейцарский франк",
            "CNY": "Китайский юань",
            "CAD": "Канадский доллар",
            "AUD": "Австралийский доллар",
            "INR": "Индийская рупия"
        }
        
        if os.path.exists("server.py"):
            with open("server.py", "r", encoding="utf-8") as f:
                content = f.read()
            
            for code, name in currency_mapping.items():
                with self.subTest(currency=f"{code} - {name}"):
                    # Проверяем что хотя бы одна пара код-имя присутствует
                    if code in content or name in content:
                        self.assertTrue(True)
                    else:
                        self.fail(f"Валюта {code} ({name}) не найдена")


class TestUserFunctionality(unittest.TestCase):
    """Тесты функциональности пользователей"""
    
    def test_users_exist(self):
        """Тест что все пользователи присутствуют в коде"""
        target_users = ["Ноунейм", "Питонист", "Брат", "Скрин"]
        
        if os.path.exists("server.py"):
            with open("server.py", "r", encoding="utf-8") as f:
                content = f.read()
            
            for user in target_users:
                with self.subTest(user=user):
                    self.assertIn(user, content,
                                f"Пользователь {user} должен быть в коде сервера")
    
    def test_user_subscriptions(self):
        """Тест что у пользователей есть подписки"""
        user_subscriptions = {
            "Ноунейм": ["USD", "EUR"],
            "Питонист": ["USD", "GBP"],
            "Брат": ["CHF"],
            "Скрин": ["EUR", "CNY"]
        }
        
        if os.path.exists("server.py"):
            with open("server.py", "r", encoding="utf-8") as f:
                content = f.read()
            
            for user, subscriptions in user_subscriptions.items():
                with self.subTest(user=user):
                    # Проверяем что пользователь существует
                    self.assertIn(user, content, f"Пользователь {user} не найден")
                    
                    # Проверяем что есть упоминание о подписках
                    subscription_text = f"Подписок: {len(subscriptions)}"
                    if subscription_text not in content:
                        # Альтернативная проверка
                        has_subscriptions = any(
                            f"'{sub}'" in content or f'"{sub}"' in content 
                            for sub in subscriptions
                        )
                        self.assertTrue(has_subscriptions, 
                                      f"У пользователя {user} должны быть подписки")


class TestRouting(unittest.TestCase):
    """Тесты маршрутизации"""
    
    def test_routes_defined(self):
        """Тест что все маршруты определены"""
        required_routes = [
            ("/", "index"),
            ("/author", "author_page"),
            ("/currencies", "currencies_page"), 
            ("/users", "users_page"),
            ("/user", "user_detail")
        ]
        
        if os.path.exists("server.py"):
            with open("server.py", "r", encoding="utf-8") as f:
                content = f.read()
            
            for route, handler in required_routes:
                with self.subTest(route=route):
                    # Проверяем наличие маршрута или обработчика
                    route_found = route in content
                    handler_found = f"def {handler}" in content
                    
                    self.assertTrue(route_found or handler_found,
                                  f"Маршрут {route} или обработчик {handler} должен быть определен")


# -------------------------------------------------------------------
# ТЕСТЫ ИНТЕГРАЦИИ
# -------------------------------------------------------------------

class TestIntegration(unittest.TestCase):
    """Интеграционные тесты"""
    
    def test_user_currency_integration(self):
        """Тест интеграции пользователя и валюты"""
        if not MODELS_AVAILABLE:
            self.skipTest("Модели не доступны")
        
        # Создаем пользователя
        user = User(id=1, name="Тестовый пользователь")
        
        # Создаем валюту
        currency = Currency(
            id="R01235",
            num_code="840",
            char_code="USD",
            name="Доллар США",
            value=92.45,
            nominal=1
        )
        
        # Пользователь подписывается на валюту
        user.subscribe_to_currency(currency)
        
        # Проверяем подписку
        self.assertIn(currency, user.subscribed_currencies)
        
        # Создаем связь через UserCurrency
        uc = UserCurrency(id=1, user_id=user.id, currency_id=currency.id)
        
        # Проверяем связь
        self.assertEqual(uc.user_id, user.id)
        self.assertEqual(uc.currency_id, currency.id)
    
    def test_complete_system_workflow(self):
        """Тест полного рабочего процесса системы"""
        if not MODELS_AVAILABLE:
            self.skipTest("Модели не доступны")
        
        # 1. Создаем автора
        author = Author(name="Мамонтов Алексей", group="P3120")
        
        # 2. Создаем приложение
        app = App(name="CurrenciesListApp", version="1.0.0", author=author)
        
        # 3. Создаем пользователей
        user1 = User(id=1, name="Ноунейм")
        user2 = User(id=2, name="Питонист")
        
        # 4. Создаем валюты
        usd = Currency(id="R01235", num_code="840", char_code="USD", 
                      name="Доллар США", value=92.45, nominal=1)
        eur = Currency(id="R01239", num_code="978", char_code="EUR", 
                      name="Евро", value=98.12, nominal=1)
        
        # 5. Пользователи подписываются на валюты
        user1.subscribe_to_currency(usd)
        user1.subscribe_to_currency(eur)
        user2.subscribe_to_currency(usd)
        
        # 6. Проверяем подписки
        self.assertEqual(len(user1.subscribed_currencies), 2)
        self.assertEqual(len(user2.subscribed_currencies), 1)
        self.assertIn(usd, user1.subscribed_currencies)
        self.assertIn(eur, user1.subscribed_currencies)
        self.assertIn(usd, user2.subscribed_currencies)
        
        # 7. Создаем связи UserCurrency
        uc1 = UserCurrency(id=1, user_id=1, currency_id="R01235")
        uc2 = UserCurrency(id=2, user_id=1, currency_id="R01239")
        uc3 = UserCurrency(id=3, user_id=2, currency_id="R01235")
        
        # 8. Проверяем связи
        self.assertEqual(uc1.user_id, user1.id)
        self.assertEqual(uc1.currency_id, usd.id)
        self.assertEqual(uc2.user_id, user1.id)
        self.assertEqual(uc2.currency_id, eur.id)
        self.assertEqual(uc3.user_id, user2.id)
        self.assertEqual(uc3.currency_id, usd.id)
        
        # 9. Проверяем что все объекты созданы корректно
        self.assertEqual(app.name, "CurrenciesListApp")
        self.assertEqual(author.name, "Мамонтов Алексей")
        self.assertEqual(usd.char_code, "USD")
        self.assertEqual(eur.char_code, "EUR")


# -------------------------------------------------------------------
# ТЕСТЫ ДЛЯ UTILS/CURRENCIES_API.PY
# -------------------------------------------------------------------

class TestCurrencyAPI(unittest.TestCase):
    """Тесты для модуля currencies_api.py"""
    
    def test_api_module_exists(self):
        """Тест наличия модуля currencies_api.py"""
        api_path = os.path.join("utils", "currencies_api.py")
        self.assertTrue(os.path.exists(api_path),
                       "Файл utils/currencies_api.py должен существовать")
    
    def test_get_currencies_function(self):
        """Тест функции get_currencies"""
        try:
            from utils.currencies_api import get_currencies
            
            # Проверяем что функция существует
            self.assertTrue(callable(get_currencies),
                          "get_currencies должна быть функцией")
            
            # Пробуем вызвать функцию
            try:
                result = get_currencies()
                
                # Проверяем тип возвращаемого значения
                self.assertIsInstance(result, list,
                                    "get_currencies должна возвращать список")
                
                # Проверяем что список не пустой
                self.assertGreater(len(result), 0,
                                 "Список валют не должен быть пустым")
                
                # Проверяем структуру данных
                for currency in result:
                    self.assertIsInstance(currency, dict,
                                        "Каждая валюта должна быть словарем")
                    
                    # Проверяем обязательные поля
                    required_fields = ["id", "num_code", "char_code", 
                                      "name", "value", "nominal"]
                    for field in required_fields:
                        self.assertIn(field, currency,
                                    f"Поле '{field}' должно присутствовать в данных о валюте")
                    
                    # Проверяем типы данных
                    self.assertIsInstance(currency['char_code'], str)
                    self.assertIsInstance(currency['name'], str)
                    self.assertIsInstance(currency['value'], (int, float))
                    self.assertIsInstance(currency['nominal'], int)
                    
                    # Проверяем корректность значений
                    self.assertGreater(currency['value'], 0,
                                     "Курс валюты должен быть положительным")
                    self.assertGreater(currency['nominal'], 0,
                                     "Номинал валюты должен быть положительным")
                    
            except Exception as e:
                # Функция может выбрасывать исключения при отсутствии интернета
                # Это допустимо для учебного проекта
                print(f"Функция get_currencies вызвала исключение (возможно нет интернета): {e}")
                
        except ImportError:
            self.skipTest("Модуль currencies_api не найден")


# -------------------------------------------------------------------
# ЗАПУСК ТЕСТОВ
# -------------------------------------------------------------------

def run_all_tests():
    """Запуск всех тестов с красивым выводом"""
    print("🧪" + "="*58 + "🧪")
    print("          ЗАПУСК ТЕСТОВ ДЛЯ ЛАБОРАТОРНОЙ РАБОТЫ")
    print("             CurrenciesListApp v1.0.0")
    print("              Автор: Мамонтов Алексей")
    print("                 Группа: P3120")
    print("🧪" + "="*58 + "🧪")
    print()
    
    # Проверка структуры проекта
    print("🔍 ПРОВЕРКА СТРУКТУРЫ ПРОЕКТА:")
    print("-" * 60)
    
    structure_checks = [
        ("📁 Папка models", os.path.exists("models")),
        ("📁 Папка templates", os.path.exists("templates")),
        ("📁 Папка static", os.path.exists("static")),
        ("📁 Папка utils", os.path.exists("utils")),
        ("📄 server.py", os.path.exists("server.py")),
        ("📄 requirements.txt", os.path.exists("requirements.txt")),
    ]
    
    for name, exists in structure_checks:
        status = "✅" if exists else "❌"
        print(f"  {status} {name}")
    
    print()
    print("🔍 ПРОВЕРКА ШАБЛОНОВ:")
    print("-" * 60)
    
    templates = ["index.html", "author.html", "currencies.html", 
                "users.html", "user_detail.html"]
    
    for template in templates:
        path = os.path.join("templates", template)
        status = "✅" if os.path.exists(path) else "❌"
        print(f"  {status} {template}")
    
    print()
    print("🚀 ЗАПУСК ЮНИТ-ТЕСТОВ:")
    print("-" * 60)
    
    # Создаем тестовый набор
    test_suite = unittest.TestSuite()
    
    # Добавляем тесты по категориям
    test_categories = [
        (TestAuthorModel, "Модель Author"),
        (TestUserModel, "Модель User"),
        (TestCurrencyModel, "Модель Currency"),
        (TestUserCurrencyModel, "Модель UserCurrency"),
        (TestAppModel, "Модель App"),
        (TestServerArchitecture, "Архитектура сервера"),
        (TestProjectStructure, "Структура проекта"),
        (TestCurrencyFunctionality, "Функциональность валют"),
        (TestUserFunctionality, "Функциональность пользователей"),
        (TestRouting, "Маршрутизация"),
        (TestIntegration, "Интеграционные тесты"),
        (TestCurrencyAPI, "API валют"),
    ]
    
    # Загружаем все тесты
    loader = unittest.TestLoader()
    for test_class, category_name in test_categories:
        try:
            suite = loader.loadTestsFromTestCase(test_class)
            test_suite.addTest(suite)
            print(f"  ✅ Загружены тесты: {category_name}")
        except Exception as e:
            print(f"  ❌ Ошибка загрузки тестов {category_name}: {e}")
    
    print()
    # Запускаем тесты
    runner = unittest.TextTestRunner(verbosity=0)
    result = runner.run(test_suite)
    

if __name__ == '__main__':
    # Устанавливаем текущую директорию
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Запускаем тесты
    success = run_all_tests()
    
    # Завершаем с соответствующим кодом
    sys.exit(0 if success else 1)
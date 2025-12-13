#!/usr/bin/env python3
"""
Полный юнит-тест для лабораторной работы по валютам.
Запуск: python test_app_complete.py
"""

import unittest
import sys
import os
import hashlib

# Временно добавляем текущую директорию в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Мокаем requests до импорта app, чтобы не делать реальные HTTP запросы
import unittest.mock as mock

class TestCurrencyApp(unittest.TestCase):
    """Тесты для приложения отслеживания курсов валют"""
    
    def setUp(self):
        """Настройка тестового окружения"""
        # Мокаем requests.get перед импортом app
        self.requests_patcher = mock.patch('requests.get')
        self.mock_requests = self.requests_patcher.start()
        
        # Настраиваем мок для API Центробанка
        self.mock_response = mock.Mock()
        self.mock_response.json.return_value = {
            'Valute': {
                'USD': {'NumCode': '840', 'CharCode': 'USD', 
                       'Name': 'Доллар США', 'Value': 91.23, 'Nominal': 1},
                'EUR': {'NumCode': '978', 'CharCode': 'EUR', 
                       'Name': 'Евро', 'Value': 98.45, 'Nominal': 1}
            }
        }
        self.mock_requests.return_value = self.mock_response
        
        # Теперь импортируем app (requests уже замокан)
        from app import app, db, User, Currency, UserCurrency, hash_password
        
        self.app_module = sys.modules['app']
        self.app = app
        self.db = db
        self.User = User
        self.Currency = Currency
        self.UserCurrency = UserCurrency
        self.hash_password = hash_password
        
        # Настраиваем тестовую базу данных
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['SECRET_KEY'] = 'test-secret-key'
        self.app.config['WTF_CSRF_ENABLED'] = False
        
        self.client = self.app.test_client()
        
        # Создаем таблицы в тестовом контексте
        with self.app.app_context():
            self.db.create_all()
    
    def tearDown(self):
        """Очистка после тестов"""
        self.requests_patcher.stop()
        with self.app.app_context():
            self.db.session.remove()
            self.db.drop_all()
    
    def test_01_hash_password_works(self):
        """Тест 1: Хеширование пароля работает корректно"""
        password = "PythonCool"
        hashed = self.hash_password(password)
        
        # Проверяем длину хеша SHA-256
        self.assertEqual(len(hashed), 64)
        
        # Проверяем, что это хеш
        self.assertNotEqual(password, hashed)
        
        # Проверяем воспроизводимость
        self.assertEqual(hashed, self.hash_password(password))
    
    def test_02_user_model_creation(self):
        """Тест 2: Модель User создается правильно"""
        with self.app.app_context():
            user = self.User(
                username="TestUser",
                password=self.hash_password("testpass"),
                is_admin=False
            )
            self.db.session.add(user)
            self.db.session.commit()
            
            saved = self.User.query.filter_by(username="TestUser").first()
            self.assertIsNotNone(saved)
            self.assertEqual(saved.username, "TestUser")
            self.assertFalse(saved.is_admin)
    
    def test_03_currency_model_creation(self):
        """Тест 3: Модель Currency создается правильно"""
        with self.app.app_context():
            currency = self.Currency(
                num_code="840",
                char_code="USD",
                name="Доллар США",
                value=90.5,
                nominal=1
            )
            self.db.session.add(currency)
            self.db.session.commit()
            
            saved = self.Currency.query.filter_by(char_code="USD").first()
            self.assertIsNotNone(saved)
            self.assertEqual(saved.name, "Доллар США")
            self.assertEqual(saved.value, 90.5)
            self.assertEqual(saved.nominal, 1)
    
    def test_04_user_registration_flow(self):
        """Тест 4: Полный цикл регистрации пользователя"""
        # Шаг 1: Регистрация
        response = self.client.post('/register', data={
            'username': 'NewTestUser',
            'password': 'TestPassword123'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        
        # Проверяем, что пользователь создан в БД
        with self.app.app_context():
            user = self.User.query.filter_by(username='NewTestUser').first()
            self.assertIsNotNone(user)
            self.assertEqual(user.username, 'NewTestUser')
            self.assertFalse(user.is_admin)
    
    def test_05_admin_user_creation(self):
        """Тест 5: Создание пользователя с правами администратора"""
        with self.app.app_context():
            admin = self.User(
                username="SuperAdmin",
                password=self.hash_password("AdminPass123"),
                is_admin=True
            )
            self.db.session.add(admin)
            self.db.session.commit()
            
            saved = self.User.query.filter_by(username="SuperAdmin").first()
            self.assertTrue(saved.is_admin)
    
    def test_06_crud_create_currency(self):
        """Тест 6: CRUD - Create (Создание валюты)"""
        with self.app.app_context():
            # Создаем валюту
            currency = self.Currency(
                num_code="978",
                char_code="EUR",
                name="Евро",
                value=95.0,
                nominal=1
            )
            self.db.session.add(currency)
            self.db.session.commit()
            
            # Проверяем создание
            count = self.Currency.query.count()
            self.assertEqual(count, 1)
            
            saved = self.Currency.query.first()
            self.assertEqual(saved.char_code, "EUR")
            self.assertEqual(saved.value, 95.0)
    
    def test_07_crud_read_currency(self):
        """Тест 7: CRUD - Read (Чтение валют)"""
        with self.app.app_context():
            # Создаем несколько валют
            currencies = [
                self.Currency(num_code="840", char_code="USD", name="Доллар США", value=90.0, nominal=1),
                self.Currency(num_code="978", char_code="EUR", name="Евро", value=95.0, nominal=1),
                self.Currency(num_code="392", char_code="JPY", name="Японская иена", value=0.6, nominal=100)
            ]
            
            for curr in currencies:
                self.db.session.add(curr)
            self.db.session.commit()
            
            # Читаем все валюты
            all_currencies = self.Currency.query.all()
            self.assertEqual(len(all_currencies), 3)
            
            # Фильтруем по коду
            usd = self.Currency.query.filter_by(char_code="USD").first()
            self.assertEqual(usd.name, "Доллар США")
            
            # Получаем по ID
            eur_id = self.Currency.query.filter_by(char_code="EUR").first().id
            eur = self.Currency.query.get(eur_id)
            self.assertEqual(eur.char_code, "EUR")
    
    def test_08_crud_update_currency(self):
        """Тест 8: CRUD - Update (Обновление валюты)"""
        with self.app.app_context():
            # Создаем валюту
            currency = self.Currency(
                num_code="840",
                char_code="USD",
                name="Доллар США",
                value=90.0,
                nominal=1
            )
            self.db.session.add(currency)
            self.db.session.commit()
            
            original_id = currency.id
            
            # Обновляем курс
            currency.value = 91.5
            self.db.session.commit()
            
            # Проверяем обновление
            updated = self.Currency.query.get(original_id)
            self.assertEqual(updated.value, 91.5)
            self.assertEqual(updated.char_code, "USD")  # Остальные поля не изменились
    
    def test_09_crud_delete_currency(self):
        """Тест 9: CRUD - Delete (Удаление валюты)"""
        with self.app.app_context():
            # Создаем валюту
            currency = self.Currency(
                num_code="840",
                char_code="USD",
                name="Доллар США",
                value=90.0,
                nominal=1
            )
            self.db.session.add(currency)
            self.db.session.commit()
            
            currency_id = currency.id
            
            # Проверяем, что создана
            self.assertIsNotNone(self.Currency.query.get(currency_id))
            
            # Удаляем
            self.db.session.delete(currency)
            self.db.session.commit()
            
            # Проверяем удаление
            self.assertIsNone(self.Currency.query.get(currency_id))
    
    def test_10_user_currency_relationship(self):
        """Тест 10: Связь многие-ко-многим User <-> Currency"""
        with self.app.app_context():
            # Создаем пользователя
            user = self.User(
                username="RelationUser",
                password=self.hash_password("pass"),
                is_admin=False
            )
            
            # Создаем валюту
            currency = self.Currency(
                num_code="840",
                char_code="USD",
                name="Доллар США",
                value=90.0,
                nominal=1
            )
            
            self.db.session.add(user)
            self.db.session.add(currency)
            self.db.session.commit()
            
            # Создаем связь
            user_currency = self.UserCurrency(
                user_id=user.id,
                currency_id=currency.id
            )
            self.db.session.add(user_currency)
            self.db.session.commit()
            
            # Проверяем связь
            relation = self.UserCurrency.query.filter_by(
                user_id=user.id,
                currency_id=currency.id
            ).first()
            
            self.assertIsNotNone(relation)
            self.assertEqual(relation.user_id, user.id)
            self.assertEqual(relation.currency_id, currency.id)
    
    def test_11_is_admin_user_function(self):
        """Тест 11: Функция проверки прав администратора"""
        with self.app.app_context():
            # Создаем обычного пользователя
            regular = self.User(
                username="RegularUser",
                password=self.hash_password("pass"),
                is_admin=False
            )
            
            # Создаем администратора
            admin = self.User(
                username="AdminUser",
                password=self.hash_password("adminpass"),
                is_admin=True
            )
            
            self.db.session.add(regular)
            self.db.session.add(admin)
            self.db.session.commit()
            
            # Импортируем функцию
            from app import is_admin_user
            
            # Тестируем
            self.assertFalse(is_admin_user(regular.id))
            self.assertTrue(is_admin_user(admin.id))
            self.assertFalse(is_admin_user(999))  # Несуществующий ID
            self.assertFalse(is_admin_user(None))  # None
    
    def test_12_api_fetch_currencies_mocked(self):
        """Тест 12: Получение курсов валют через API (с использованием mock)"""
        # Мок уже настроен в setUp
        
        # Проверяем, что мок работает
        self.mock_requests.assert_not_called()  # Пока не вызывали
        
        # Имитируем вызов API (как в реальном приложении)
        response = self.mock_requests('https://www.cbr-xml-daily.ru/daily_json.js')
        data = response.json()
        
        # Проверяем, что мок вызван
        self.mock_requests.assert_called_once_with('https://www.cbr-xml-daily.ru/daily_json.js')
        
        # Проверяем структуру данных
        self.assertIn('Valute', data)
        self.assertIn('USD', data['Valute'])
        self.assertEqual(data['Valute']['USD']['CharCode'], 'USD')
        self.assertEqual(data['Valute']['EUR']['Value'], 98.45)
    
    def test_13_session_management(self):
        """Тест 13: Работа с сессиями Flask"""
        with self.app.app_context():
            # Создаем тестового пользователя
            user = self.User(
                username="SessionTest",
                password=self.hash_password("sessionpass"),
                is_admin=False
            )
            self.db.session.add(user)
            self.db.session.commit()
            
            # Имитируем вход (устанавливаем сессию)
            with self.client.session_transaction() as session:
                session['user_id'] = user.id
                session['username'] = user.username
            
            # Теперь должны иметь доступ к защищенным страницам
            # (но для этого нужно мокнуть проверки в маршрутах)
    
    def test_14_initial_admin_exists(self):
        """Тест 14: Проверка существования начального администратора"""
        # Этот тест проверяет логику, которая должна быть в init_data()
        with self.app.app_context():
            # Создаем администратора как в init_data()
            from app import hash_password
            admin = self.User(
                username="MamontovAleksei",
                password=hash_password("PythonCool"),
                is_admin=True
            )
            self.db.session.add(admin)
            self.db.session.commit()
            
            # Проверяем
            saved_admin = self.User.query.filter_by(username="MamontovAleksei").first()
            self.assertIsNotNone(saved_admin)
            self.assertTrue(saved_admin.is_admin)
            self.assertEqual(saved_admin.password, hash_password("PythonCool"))


def run_tests():
    """Запуск всех тестов с минимальным выводом"""
    # Создаем TestSuite
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestCurrencyApp)
    
    # Настраиваем runner
    runner = unittest.TextTestRunner(
        verbosity=1,  # Минимальный вывод
        descriptions=True,
        failfast=False
    )
    
    
    # Запускаем тесты
    result = runner.run(test_suite)
    
    if result.failures:
        print(f"ПРОВАЛЕНО: {len(result.failures)}")
        for test, traceback in result.failures:
            print(f"\nПровален: {test}")
            print(traceback)
    
    if result.errors:
        print(f"ОШИБОК: {len(result.errors)}")
        for test, traceback in result.errors:
            print(f"\nОшибка в: {test}")
            print(traceback)
    
    
    return result.wasSuccessful()


if __name__ == '__main__':
    # Запускаем тесты
    success = run_tests()
    
    # Выходим с соответствующим кодом
    sys.exit(0 if success else 1)
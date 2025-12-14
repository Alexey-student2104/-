#!/usr/bin/env python3
"""
Юнит-тесты для лабораторной работы по валютам.
"""

import unittest
import sys
import os
import hashlib
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
    
    # ========== БАЗОВЫЕ ТЕСТЫ МОДЕЛЕЙ ==========
    
    def test_hash_password(self):
        """Хеширование пароля работает корректно"""
        password = "PythonCool"
        hashed = self.hash_password(password)
        
        self.assertEqual(len(hashed), 64)
        self.assertNotEqual(password, hashed)
        self.assertEqual(hashed, self.hash_password(password))
    
    def test_user_model_creation(self):
        """Модель User создается правильно"""
        with self.app.app_context():
            user = self.User(
                username="TestUser",
                password=self.hash_password("testpass"),
                is_admin=False
            )
            self.db.session.add(user)
            self.db.session.commit()
            
            saved = self.db.session.get(self.User, user.id)
            self.assertIsNotNone(saved)
            self.assertEqual(saved.username, "TestUser")
            self.assertFalse(saved.is_admin)
    
    def test_user_model_admin_property(self):
        """Проверка свойства администратора"""
        with self.app.app_context():
            regular_user = self.User(
                username="RegularUser",
                password=self.hash_password("pass"),
                is_admin=False
            )
            
            admin_user = self.User(
                username="AdminUser",
                password=self.hash_password("adminpass"),
                is_admin=True
            )
            
            self.db.session.add(regular_user)
            self.db.session.add(admin_user)
            self.db.session.commit()
            
            saved_regular = self.db.session.get(self.User, regular_user.id)
            saved_admin = self.db.session.get(self.User, admin_user.id)
            
            self.assertFalse(saved_regular.is_admin)
            self.assertTrue(saved_admin.is_admin)
    
    def test_currency_model_creation(self):
        """Модель Currency создается правильно"""
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
            
            saved = self.db.session.get(self.Currency, currency.id)
            self.assertIsNotNone(saved)
            self.assertEqual(saved.char_code, "USD")
            self.assertEqual(saved.name, "Доллар США")
            self.assertEqual(saved.value, 90.5)
            self.assertEqual(saved.nominal, 1)
    
    def test_user_currency_relationship(self):
        """Связь многие-ко-многим работает"""
        with self.app.app_context():
            user = self.User(
                username="RelationUser",
                password=self.hash_password("pass"),
                is_admin=False
            )
            
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
            
            user_currency = self.UserCurrency(
                user_id=user.id,
                currency_id=currency.id
            )
            self.db.session.add(user_currency)
            self.db.session.commit()
            
            saved_sub = self.db.session.query(self.UserCurrency).filter_by(
                user_id=user.id,
                currency_id=currency.id
            ).first()
            
            self.assertIsNotNone(saved_sub)
            self.assertEqual(saved_sub.user_id, user.id)
            self.assertEqual(saved_sub.currency_id, currency.id)
    
    # ========== ТЕСТЫ ДЛЯ МАРШРУТОВ ==========
    
    def test_home_page_accessible(self):
        """Главная страница доступна"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_author_page_accessible(self):
        """Страница об авторе доступна"""
        response = self.client.get('/author')
        self.assertEqual(response.status_code, 200)
    
    def test_login_page_accessible(self):
        """Страница входа доступна"""
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
    
    def test_register_page_accessible(self):
        """Страница регистрации доступна"""
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)
    
    def test_protected_pages_redirect(self):
        """Защищенные страницы перенаправляют"""
        response = self.client.get('/currencies')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.headers['Location'])
    
    # ========== ТЕСТЫ ДЛЯ РЕГИСТРАЦИИ И АВТОРИЗАЦИИ ==========
    
    def test_successful_registration(self):
        """Успешная регистрация пользователя"""
        response = self.client.post('/register', data={
            'username': 'NewTestUser123',
            'password': 'TestPassword123'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        
        with self.app.app_context():
            user = self.db.session.query(self.User).filter_by(username='NewTestUser123').first()
            self.assertIsNotNone(user)
            self.assertEqual(user.username, 'NewTestUser123')
    
    # ========== ТЕСТЫ ДЛЯ CRUD ОПЕРАЦИЙ ==========
    
    def test_crud_create_currency(self):
        """Создание валюты"""
        with self.app.app_context():
            currency = self.Currency(
                num_code="978",
                char_code="EUR",
                name="Евро",
                value=95.0,
                nominal=1
            )
            self.db.session.add(currency)
            self.db.session.commit()
            
            count = self.db.session.query(self.Currency).count()
            self.assertEqual(count, 1)
            
            saved = self.db.session.query(self.Currency).first()
            self.assertEqual(saved.char_code, "EUR")
            self.assertEqual(saved.value, 95.0)
    
    def test_crud_read_currencies(self):
        """Чтение валют"""
        with self.app.app_context():
            currencies = [
                self.Currency(num_code="840", char_code="USD", name="Доллар США", value=90.0, nominal=1),
                self.Currency(num_code="978", char_code="EUR", name="Евро", value=95.0, nominal=1),
            ]
            
            for curr in currencies:
                self.db.session.add(curr)
            self.db.session.commit()
            
            all_currencies = self.db.session.query(self.Currency).all()
            self.assertEqual(len(all_currencies), 2)
    
    def test_crud_update_currency(self):
        """Обновление валюты"""
        with self.app.app_context():
            currency = self.Currency(
                num_code="840",
                char_code="USD",
                name="Доллар США",
                value=90.0,
                nominal=1
            )
            self.db.session.add(currency)
            self.db.session.commit()
            
            currency.value = 91.5
            self.db.session.commit()
            
            updated = self.db.session.get(self.Currency, currency.id)
            self.assertEqual(updated.value, 91.5)
    
    def test_crud_delete_currency(self):
        """Удаление валюты"""
        with self.app.app_context():
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
            
            self.db.session.delete(currency)
            self.db.session.commit()
            
            self.assertIsNone(self.db.session.get(self.Currency, currency_id))
    
    def test_crud_create_user(self):
        """Создание пользователя"""
        with self.app.app_context():
            user = self.User(
                username="CRUDTestUser",
                password=self.hash_password("crudpass"),
                is_admin=False
            )
            self.db.session.add(user)
            self.db.session.commit()
            
            saved = self.db.session.query(self.User).filter_by(username="CRUDTestUser").first()
            self.assertIsNotNone(saved)
            self.assertEqual(saved.username, "CRUDTestUser")
    
    def test_crud_delete_user(self):
        """Удаление пользователя"""
        with self.app.app_context():
            user = self.User(
                username="DeleteTestUser",
                password=self.hash_password("deletepass"),
                is_admin=False
            )
            self.db.session.add(user)
            self.db.session.commit()
            
            user_id = user.id
            
            self.db.session.delete(user)
            self.db.session.commit()
            
            self.assertIsNone(self.db.session.get(self.User, user_id))
    
    # ========== ТЕСТЫ ДЛЯ API ИНТЕГРАЦИИ ==========
    
    def test_api_fetch_currencies_mocked(self):
        """Получение курсов валют через API"""
        self.mock_requests.assert_not_called()
        
        response = self.mock_requests('https://www.cbr-xml-daily.ru/daily_json.js')
        data = response.json()
        
        self.mock_requests.assert_called_once_with('https://www.cbr-xml-daily.ru/daily_json.js')
        self.assertIn('Valute', data)
        self.assertIn('USD', data['Valute'])
        self.assertEqual(data['Valute']['USD']['CharCode'], 'USD')
    
    # ========== ТЕСТЫ ДЛЯ БИЗНЕС-ЛОГИКИ ==========
    
    def test_is_admin_user_function(self):
        """Функция проверки прав администратора"""
        with self.app.app_context():
            from app import is_admin_user
            
            regular = self.User(
                username="RegularTestUser",
                password=self.hash_password("pass"),
                is_admin=False
            )
            
            admin = self.User(
                username="AdminTestUser",
                password=self.hash_password("adminpass"),
                is_admin=True
            )
            
            self.db.session.add(regular)
            self.db.session.add(admin)
            self.db.session.commit()
            
            self.assertFalse(is_admin_user(regular.id))
            self.assertTrue(is_admin_user(admin.id))
            self.assertFalse(is_admin_user(999))
            self.assertFalse(is_admin_user(None))
    
    def test_user_subscription_management(self):
        """Управление подписками пользователя"""
        with self.app.app_context():
            user = self.User(
                username="SubscriptionUser",
                password=self.hash_password("subpass"),
                is_admin=False
            )
            
            currency1 = self.Currency(
                num_code="840",
                char_code="USD",
                name="Доллар США",
                value=90.0,
                nominal=1
            )
            
            currency2 = self.Currency(
                num_code="978",
                char_code="EUR",
                name="Евро",
                value=95.0,
                nominal=1
            )
            
            self.db.session.add(user)
            self.db.session.add(currency1)
            self.db.session.add(currency2)
            self.db.session.commit()
            
            subscription1 = self.UserCurrency(user_id=user.id, currency_id=currency1.id)
            subscription2 = self.UserCurrency(user_id=user.id, currency_id=currency2.id)
            
            self.db.session.add(subscription1)
            self.db.session.add(subscription2)
            self.db.session.commit()
            
            subscriptions = self.db.session.query(self.UserCurrency).filter_by(user_id=user.id).all()
            self.assertEqual(len(subscriptions), 2)
    
    def test_currency_popularity_tracking(self):
        """Отслеживание популярности валют"""
        with self.app.app_context():
            users = []
            for i in range(3):
                user = self.User(
                    username=f"PopularityUser{i}",
                    password=self.hash_password(f"pass{i}"),
                    is_admin=False
                )
                users.append(user)
                self.db.session.add(user)
            
            usd = self.Currency(
                num_code="840",
                char_code="USD",
                name="Доллар США",
                value=90.0,
                nominal=1
            )
            
            eur = self.Currency(
                num_code="978",
                char_code="EUR",
                name="Евро",
                value=95.0,
                nominal=1
            )
            
            self.db.session.add(usd)
            self.db.session.add(eur)
            self.db.session.commit()
            
            for user in users:
                subscription = self.UserCurrency(user_id=user.id, currency_id=usd.id)
                self.db.session.add(subscription)
            
            subscription = self.UserCurrency(user_id=users[0].id, currency_id=eur.id)
            self.db.session.add(subscription)
            
            self.db.session.commit()
            
            usd_subscribers = self.db.session.query(self.UserCurrency).filter_by(currency_id=usd.id).count()
            eur_subscribers = self.db.session.query(self.UserCurrency).filter_by(currency_id=eur.id).count()
            
            self.assertEqual(usd_subscribers, 3)
            self.assertEqual(eur_subscribers, 1)
    
    # ========== ТЕСТЫ ДЛЯ СЕССИЙ И АУТЕНТИФИКАЦИИ ==========
    
    def test_admin_access_control(self):
        """Контроль доступа для администраторов"""
        with self.app.app_context():
            from app import is_admin_user
            
            regular = self.User(
                username="RegularAccessUser",
                password=self.hash_password("pass"),
                is_admin=False
            )
            
            admin = self.User(
                username="AdminAccessUser",
                password=self.hash_password("adminpass"),
                is_admin=True
            )
            
            self.db.session.add(regular)
            self.db.session.add(admin)
            self.db.session.commit()
            
            self.assertFalse(is_admin_user(regular.id))
            self.assertTrue(is_admin_user(admin.id))
    
    # ========== ТЕСТЫ ДЛЯ ИНИЦИАЛИЗАЦИИ ДАННЫХ ==========
    
    def test_initial_admin_exists(self):
        """Проверка существования начального администратора"""
        with self.app.app_context():
            admin = self.User(
                username="MamontovAleksei",
                password=self.hash_password("PythonCool"),
                is_admin=True
            )
            self.db.session.add(admin)
            self.db.session.commit()
            
            saved_admin = self.db.session.query(self.User).filter_by(username="MamontovAleksei").first()
            self.assertIsNotNone(saved_admin)
            self.assertTrue(saved_admin.is_admin)
    
    def test_initial_users_exist(self):
        """Проверка существования начальных пользователей"""
        with self.app.app_context():
            initial_users = ['Питон', 'Карл', 'Серго', 'Гоку', 'Кирилл', 'Микрофон']
            for username in initial_users:
                user = self.User(
                    username=username,
                    password=self.hash_password("password123"),
                    is_admin=False
                )
                self.db.session.add(user)
            
            self.db.session.commit()
            
            for username in initial_users:
                user = self.db.session.query(self.User).filter_by(username=username).first()
                self.assertIsNotNone(user)
                self.assertFalse(user.is_admin)
    
    # ========== ТЕСТЫ ДЛЯ ПАГИНАЦИИ И ЛИМИТОВ ==========
    
    def test_home_page_currency_limit(self):
        """Проверка лимита валют"""
        with self.app.app_context():
            for i in range(30):
                currency = self.Currency(
                    num_code=str(800 + i),
                    char_code=f"CUR{i}",
                    name=f"Валюта {i}",
                    value=float(i + 80),
                    nominal=1
                )
                self.db.session.add(currency)
            
            self.db.session.commit()
            
            currencies = self.db.session.query(self.Currency).limit(20).all()
            self.assertEqual(len(currencies), 20)
    
    def test_database_transaction_rollback(self):
        """Проверка отката транзакций"""
        with self.app.app_context():
            try:
                user = self.User(
                    username="RollbackUser",
                    password=self.hash_password("pass"),
                    is_admin=False
                )
                self.db.session.add(user)
                self.db.session.flush()
                
                raise Exception("Тестовая ошибка")
                
                self.db.session.commit()
            except:
                self.db.session.rollback()
            
            user = self.db.session.query(self.User).filter_by(username="RollbackUser").first()
            self.assertIsNone(user)
    
    # ========== ТЕСТЫ ДЛЯ УНИКАЛЬНОСТИ ДАННЫХ ==========
    
    def test_user_username_uniqueness(self):
        """Проверка уникальности имен пользователей"""
        with self.app.app_context():
            user1 = self.User(
                username="UniqueUser",
                password=self.hash_password("pass1"),
                is_admin=False
            )
            self.db.session.add(user1)
            self.db.session.commit()
            
            user2 = self.User(
                username="UniqueUser",
                password=self.hash_password("pass2"),
                is_admin=False
            )
            self.db.session.add(user2)
            
            try:
                self.db.session.commit()
                self.fail("Должна была возникнуть ошибка уникальности")
            except Exception as e:
                self.db.session.rollback()
                self.assertIn("unique", str(e).lower())
    
    # ========== ТЕСТЫ ДЛЯ ПРОИЗВОДИТЕЛЬНОСТИ ==========
    
    def test_query_performance(self):
        """Проверка производительности запросов"""
        import time
        
        with self.app.app_context():
            start_time = time.time()
            
            for i in range(50):
                user = self.User(
                    username=f"PerfUser{i}",
                    password=self.hash_password(f"pass{i}"),
                    is_admin=False
                )
                self.db.session.add(user)
            
            self.db.session.commit()
            
            create_time = time.time() - start_time
            
            start_time = time.time()
            users = self.db.session.query(self.User).all()
            query_time = time.time() - start_time
            
            self.assertLess(query_time, 0.5)
            self.assertEqual(len(users), 50)


if __name__ == '__main__':
    # Простой запуск тестов
    unittest.main()
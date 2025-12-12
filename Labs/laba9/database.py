import sqlite3
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any

class Database:
    """Управление SQLite базой данных"""
    
    def __init__(self, db_path=':memory:'):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.create_tables()
        self.seed_data()
    
    def create_tables(self):
        """Создание таблиц в БД"""
        cursor = self.conn.cursor()
        
        # Пользователи (админы и обычные)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE,
                password_hash TEXT NOT NULL,
                full_name TEXT,
                is_admin BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Сессии для авторизации
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                token TEXT UNIQUE NOT NULL,
                expires_at TIMESTAMP NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        ''')
        
        # Валюты с курсами
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS currencies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                num_code TEXT NOT NULL,
                char_code TEXT NOT NULL UNIQUE,
                name TEXT NOT NULL,
                value REAL DEFAULT 1.0,
                nominal INTEGER DEFAULT 1,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Избранные валюты пользователей
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_favorites (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                currency_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (currency_id) REFERENCES currencies(id) ON DELETE CASCADE,
                UNIQUE(user_id, currency_id)
            )
        ''')
        
        self.conn.commit()
    
    def hash_password(self, password: str) -> str:
        """Хеширование пароля"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password: str, password_hash: str) -> bool:
        """Проверка пароля"""
        return self.hash_password(password) == password_hash
    
    def seed_data(self):
        """Начальное заполнение данными"""
        cursor = self.conn.cursor()
        
        # Администратор (из задания)
        admin_password = self.hash_password("PythonCool")
        try:
            cursor.execute(
                '''INSERT OR IGNORE INTO users 
                (username, email, password_hash, full_name, is_admin) 
                VALUES (?, ?, ?, ?, ?)''',
                ('MamontovAleksei', 'admin@example.com', admin_password, 'Мамонтов Алексей', 1)
            )
        except:
            pass
        
        # Пользователи из задания
        users = [
            ('Python', 'python@example.com', self.hash_password('python123'), 'Питон', 0),
            ('Karl', 'karl@example.com', self.hash_password('karl123'), 'Карл', 0),
            ('Sergo', 'sergo@example.com', self.hash_password('sergo123'), 'Серго', 0),
            ('Goku', 'goku@example.com', self.hash_password('goku123'), 'Гоку', 0),
            ('Kirill', 'kirill@example.com', self.hash_password('kirill123'), 'Кирилл', 0),
            ('Microphone', 'microphone@example.com', self.hash_password('microphone123'), 'Микрофон', 0),
        ]
        
        for username, email, password_hash, full_name, is_admin in users:
            try:
                cursor.execute(
                    '''INSERT OR IGNORE INTO users 
                    (username, email, password_hash, full_name, is_admin) 
                    VALUES (?, ?, ?, ?, ?)''',
                    (username, email, password_hash, full_name, is_admin)
                )
            except:
                pass
        
        # Основные валюты (20 шт кроме рубля)
        currencies = [
            ('840', 'USD', 'Доллар США', 90.0, 1),
            ('978', 'EUR', 'Евро', 98.0, 1),
            ('826', 'GBP', 'Фунт стерлингов', 114.0, 1),
            ('392', 'JPY', 'Японская иена', 0.60, 100),
            ('756', 'CHF', 'Швейцарский франк', 102.0, 1),
            ('124', 'CAD', 'Канадский доллар', 67.0, 1),
            ('036', 'AUD', 'Австралийский доллар', 59.0, 1),
            ('156', 'CNY', 'Китайский юань', 12.5, 1),
            ('344', 'HKD', 'Гонконгский доллар', 11.6, 1),
            ('702', 'SGD', 'Сингапурский доллар', 67.3, 1),
            ('554', 'NZD', 'Новозеландский доллар', 55.4, 1),
            ('410', 'KRW', 'Южнокорейская вона', 0.068, 1),
            ('356', 'INR', 'Индийская рупия', 1.08, 1),
            ('986', 'BRL', 'Бразильский реал', 18.4, 1),
            ('710', 'ZAR', 'Южноафриканский рэнд', 4.9, 1),
            ('949', 'TRY', 'Турецкая лира', 2.9, 1),
            ('484', 'MXN', 'Мексиканское песо', 5.3, 1),
            ('752', 'SEK', 'Шведская крона', 8.7, 1),
            ('578', 'NOK', 'Норвежская крона', 8.5, 1),
            ('208', 'DKK', 'Датская крона', 13.1, 1),
        ]
        
        for num_code, char_code, name, value, nominal in currencies:
            try:
                cursor.execute(
                    '''INSERT OR IGNORE INTO currencies 
                    (num_code, char_code, name, value, nominal) 
                    VALUES (?, ?, ?, ?, ?)''',
                    (num_code, char_code, name, value, nominal)
                )
            except:
                pass
        
        # Российский рубль
        try:
            cursor.execute(
                '''INSERT OR IGNORE INTO currencies 
                (num_code, char_code, name, value, nominal) 
                VALUES (?, ?, ?, ?, ?)''',
                ('643', 'RUB', 'Российский рубль', 1.0, 1)
            )
        except:
            pass
        
        self.conn.commit()
        print("✅ База данных инициализирована с тестовыми данными")
    
    def create_session(self, user_id: int) -> str:
        """Создание сессии для пользователя"""
        cursor = self.conn.cursor()
        token = secrets.token_urlsafe(32)
        expires_at = datetime.now() + timedelta(hours=24)
        
        cursor.execute(
            'INSERT INTO sessions (user_id, token, expires_at) VALUES (?, ?, ?)',
            (user_id, token, expires_at)
        )
        self.conn.commit()
        return token
    
    def get_user_by_session(self, token: str) -> Optional[Dict[str, Any]]:
        """Получение пользователя по токену сессии"""
        cursor = self.conn.cursor()
        cursor.execute(
            '''SELECT u.* FROM users u 
            JOIN sessions s ON u.id = s.user_id 
            WHERE s.token = ? AND s.expires_at > ?''',
            (token, datetime.now())
        )
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def delete_session(self, token: str):
        """Удаление сессии"""
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM sessions WHERE token = ?', (token,))
        self.conn.commit()
    
    # CRUD для пользователей
    def create_user(self, username: str, email: str, password: str, full_name: str, is_admin: bool = False) -> Optional[int]:
        """Создание нового пользователя"""
        try:
            cursor = self.conn.cursor()
            password_hash = self.hash_password(password)
            cursor.execute(
                '''INSERT INTO users (username, email, password_hash, full_name, is_admin) 
                VALUES (?, ?, ?, ?, ?)''',
                (username, email, password_hash, full_name, is_admin)
            )
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None
    
    def get_user_by_credentials(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Поиск пользователя по логину и паролю"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        row = cursor.fetchone()
        
        if row and self.verify_password(password, row['password_hash']):
            return dict(row)
        return None
    
    def get_all_users(self) -> List[Dict[str, Any]]:
        """Получение всех пользователей"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM users ORDER BY id')
        return [dict(row) for row in cursor.fetchall()]
    
    def delete_user(self, user_id: int) -> bool:
        """Удаление пользователя"""
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
        self.conn.commit()
        return cursor.rowcount > 0
    
    def get_user_password(self, user_id: int) -> Optional[str]:
        """Получение хеша пароля пользователя (для админа)"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT password_hash FROM users WHERE id = ?', (user_id,))
        row = cursor.fetchone()
        return row['password_hash'] if row else None
    
    # CRUD для валют
    def get_all_currencies(self) -> List[Dict[str, Any]]:
        """Получение всех валют"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM currencies ORDER BY char_code')
        return [dict(row) for row in cursor.fetchall()]
    
    def get_currency(self, currency_id: int) -> Optional[Dict[str, Any]]:
        """Получение валюты по ID"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM currencies WHERE id = ?', (currency_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def get_currency_by_code(self, char_code: str) -> Optional[Dict[str, Any]]:
        """Получение валюты по коду"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM currencies WHERE char_code = ?', (char_code,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def create_currency(self, num_code: str, char_code: str, name: str, value: float, nominal: int = 1) -> Optional[int]:
        """Создание новой валюты"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                '''INSERT INTO currencies (num_code, char_code, name, value, nominal, updated_at) 
                VALUES (?, ?, ?, ?, ?, ?)''',
                (num_code, char_code.upper(), name, value, nominal, datetime.now())
            )
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None
    
    def update_currency(self, currency_id: int, value: float) -> bool:
        """Обновление курса валюты"""
        cursor = self.conn.cursor()
        cursor.execute(
            'UPDATE currencies SET value = ?, updated_at = ? WHERE id = ?',
            (value, datetime.now(), currency_id)
        )
        self.conn.commit()
        return cursor.rowcount > 0
    
    def delete_currency(self, currency_id: int) -> bool:
        """Удаление валюты"""
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM currencies WHERE id = ?', (currency_id,))
        self.conn.commit()
        return cursor.rowcount > 0
    
    def update_currency_from_api(self, char_code: str, value: float) -> bool:
        """Обновление курса валюты из API"""
        cursor = self.conn.cursor()
        cursor.execute(
            'UPDATE currencies SET value = ?, updated_at = ? WHERE char_code = ?',
            (value, datetime.now(), char_code.upper())
        )
        self.conn.commit()
        return cursor.rowcount > 0
    
    # Избранные валюты
    def add_favorite(self, user_id: int, currency_id: int) -> bool:
        """Добавление валюты в избранное"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                'INSERT OR IGNORE INTO user_favorites (user_id, currency_id) VALUES (?, ?)',
                (user_id, currency_id)
            )
            self.conn.commit()
            return True
        except:
            return False
    
    def remove_favorite(self, user_id: int, currency_id: int) -> bool:
        """Удаление валюты из избранного"""
        cursor = self.conn.cursor()
        cursor.execute(
            'DELETE FROM user_favorites WHERE user_id = ? AND currency_id = ?',
            (user_id, currency_id)
        )
        self.conn.commit()
        return cursor.rowcount > 0
    
    def get_user_favorites(self, user_id: int) -> List[Dict[str, Any]]:
        """Получение избранных валют пользователя"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT c.* FROM currencies c
            JOIN user_favorites uf ON c.id = uf.currency_id
            WHERE uf.user_id = ?
            ORDER BY c.char_code
        ''', (user_id,))
        return [dict(row) for row in cursor.fetchall()]
    
    def is_favorite(self, user_id: int, currency_id: int) -> bool:
        """Проверка, есть ли валюта в избранном"""
        cursor = self.conn.cursor()
        cursor.execute(
            'SELECT 1 FROM user_favorites WHERE user_id = ? AND currency_id = ?',
            (user_id, currency_id)
        )
        return cursor.fetchone() is not None
    
    def close(self):
        """Закрытие соединения с БД"""
        self.conn.close()

# Глобальный экземпляр БД
db = Database()
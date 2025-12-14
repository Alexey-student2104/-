from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests
import hashlib
import os
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Используем файловую базу данных для сохранения данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///currencies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Модели
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Currency(db.Model):
    __tablename__ = 'currency'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    num_code = db.Column(db.String(3), nullable=False)
    char_code = db.Column(db.String(3), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    value = db.Column(db.Float, nullable=False)
    nominal = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return f'<Currency {self.char_code} {self.value}>'

class UserCurrency(db.Model):
    __tablename__ = 'user_currency'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    currency_id = db.Column(db.Integer, db.ForeignKey('currency.id'), nullable=False)
    
    user = db.relationship('User', backref=db.backref('currencies', lazy=True))
    currency = db.relationship('Currency', backref=db.backref('users', lazy=True))

# Хеширование пароля
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Инициализация базы данных
def init_db():
    with app.app_context():
        # Проверяем, существует ли файл базы данных
        db_exists = os.path.exists('currencies.db')
        
        # Создаем все таблицы
        db.create_all()
        
        # Если база данных новая (файл не существовал), инициализируем начальные данные
        if not db_exists:
            print("Инициализация начальных данных...")
            init_data()
        else:
            # Проверяем, есть ли администратор
            admin = User.query.filter_by(username='MamontovAleksei').first()
            if not admin:
                admin = User(username='MamontovAleksei', 
                            password=hash_password('PythonCool'), 
                            is_admin=True)
                db.session.add(admin)
                db.session.commit()

def add_test_currencies():
    """Добавление тестовых данных о валютах"""
    test_currencies = [
        ("840", "USD", "Доллар США", 90.0, 1),
        ("978", "EUR", "Евро", 91.0, 1),
        ("826", "GBP", "Фунт стерлингов", 105.0, 1),
        ("392", "JPY", "Японская иена", 0.6, 100),
        ("156", "CNY", "Китайский юань", 12.5, 1),
        ("756", "CHF", "Швейцарский франк", 95.0, 1),
        ("124", "CAD", "Канадский доллар", 70.0, 1),
        ("036", "AUD", "Австралийский доллар", 65.0, 1),
        ("554", "NZD", "Новозеландский доллар", 60.0, 1),
        ("702", "SGD", "Сингапурский доллар", 75.0, 1),
        ("344", "HKD", "Гонконгский доллар", 11.5, 1),
        ("752", "SEK", "Шведская крона", 9.0, 1),
        ("578", "NOK", "Норвежская крона", 9.5, 1),
        ("208", "DKK", "Датская крона", 12.0, 1),
        ("949", "TRY", "Турецкая лира", 3.0, 1),
        ("410", "KRW", "Вон Республики Корея", 0.07, 100),
        ("356", "INR", "Индийская рупия", 1.1, 1),
        ("986", "BRL", "Бразильский реал", 18.0, 1),
        ("710", "ZAR", "Южноафриканский рэнд", 5.0, 1),
        ("484", "MXN", "Мексиканское песо", 5.5, 1)
    ]
    
    for num_code, char_code, name, value, nominal in test_currencies:
        currency = Currency(num_code=num_code, char_code=char_code, 
                           name=name, value=value, nominal=nominal)
        db.session.add(currency)
    db.session.commit()

def create_specific_subscriptions():
    """Создание конкретных подписок для каждого пользователя"""
    with app.app_context():
        try:
            # Очищаем все старые подписки
            UserCurrency.query.delete()
            db.session.commit()
            
            # Находим пользователей
            users = User.query.filter_by(is_admin=False).all()
            currencies = Currency.query.all()
            
            if not users or not currencies:
                return
            
            # Подписываем каждого пользователя на разные валюты
            for i, user in enumerate(users):
                # Берем разные валюты для каждого пользователя
                start_idx = i % len(currencies)
                num_subs = min(3, len(currencies))
                
                for j in range(num_subs):
                    idx = (start_idx + j) % len(currencies)
                    currency = currencies[idx]
                    
                    subscription = UserCurrency(
                        user_id=user.id,
                        currency_id=currency.id
                    )
                    db.session.add(subscription)
            
            db.session.commit()
            
        except Exception as e:
            db.session.rollback()

# Инициализация начальных данных
def init_data():
    """Инициализация начальных данных"""
    try:
        # Добавляем начальных пользователей
        initial_users = ['Питон', 'Карл', 'Серго', 'Гоку', 'Кирилл', 'Микрофон']
        for username in initial_users:
            if not User.query.filter_by(username=username).first():
                user = User(username=username, 
                           password=hash_password('password123'), 
                           is_admin=False)
                db.session.add(user)
        
        # Добавляем администратора
        if not User.query.filter_by(username='MamontovAleksei').first():
            admin = User(username='MamontovAleksei', 
                        password=hash_password('PythonCool'), 
                        is_admin=True)
            db.session.add(admin)
        
        # Добавляем валюты
        if Currency.query.count() == 0:
            add_test_currencies()
        
        # Создаем подписки
        create_specific_subscriptions()
        
        db.session.commit()
        
    except Exception as e:
        db.session.rollback()
        raise

def is_admin_user(user_id):
    """Проверка, является ли пользователь администратором"""
    if not user_id:
        return False
    user = User.query.get(user_id)
    return user.is_admin if user else False

# Контекстный процессор для передачи функции в шаблоны
@app.context_processor
def utility_processor():
    return dict(is_admin_user=is_admin_user)

# ========== МАРШРУТЫ ==========

@app.route('/')
def index():
    currencies = Currency.query.limit(20).all()
    return render_template('index.html', currencies=currencies)

@app.route('/author')
def author():
    return render_template('author.html')

@app.route('/users')
def users():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_list = User.query.all()
    return render_template('users.html', users=user_list, 
                          is_admin=is_admin_user(session.get('user_id')))

@app.route('/user')
def user():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = request.args.get('id')
    if user_id:
        user_data = User.query.get(user_id)
        if user_data:
            return render_template('user.html', user=user_data)
    return redirect(url_for('users'))

@app.route('/currencies')
def currencies():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    currency_list = Currency.query.all()
    user_id = session.get('user_id')
    
    # Получаем подписки текущего пользователя
    user_subscriptions = []
    if user_id:
        subscriptions = UserCurrency.query.filter_by(user_id=user_id).all()
        user_subscriptions = [sub.currency_id for sub in subscriptions]
    
    return render_template('currencies.html', 
                          currencies=currency_list,
                          user_subscriptions=user_subscriptions)

@app.route('/currency/delete')
def delete_currency_route():
    if 'user_id' not in session or not is_admin_user(session.get('user_id')):
        return redirect(url_for('login'))
    
    currency_id = request.args.get('id')
    if currency_id:
        currency = Currency.query.get(currency_id)
        if currency:
            db.session.delete(currency)
            db.session.commit()
    return redirect(url_for('currencies'))

@app.route('/currency/update')
def update_currency_route():
    if 'user_id' not in session or not is_admin_user(session.get('user_id')):
        return redirect(url_for('login'))
    
    return redirect(url_for('currencies'))

@app.route('/currency/show')
def show_currencies():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    currencies = Currency.query.all()
    for currency in currencies:
        print(f"{currency.char_code}: {currency.value}")
    return "Курсы валют выведены в консоль"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = hash_password(request.form['password'])
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('index'))
        return render_template('login.html', error='Неверные учетные данные')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = hash_password(request.form['password'])
        
        # Проверяем, существует ли пользователь
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return render_template('register.html', error='Пользователь уже существует')
        
        # Создаем нового пользователя
        new_user = User(username=username, password=password, is_admin=False)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/admin')
def admin():
    if 'user_id' not in session or not is_admin_user(session.get('user_id')):
        return redirect(url_for('login'))
    
    users = User.query.all()
    currencies = Currency.query.all()
    return render_template('admin.html', users=users, currencies=currencies)

@app.route('/admin/delete_user/<int:user_id>')
def admin_delete_user(user_id):
    if 'user_id' not in session or not is_admin_user(session.get('user_id')):
        return redirect(url_for('login'))
    
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for('admin'))

@app.route('/admin/add_currency', methods=['POST'])
def admin_add_currency():
    if 'user_id' not in session or not is_admin_user(session.get('user_id')):
        return redirect(url_for('login'))
    
    num_code = request.form['num_code']
    char_code = request.form['char_code']
    name = request.form['name']
    value = float(request.form['value'])
    nominal = int(request.form['nominal'])
    
    new_currency = Currency(num_code=num_code, char_code=char_code, 
                           name=name, value=value, nominal=nominal)
    db.session.add(new_currency)
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/admin/reset_database')
def reset_database():
    """Сброс базы данных к начальному состоянию"""
    if 'user_id' not in session or not is_admin_user(session.get('user_id')):
        return redirect(url_for('login'))
    
    try:
        # Закрываем все соединения
        db.session.remove()
        
        # Удаляем файл базы данных если он существует
        if os.path.exists('currencies.db'):
            os.remove('currencies.db')
        
        # Ждем немного
        time.sleep(0.5)
        
        # Пересоздаем базу с начальными данными
        db.create_all()
        init_data()
        
        return redirect(url_for('admin'))
    except Exception as e:
        return f"Ошибка при сбросе базы данных: {e}"

@app.route('/admin/generate_subscriptions')
def generate_test_subscriptions():
    """Генерация тестовых подписок"""
    if 'user_id' not in session or not is_admin_user(session.get('user_id')):
        return redirect(url_for('login'))
    
    create_specific_subscriptions()
    return redirect(url_for('users'))

@app.route('/admin/subscriptions_stats')
def subscriptions_statistics():
    """Статистика по подпискам"""
    if 'user_id' not in session or not is_admin_user(session.get('user_id')):
        return redirect(url_for('login'))
    
    # Статистика по пользователям
    users_stats = []
    users = User.query.all()
    
    for user in users:
        subscription_count = UserCurrency.query.filter_by(user_id=user.id).count()
        users_stats.append({
            'user': user,
            'subscription_count': subscription_count,
        })
    
    # Статистика по валютам
    currencies_stats = []
    currencies = Currency.query.all()
    
    for currency in currencies:
        subscriber_count = UserCurrency.query.filter_by(currency_id=currency.id).count()
        currencies_stats.append({
            'currency': currency,
            'subscriber_count': subscriber_count
        })
    
    users_stats.sort(key=lambda x: x['subscription_count'], reverse=True)
    currencies_stats.sort(key=lambda x: x['subscriber_count'], reverse=True)
    
    return render_template('subscriptions_stats.html',
                         users_stats=users_stats,
                         currencies_stats=currencies_stats)

# Маршруты для подписок на валюты
@app.route('/subscribe/<int:currency_id>')
def subscribe_to_currency(currency_id):
    """Подписаться на валюту"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    
    # Проверяем, не подписан ли уже пользователь
    existing = UserCurrency.query.filter_by(
        user_id=user_id, 
        currency_id=currency_id
    ).first()
    
    if not existing:
        subscription = UserCurrency(user_id=user_id, currency_id=currency_id)
        db.session.add(subscription)
        db.session.commit()
        session['message'] = 'Вы успешно подписались на валюту'
    
    return redirect(url_for('user_subscriptions'))

@app.route('/unsubscribe/<int:currency_id>')
def unsubscribe_from_currency(currency_id):
    """Отписаться от валюты"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    
    # Находим и удаляем подписку
    subscription = UserCurrency.query.filter_by(
        user_id=user_id, 
        currency_id=currency_id
    ).first()
    
    if subscription:
        db.session.delete(subscription)
        db.session.commit()
        session['message'] = 'Вы успешно отписались от валюты'
    
    return redirect(url_for('user_subscriptions'))

@app.route('/user/subscriptions')
def user_subscriptions():
    """Страница подписок текущего пользователя"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    user = User.query.get(user_id)
    
    # Получаем подписки пользователя
    subscriptions = UserCurrency.query.filter_by(user_id=user_id).all()
    subscribed_currencies = []
    
    for sub in subscriptions:
        currency = Currency.query.get(sub.currency_id)
        if currency:
            subscribed_currencies.append(currency)
    
    # Получаем все доступные валюты
    all_currencies = Currency.query.all()
    
    # Получаем сообщение из сессии, если есть
    message = session.pop('message', None)
    
    return render_template('subscriptions.html', 
                         user=user,
                         subscribed_currencies=subscribed_currencies,
                         all_currencies=all_currencies,
                         message=message)

@app.route('/user/<int:user_id>/subscriptions')
def view_user_subscriptions(user_id):
    """Просмотр подписок другого пользователя"""
    if 'user_id' not in session or not is_admin_user(session.get('user_id')):
        return redirect(url_for('login'))
    
    user = User.query.get(user_id)
    if not user:
        return redirect(url_for('users'))
    
    # Получаем подписки пользователя
    subscriptions = UserCurrency.query.filter_by(user_id=user_id).all()
    subscribed_currencies = []
    
    for sub in subscriptions:
        currency = Currency.query.get(sub.currency_id)
        if currency:
            subscribed_currencies.append(currency)
    
    return render_template('user_subscriptions_admin.html', 
                         user=user,
                         subscribed_currencies=subscribed_currencies)

@app.route('/fetch_currencies')
def fetch_currencies():
    """Получение курсов валют с API Центробанка России"""
    if 'user_id' not in session or not is_admin_user(session.get('user_id')):
        return redirect(url_for('login'))
    
    try:
        response = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
        data = response.json()
        
        currencies_data = data['Valute']
        
        # Очищаем старые данные
        Currency.query.delete()
        
        # Основные валюты
        main_currencies = ['USD', 'EUR', 'GBP', 'JPY', 'CNY', 'CHF', 'CAD', 'AUD']
        
        for char_code in main_currencies:
            if char_code in currencies_data:
                currency_info = currencies_data[char_code]
                currency = Currency(
                    num_code=str(currency_info['NumCode']),
                    char_code=currency_info['CharCode'],
                    name=currency_info['Name'],
                    value=currency_info['Value'],
                    nominal=currency_info['Nominal']
                )
                db.session.add(currency)
        
        db.session.commit()
        return redirect(url_for('currencies'))
    except Exception as e:
        # Если API не доступно, добавляем тестовые данные
        add_test_currencies()
        return redirect(url_for('currencies'))

@app.teardown_appcontext
def shutdown_session(exception=None):
    """Закрытие сессии при завершении контекста"""
    db.session.remove()

if __name__ == '__main__':
    # Инициализация базы данных
    init_db()
    
    print("Сервер запущен")
    print("Сайт доступен по адресу: http://localhost:5000")
    
    # Запуск сервера
    app.run(debug=True, port=5000, use_reloader=False)
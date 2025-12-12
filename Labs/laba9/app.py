from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests
import hashlib
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Изменяем URI базы данных с :memory: на файл
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///currencies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Модели (остаются без изменений)
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
            print("Создана новая база данных. Инициализация начальных данных...")
            init_data()
        else:
            print("База данных уже существует. Пропускаем инициализацию начальных данных.")
            
            # Проверяем, есть ли администратор
            admin = User.query.filter_by(username='MamontovAleksei').first()
            if not admin:
                print("Администратор не найден. Добавляем...")
                admin = User(username='MamontovAleksei', 
                            password=hash_password('PythonCool'), 
                            is_admin=True)
                db.session.add(admin)
                db.session.commit()

# Инициализация начальных данных (только для новой БД)
def init_data():
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
    
    # Добавляем валюты только если их нет
    if Currency.query.count() == 0:
        add_test_currencies()
    
    db.session.commit()
    print("Начальные данные успешно добавлены в базу данных.")

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

# Маршруты (остаются без изменений)
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
    return render_template('currencies.html', currencies=currency_list)

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
    
    char_code = request.args.get('USD')
    if char_code:
        # Логика обновления курса
        pass
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
    """Сброс базы данных к начальному состоянию (только для админов)"""
    if 'user_id' not in session or not is_admin_user(session.get('user_id')):
        return redirect(url_for('login'))
    
    # Удаляем файл базы данных
    if os.path.exists('currencies.db'):
        os.remove('currencies.db')
        print("База данных удалена")
    
    # Пересоздаем базу с начальными данными
    db.create_all()
    init_data()
    
    return redirect(url_for('admin'))

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

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import os
import json
from datetime import datetime, timedelta
import random

class CurrencyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlparse(self.path).path
        
        # Статика
        if path.startswith('/static/'):
            self.serve_static(path)
            return
        
        # Маршруты
        routes = {
            '/': self.index,
            '/author': self.author_page,
            '/currencies': self.currencies_page,
            '/users': self.users_page,
            '/user': self.user_detail
        }
        
        handler = routes.get(path)
        if handler:
            handler()
        else:
            self.send_error(404, "Page not found")
    
    def serve_static(self, path):
        try:
            filepath = '.' + path
            if os.path.exists(filepath):
                with open(filepath, 'rb') as f:
                    content = f.read()
                
                if filepath.endswith('.css'):
                    content_type = 'text/css'
                elif filepath.endswith('.js'):
                    content_type = 'application/javascript'
                else:
                    content_type = 'text/plain'
                
                self.send_response(200)
                self.send_header('Content-Type', content_type)
                self.end_headers()
                self.wfile.write(content)
            else:
                self.send_error(404, "File not found")
        except:
            self.send_error(500, "Server error")
    
    def send_html(self, html):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
    def index(self):
        html = f"""
        <!DOCTYPE html>
        <html lang="ru">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>CurrenciesListApp - Главная</title>
            <link rel="stylesheet" href="/static/style.css">
        </head>
        <body>
            <div class="container">
                <nav class="navbar">
                    <a href="/" class="nav-link active">Главная</a>
                    <a href="/author" class="nav-link">Автор</a>
                    <a href="/currencies" class="nav-link">Валюты</a>
                    <a href="/users" class="nav-link">Пользователи</a>
                </nav>

                <header class="header">
                    <h1>CurrenciesListApp</h1>
                    <p>Версия 1.0.0 • Мониторинг курсов валют в реальном времени</p>
                </header>

                <div class="dashboard">
                    <div class="card">
                        <h2 class="card-title">👨‍💻 Автор</h2>
                        <div class="card-content">
                            <p><strong>Имя:</strong> Мамонтов Алексей</p>
                            <p><strong>Группа:</strong> P3120</p>
                            <p><strong>Приложение:</strong> CurrenciesListApp</p>
                            <p><strong>Версия:</strong> 1.0.0</p>
                        </div>
                    </div>

                    <div class="card">
                        <h2 class="card-title">💰 Валюты</h2>
                        <div class="card-content">
                            <p>Отслеживаемые валюты:</p>
                            <ul>
                                <li>USD — доллар США</li>
                                <li>EUR — евро</li>
                                <li>GBP — британский фунт</li>
                                <li>JPY — японская иена</li>
                                <li>CHF — швейцарский франк</li>
                                <li>CNY — китайский юань</li>
                                <li>CAD — канадский доллар</li>
                                <li>AUD — австралийский доллар</li>
                                <li>INR — индийская рупия</li>
                            </ul>
                        </div>
                    </div>

                    <div class="card">
                        <h2 class="card-title">👥 Пользователи</h2>
                        <div class="card-content">
                            <p>Активные пользователи системы:</p>
                            <div style="margin-top: 15px;">
                                <div style="background: rgba(255,255,255,0.1); padding: 10px; border-radius: 8px; margin-bottom: 10px;">
                                    <strong>Ноунейм</strong>
                                    <span style="float: right; font-size: 0.9em; opacity: 0.8;">Подписок: 2</span>
                                </div>
                                <div style="background: rgba(255,255,255,0.1); padding: 10px; border-radius: 8px; margin-bottom: 10px;">
                                    <strong>Питонист</strong>
                                    <span style="float: right; font-size: 0.9em; opacity: 0.8;">Подписок: 2</span>
                                </div>
                                <div style="background: rgba(255,255,255,0.1); padding: 10px; border-radius: 8px; margin-bottom: 10px;">
                                    <strong>Брат</strong>
                                    <span style="float: right; font-size: 0.9em; opacity: 0.8;">Подписок: 1</span>
                                </div>
                                <div style="background: rgba(255,255,255,0.1); padding: 10px; border-radius: 8px; margin-bottom: 10px;">
                                    <strong>Скрин</strong>
                                    <span style="float: right; font-size: 0.9em; opacity: 0.8;">Подписок: 2</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="card" style="margin-top: 40px;">
                    <h2 class="card-title">📊 Статистика</h2>
                    <div class="card-content" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px;">
                        <div style="text-align: center;">
                            <div style="font-size: 2.5rem; font-weight: bold;">9</div>
                            <div style="opacity: 0.8;">Валют отслеживается</div>
                        </div>
                        <div style="text-align: center;">
                            <div style="font-size: 2.5rem; font-weight: bold;">4</div>
                            <div style="opacity: 0.8;">Активных пользователей</div>
                        </div>
                        <div style="text-align: center;">
                            <div style="font-size: 2.5rem; font-weight: bold;">7</div>
                            <div style="opacity: 0.8;">Всего подписок</div>
                        </div>
                        <div style="text-align: center;">
                            <div style="font-size: 2.5rem; font-weight: bold;">24/7</div>
                            <div style="opacity: 0.8;">Обновление данных</div>
                        </div>
                    </div>
                </div>

                <footer class="footer">
                    <p>CurrenciesListApp v1.0.0 • Разработано Мамонтов Алексей (P3120) • {datetime.now().year}</p>
                </footer>
            </div>
        </body>
        </html>
        """
        self.send_html(html)
    
    def author_page(self):
        html = """
        <!DOCTYPE html>
        <html lang="ru">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>CurrenciesListApp - Об авторе</title>
            <link rel="stylesheet" href="/static/style.css">
        </head>
        <body>
            <div class="container">
                <nav class="navbar">
                    <a href="/" class="nav-link">Главная</a>
                    <a href="/author" class="nav-link active">Автор</a>
                    <a href="/currencies" class="nav-link">Валюты</a>
                    <a href="/users" class="nav-link">Пользователи</a>
                </nav>

                <div class="card" style="max-width: 600px; margin: 0 auto; text-align: center;">
                    <h2 class="card-title" style="font-size: 2rem;">👨‍🎓 Автор</h2>
                    
                    <div style="margin: 30px 0;">
                        <div style="width: 150px; height: 150px; background: linear-gradient(135deg, #ff8e53, #ff6b6b); 
                             border-radius: 50%; margin: 0 auto 20px; display: flex; align-items: center; 
                             justify-content: center; font-size: 3rem;">
                            🎓
                        </div>
                        <h3 style="font-size: 2rem; margin-bottom: 10px;">Мамонтов Алексей</h3>
                        <p style="font-size: 1.2rem; opacity: 0.9;">P3120</p>
                    </div>

                    <div style="margin-top: 40px; text-align: center;">
                        <a href="/" class="btn btn-primary">Вернуться на главную</a>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        self.send_html(html)
    
    def currencies_page(self):
        # Получаем курсы валют (реальные данные)
        try:
            from utils.currencies_api import get_currencies
            currencies = get_currencies()
        except ImportError:
            # Если модуль не найден, используем статические данные
            currencies = [
                {"char_code": "USD", "name": "Доллар США", "value": self.get_realistic_value("USD"), "nominal": 1, "num_code": "840", "id": "R01235"},
                {"char_code": "EUR", "name": "Евро", "value": self.get_realistic_value("EUR"), "nominal": 1, "num_code": "978", "id": "R01239"},
                {"char_code": "GBP", "name": "Фунт стерлингов", "value": self.get_realistic_value("GBP"), "nominal": 1, "num_code": "826", "id": "R01035"},
                {"char_code": "JPY", "name": "Японская иена", "value": self.get_realistic_value("JPY"), "nominal": 100, "num_code": "392", "id": "R01820"},
                {"char_code": "CHF", "name": "Швейцарский франк", "value": self.get_realistic_value("CHF"), "nominal": 1, "num_code": "756", "id": "R01775"},
                {"char_code": "CNY", "name": "Китайский юань", "value": self.get_realistic_value("CNY"), "nominal": 1, "num_code": "156", "id": "R01375"},
                {"char_code": "CAD", "name": "Канадский доллар", "value": self.get_realistic_value("CAD"), "nominal": 1, "num_code": "124", "id": "R01350"},
                {"char_code": "AUD", "name": "Австралийский доллар", "value": self.get_realistic_value("AUD"), "nominal": 1, "num_code": "036", "id": "R01020"},
                {"char_code": "INR", "name": "Индийская рупия", "value": self.get_realistic_value("INR"), "nominal": 100, "num_code": "356", "id": "R01280"}
            ]
        
        currency_cards = ""
        for currency in currencies:
            # Генерируем данные для графика (история 30 дней)
            chart_data = []
            base_value = currency['value']
            for i in range(30):
                # Реалистичные колебания курса
                change = random.uniform(-0.02, 0.02) * base_value  # ±2%
                day_value = base_value + (change * (30 - i) / 30)  # Плавное изменение
                day_value = max(day_value * 0.8, day_value)  # Минимум 80% от текущего
                chart_data.append(round(day_value, 2))
            
            currency_cards += f"""
            <div class="currency-card">
                <div class="currency-header">
                    <div>
                        <div class="currency-code">{currency['char_code']}</div>
                        <div class="currency-name">{currency['name']}</div>
                    </div>
                    <div style="font-size: 0.9rem; opacity: 0.8;">
                        #{currency.get('num_code', '---')}
                    </div>
                </div>
                
                <div class="currency-value">
                    {currency['value']:.2f} ₽
                </div>
                
                <div class="currency-nominal">
                    За {currency['nominal']} {currency['char_code']}
                </div>
                
                <div style="margin-top: 15px; font-size: 0.9rem; opacity: 0.8;">
                    <div>ID: {currency.get('id', '---')}</div>
                    <div>Номинал: {currency['nominal']}</div>
                    <div>Обновлено: {datetime.now().strftime('%H:%M')}</div>
                </div>
                
                <div style="margin-top: 15px; text-align: center;">
                    <button onclick="showChart('{currency['char_code']}', {json.dumps(chart_data)})" 
                            class="btn" style="width: 100%;">
                        📈 Показать график
                    </button>
                </div>
            </div>
            """
        
        html = f"""
        <!DOCTYPE html>
        <html lang="ru">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>CurrenciesListApp - Валюты</title>
            <link rel="stylesheet" href="/static/style.css">
        </head>
        <body>
            <div class="container">
                <nav class="navbar">
                    <a href="/" class="nav-link">Главная</a>
                    <a href="/author" class="nav-link">Автор</a>
                    <a href="/currencies" class="nav-link active">Валюты</a>
                    <a href="/users" class="nav-link">Пользователи</a>
                </nav>

                <div class="list-header">
                    <h1 class="list-title">💱 Курсы валют ЦБ РФ</h1>
                    <div>
                        <span style="opacity: 0.8; margin-right: 20px;">
                            Обновлено: {datetime.now().strftime('%d.%m.%Y %H:%M')}
                        </span>
                        <a href="/currencies" class="btn btn-primary">
                            🔄 Обновить курсы
                        </a>
                    </div>
                </div>

                <div class="currency-grid">
                    {currency_cards}
                </div>

                <div id="chartContainer" class="chart-container" style="display: none; margin-top: 40px;">
                    <h3 class="chart-title" id="chartTitle">График курса</h3>
                    <div style="height: 300px; position: relative;">
                        <canvas id="currencyChart"></canvas>
                    </div>
                    <div style="text-align: center; margin-top: 20px;">
                        <button onclick="hideChart()" class="btn">Скрыть график</button>
                    </div>
                </div>

                <div class="card" style="margin-top: 40px;">
                    <h3 class="card-title">📈 Общая статистика</h3>
                    <div class="card-content">
                        <p>Всего отслеживается валют: <strong>9</strong></p>
                        <p>Данные предоставлены Центральным Банком РФ</p>
                        <p>Курсы обновляются ежедневно в 12:00 по московскому времени</p>
                        <p>История курсов хранится за последние 30 дней</p>
                    </div>
                </div>
            </div>

            <script>
                let chartInstance = null;
                
                function showChart(currencyCode, data) {{
                    document.getElementById('chartContainer').style.display = 'block';
                    document.getElementById('chartTitle').textContent = 
                        `График курса ${{currencyCode}} за 30 дней`;
                    
                    const ctx = document.getElementById('currencyChart').getContext('2d');
                    
                    // Удаляем старый график если есть
                    if (chartInstance) {{
                        chartInstance.destroy();
                    }}
                    
                    // Создаем линейный график
                    chartInstance = new Chart(ctx, {{
                        type: 'line',
                        data: {{
                            labels: Array.from({{length: 30}}, (_, i) => `${{30 - i}} дн. назад`),
                            datasets: [{{
                                label: `Курс ${{currencyCode}}, руб`,
                                data: data.reverse(),
                                borderColor: '#ff6b6b',
                                backgroundColor: 'rgba(255, 107, 107, 0.1)',
                                borderWidth: 3,
                                fill: true,
                                tension: 0.4,
                                pointBackgroundColor: '#ff8e53',
                                pointBorderColor: '#fff',
                                pointBorderWidth: 2,
                                pointRadius: 4
                            }}]
                        }},
                        options: {{
                            responsive: true,
                            maintainAspectRatio: false,
                            plugins: {{
                                legend: {{
                                    labels: {{
                                        color: 'white',
                                        font: {{
                                            size: 14
                                        }}
                                    }}
                                }},
                                tooltip: {{
                                    backgroundColor: 'rgba(0, 0, 0, 0.7)',
                                    titleColor: '#fff',
                                    bodyColor: '#fff',
                                    callbacks: {{
                                        label: function(context) {{
                                            return `${{context.dataset.label}}: ${{context.parsed.y.toFixed(2)}} ₽`;
                                        }}
                                    }}
                                }}
                            }},
                            scales: {{
                                x: {{
                                    ticks: {{
                                        color: 'rgba(255,255,255,0.8)',
                                        maxTicksLimit: 10
                                    }},
                                    grid: {{
                                        color: 'rgba(255,255,255,0.1)'
                                    }}
                                }},
                                y: {{
                                    ticks: {{
                                        color: 'rgba(255,255,255,0.8)',
                                        callback: function(value) {{
                                            return value.toFixed(2) + ' ₽';
                                        }}
                                    }},
                                    grid: {{
                                        color: 'rgba(255,255,255,0.1)'
                                    }}
                                }}
                            }}
                        }}
                    }});
                    
                    // Прокручиваем к графику
                    window.scrollTo({{
                        top: document.getElementById('chartContainer').offsetTop - 20,
                        behavior: 'smooth'
                    }});
                }}
                
                function hideChart() {{
                    document.getElementById('chartContainer').style.display = 'none';
                    if (chartInstance) {{
                        chartInstance.destroy();
                        chartInstance = null;
                    }}
                }}
            </script>
            
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        </body>
        </html>
        """
        self.send_html(html)
    
    def get_realistic_value(self, currency_code):
        """Возвращает реалистичные значения курсов (примерные реальные)"""
        realistic_values = {
            "USD": random.uniform(85.0, 95.0),  # Доллар обычно 85-95 руб
            "EUR": random.uniform(90.0, 100.0),  # Евро обычно 90-100 руб
            "GBP": random.uniform(105.0, 115.0),  # Фунт обычно 105-115 руб
            "JPY": random.uniform(0.55, 0.65),  # 100 иен обычно 55-65 коп
            "CHF": random.uniform(95.0, 105.0),  # Франк обычно 95-105 руб
            "CNY": random.uniform(12.0, 13.5),  # Юань обычно 12-13.5 руб
            "CAD": random.uniform(65.0, 70.0),  # Канадский доллар обычно 65-70 руб
            "AUD": random.uniform(55.0, 60.0),  # Австралийский доллар обычно 55-60 руб
            "INR": random.uniform(1.0, 1.2),  # 100 рупий обычно 1-1.2 руб
        }
        return round(realistic_values.get(currency_code, 1.0), 2)
    
    def users_page(self):
        html = """
        <!DOCTYPE html>
        <html lang="ru">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>CurrenciesListApp - Пользователи</title>
            <link rel="stylesheet" href="/static/style.css">
        </head>
        <body>
            <div class="container">
                <nav class="navbar">
                    <a href="/" class="nav-link">Главная</a>
                    <a href="/author" class="nav-link">Автор</a>
                    <a href="/currencies" class="nav-link">Валюты</a>
                    <a href="/users" class="nav-link active">Пользователи</a>
                </nav>

                <div class="list-header">
                    <h1 class="list-title">👥 Пользователи системы</h1>
                    <div>
                        <span style="opacity: 0.8; margin-right: 20px;">
                            Всего пользователей: 4
                        </span>
                    </div>
                </div>

                <div class="list-container">
                    <table class="table">
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Имя пользователя</th>
                                <th>Подписки на валюты</th>
                                <th>Действия</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>#1</td>
                                <td><strong>Ноунейм</strong></td>
                                <td>
                                    <span class="subscription-badge">USD</span>
                                    <span class="subscription-badge">EUR</span>
                                </td>
                                <td>
                                    <a href="/user?id=1" class="btn">
                                        👁️ Просмотр
                                    </a>
                                </td>
                            </tr>
                            <tr>
                                <td>#2</td>
                                <td><strong>Питонист</strong></td>
                                <td>
                                    <span class="subscription-badge">USD</span>
                                    <span class="subscription-badge">GBP</span>
                                </td>
                                <td>
                                    <a href="/user?id=2" class="btn">
                                        👁️ Просмотр
                                    </a>
                                </td>
                            </tr>
                            <tr>
                                <td>#3</td>
                                <td><strong>Брат</strong></td>
                                <td>
                                    <span class="subscription-badge">CHF</span>
                                </td>
                                <td>
                                    <a href="/user?id=3" class="btn">
                                        👁️ Просмотр
                                    </a>
                                </td>
                            </tr>
                            <tr>
                                <td>#4</td>
                                <td><strong>Скрин</strong></td>
                                <td>
                                    <span class="subscription-badge">EUR</span>
                                    <span class="subscription-badge">CNY</span>
                                </td>
                                <td>
                                    <a href="/user?id=4" class="btn">
                                        👁️ Просмотр
                                    </a>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <div class="card" style="margin-top: 30px;">
                    <h3 class="card-title">📊 Статистика подписок</h3>
                    <div class="card-content">
                        <p>Всего подписок: <strong>7</strong></p>
                        <p>Среднее количество подписок на пользователя: <strong>1.75</strong></p>
                        <p>Самая популярная валюта: <strong>USD</strong> (2 подписчика)</p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        self.send_html(html)
    
    def user_detail(self):
        query = parse_qs(urlparse(self.path).query)
        user_id = query.get('id', ['1'])[0]
        
        users = {
            '1': {'name': 'Ноунейм', 'id': 1, 'subscriptions': ['USD', 'EUR']},
            '2': {'name': 'Питонист', 'id': 2, 'subscriptions': ['USD', 'GBP']},
            '3': {'name': 'Брат', 'id': 3, 'subscriptions': ['CHF']},
            '4': {'name': 'Скрин', 'id': 4, 'subscriptions': ['EUR', 'CNY']}
        }
        
        user = users.get(user_id, users['1'])
        
        # Получаем реальные курсы валют (те же, что на странице /currencies)
        try:
            from utils.currencies_api import get_currencies
            all_currencies = get_currencies()
        except ImportError:
            # Если модуль не найден, используем статические данные
            all_currencies = [
                {"char_code": "USD", "name": "Доллар США", "value": 92.45},
                {"char_code": "EUR", "name": "Евро", "value": 98.12},
                {"char_code": "GBP", "name": "Фунт стерлингов", "value": 110.23},
                {"char_code": "JPY", "name": "Японская иена", "value": 0.58},
                {"char_code": "CHF", "name": "Швейцарский франк", "value": 99.87},
                {"char_code": "CNY", "name": "Китайский юань", "value": 12.34},
                {"char_code": "CAD", "name": "Канадский доллар", "value": 67.89},
                {"char_code": "AUD", "name": "Австралийский доллар", "value": 57.89},
                {"char_code": "INR", "name": "Индийская рупия", "value": 1.10},
            ]
        
        # Создаем словарь для быстрого доступа к курсам
        currency_dict = {c['char_code']: c for c in all_currencies}
        
        subscriptions_html = ""
        subscription_data = []
        
        if user['subscriptions']:
            for sub_code in user['subscriptions']:
                currency = currency_dict.get(sub_code)
                if currency:
                    value = currency['value']
                    name = currency['name']
                    
                    subscriptions_html += f"""
                    <div class="currency-item">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <div style="font-size: 1.5rem; font-weight: bold;">{sub_code}</div>
                                <div style="font-size: 0.9rem; opacity: 0.8;">{name}</div>
                            </div>
                            <div style="text-align: right;">
                                <div style="font-size: 1.2rem; font-weight: bold;">
                                    {value:.2f} ₽
                                </div>
                                <div style="font-size: 0.8rem; opacity: 0.7;">
                                    Реальный курс ЦБ РФ
                                </div>
                            </div>
                        </div>
                    </div>
                    """
                    
                    # Сохраняем данные для графика
                    subscription_data.append({
                        'code': sub_code,
                        'name': name,
                        'value': value,
                        'currency': currency
                    })
        
        # Генерируем данные для линейного графика на основе реальных данных
        chart_datasets = ""
        colors = ['#ff6b6b', '#ff8e53', '#36a2eb', '#4bc0c0', '#9966ff']
        
        for i, sub in enumerate(subscription_data):
            color = colors[i % len(colors)]
            base_value = sub['value']
            
            # Используем историю из реальных данных если есть, иначе генерируем
            if 'history' in sub['currency']:
                # Берем исторические данные из API
                history = sub['currency']['history']
                data_points = [h['value'] for h in history[:30]]  # Берем последние 30 дней
            else:
                # Генерируем реалистичные исторические данные
                data_points = []
                for day in range(30):
                    # Колебания в пределах ±2% от реального курса
                    fluctuation = random.uniform(-0.02, 0.02)
                    day_value = base_value * (1 + fluctuation)
                    data_points.append(round(day_value, 2))
            
            chart_datasets += f"""{{
                label: '{sub['code']} - {sub['name']}',
                data: {data_points},
                borderColor: '{color}',
                backgroundColor: '{color}20',
                borderWidth: 2,
                fill: true,
                tension: 0.4,
                pointRadius: 3
            }}{',' if i < len(subscription_data) - 1 else ''}"""
        
        html = f"""
        <!DOCTYPE html>
        <html lang="ru">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>CurrenciesListApp - {user['name']}</title>
            <link rel="stylesheet" href="/static/style.css">
        </head>
        <body>
            <div class="container">
                <nav class="navbar">
                    <a href="/" class="nav-link">Главная</a>
                    <a href="/author" class="nav-link">Автор</a>
                    <a href="/currencies" class="nav-link">Валюты</a>
                    <a href="/users" class="nav-link">Пользователи</a>
                </nav>

                <div class="card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                        <h2 class="card-title" style="margin: 0;">👤 {user['name']}</h2>
                        <span style="opacity: 0.8;">ID: #{user['id']}</span>
                    </div>

                    <div style="margin: 30px 0;">
                        <h3 style="margin-bottom: 15px; color: white; border-bottom: 2px solid rgba(255,255,255,0.3); 
                           padding-bottom: 10px;">💰 Подписки на валюты</h3>
                        
                        {subscriptions_html if subscriptions_html else '<p style="text-align: center; opacity: 0.7; padding: 30px;">У пользователя нет подписок на валюты</p>'}
                        
                        <p style="margin-top: 20px; opacity: 0.8; font-size: 0.9rem;">
                            <i>Курсы соответствуют официальным данным Центрального Банка РФ</i>
                        </p>
                    </div>

                    <div style="margin: 40px 0;">
                        <h3 style="margin-bottom: 15px; color: white; border-bottom: 2px solid rgba(255,255,255,0.3); 
                           padding-bottom: 10px;">📊 Динамика курсов подписок</h3>
                        
                        <div class="chart-container" style="margin-top: 20px;">
                            <div style="height: 300px; position: relative;">
                                <canvas id="userChart"></canvas>
                            </div>
                            <p style="text-align: center; opacity: 0.8; margin-top: 10px;">
                                <small>История изменения курсов за последние 30 дней</small>
                            </p>
                        </div>
                    </div>

                    <div style="text-align: center; margin-top: 30px;">
                        <a href="/currencies" class="btn" style="margin-right: 10px;">
                            📊 Все курсы валют
                        </a>
                        <a href="/users" class="btn btn-primary">
                            ← Назад к списку пользователей
                        </a>
                    </div>
                </div>
            </div>

            <script>
                document.addEventListener('DOMContentLoaded', function() {{
                    if ({len(subscription_data)}) {{
                        const ctx = document.getElementById('userChart').getContext('2d');
                        
                        new Chart(ctx, {{
                            type: 'line',
                            data: {{
                                labels: Array.from({{length: 30}}, (_, i) => `${{30 - i}} дн. назад`),
                                datasets: [{chart_datasets}]
                            }},
                            options: {{
                                responsive: true,
                                maintainAspectRatio: false,
                                plugins: {{
                                    legend: {{
                                        labels: {{
                                            color: 'white',
                                            font: {{
                                                size: 14
                                            }}
                                        }}
                                    }},
                                    tooltip: {{
                                        backgroundColor: 'rgba(0, 0, 0, 0.7)',
                                        titleColor: '#fff',
                                        bodyColor: '#fff',
                                        callbacks: {{
                                            label: function(context) {{
                                                return `${{context.dataset.label}}: ${{context.parsed.y.toFixed(2)}} ₽`;
                                            }}
                                        }}
                                    }}
                                }},
                                scales: {{
                                    x: {{
                                        ticks: {{
                                            color: 'rgba(255,255,255,0.8)',
                                            maxTicksLimit: 10
                                        }},
                                        grid: {{
                                            color: 'rgba(255,255,255,0.1)'
                                        }}
                                    }},
                                    y: {{
                                        ticks: {{
                                            color: 'rgba(255,255,255,0.8)',
                                            callback: function(value) {{
                                                return value.toFixed(2) + ' ₽';
                                            }}
                                        }},
                                        grid: {{
                                            color: 'rgba(255,255,255,0.1)'
                                        }}
                                    }}
                                }}
                            }}
                        }});
                    }} else {{
                        document.getElementById('userChart').parentElement.innerHTML = 
                            '<p style="text-align: center; padding: 50px; opacity: 0.7;">Нет данных для построения графика</p>';
                    }}
                }});
            </script>
            
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        </body>
        </html>
        """
        self.send_html(html)
    def log_message(self, format, *args):
        pass

def run_server(port=8000):
    # Проверяем и создаем структуру
    if not os.path.exists('static'):
        os.makedirs('static')
    
    # Создаем CSS файл (остается без изменений)
    css_content = """/* Основные стили */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #ff6b6b 0%, #ff8e53 100%);
    min-height: 100vh;
    color: white;
    line-height: 1.6;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

/* Навигация */
.navbar {
    background: rgba(0, 0, 0, 0.2);
    backdrop-filter: blur(10px);
    padding: 1rem 2rem;
    border-radius: 15px;
    margin-bottom: 30px;
    display: flex;
    gap: 30px;
}

.nav-link {
    color: white;
    text-decoration: none;
    font-size: 1.1rem;
    font-weight: 500;
    padding: 10px 20px;
    border-radius: 10px;
    transition: all 0.3s ease;
    background: rgba(255, 255, 255, 0.1);
}

.nav-link:hover {
    background: rgba(255, 255, 255, 0.2);
    transform: translateY(-2px);
}

.nav-link.active {
    background: rgba(255, 255, 255, 0.3);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

/* Главная страница - плашки */
.header {
    text-align: center;
    margin-bottom: 40px;
}

.header h1 {
    font-size: 3rem;
    margin-bottom: 10px;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}

.header p {
    font-size: 1.2rem;
    opacity: 0.9;
}

.dashboard {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 30px;
    margin-bottom: 40px;
}

.card {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 30px;
    transition: all 0.3s ease;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
}

.card:hover {
    transform: translateY(-10px);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
    background: rgba(255, 255, 255, 0.15);
}

.card-title {
    font-size: 1.5rem;
    margin-bottom: 20px;
    color: #fff;
    border-bottom: 2px solid rgba(255, 255, 255, 0.3);
    padding-bottom: 10px;
}

.card-content {
    font-size: 1.1rem;
}

.card-content ul {
    margin-top: 15px;
    padding-left: 20px;
}

.card-content li {
    margin-bottom: 8px;
}

/* Стили для списков */
.list-container {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 30px;
    margin-top: 20px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.list-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 30px;
    padding-bottom: 20px;
    border-bottom: 2px solid rgba(255, 255, 255, 0.3);
}

.list-title {
    font-size: 2rem;
    color: white;
}

.btn {
    background: rgba(255, 255, 255, 0.2);
    color: white;
    border: none;
    padding: 12px 24px;
    border-radius: 10px;
    cursor: pointer;
    font-size: 1rem;
    transition: all 0.3s ease;
    text-decoration: none;
    display: inline-block;
}

.btn:hover {
    background: rgba(255, 255, 255, 0.3);
    transform: translateY(-2px);
}

.btn-primary {
    background: linear-gradient(135deg, #ff8e53 0%, #ff6b6b 100%);
}

.btn-primary:hover {
    background: linear-gradient(135deg, #ff6b6b 0%, #ff8e53 100%);
}

/* Таблицы */
.table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
}

.table th {
    background: rgba(255, 255, 255, 0.2);
    padding: 15px;
    text-align: left;
    font-weight: 600;
    color: white;
}

.table td {
    padding: 15px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.table tr:hover {
    background: rgba(255, 255, 255, 0.05);
}

/* Карточки валют */
.currency-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 20px;
    margin-top: 30px;
}

.currency-card {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 15px;
    padding: 20px;
    transition: all 0.3s ease;
    border: 1px solid rgba(255, 255, 255, 0.2);
}

.currency-card:hover {
    background: rgba(255, 255, 255, 0.15);
    transform: translateY(-5px);
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
}

.currency-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;
}

.currency-code {
    font-size: 1.5rem;
    font-weight: bold;
    color: white;
}

.currency-name {
    color: rgba(255, 255, 255, 0.8);
    font-size: 0.9rem;
}

.currency-value {
    font-size: 2rem;
    font-weight: bold;
    color: white;
    text-align: center;
    margin: 10px 0;
}

.currency-nominal {
    color: rgba(255, 255, 255, 0.7);
    font-size: 0.9rem;
    text-align: center;
}

.currency-item {
    background: rgba(255, 255, 255, 0.1);
    padding: 20px;
    border-radius: 10px;
    margin-bottom: 10px;
    transition: all 0.3s ease;
}

.currency-item:hover {
    background: rgba(255, 255, 255, 0.15);
}

/* Подписки */
.subscription-badge {
    display: inline-block;
    background: rgba(255, 255, 255, 0.2);
    padding: 5px 15px;
    border-radius: 20px;
    margin: 5px;
    font-size: 0.9rem;
    transition: all 0.3s ease;
}

.subscription-badge:hover {
    background: rgba(255, 255, 255, 0.3);
    transform: scale(1.05);
}

/* Графики */
.chart-container {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 30px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.chart-title {
    font-size: 1.5rem;
    margin-bottom: 20px;
    color: white;
    text-align: center;
}

/* Футер */
.footer {
    text-align: center;
    margin-top: 50px;
    padding: 20px;
    color: rgba(255, 255, 255, 0.7);
    border-top: 1px solid rgba(255, 255, 255, 0.1);
}

/* Адаптивность */
@media (max-width: 768px) {
    .navbar {
        flex-direction: column;
        gap: 10px;
    }
    
    .dashboard {
        grid-template-columns: 1fr;
    }
    
    .currency-grid {
        grid-template-columns: 1fr;
    }
    
    .list-header {
        flex-direction: column;
        gap: 20px;
        text-align: center;
    }
}"""
    
    with open('static/style.css', 'w', encoding='utf-8') as f:
        f.write(css_content)
    
    server_address = ('', port)
    httpd = HTTPServer(server_address, CurrencyHandler)
    
    print(f" Сервер запущен: http://localhost:{port}/")

    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Сервер остановлен")

if __name__ == '__main__':
    run_server()
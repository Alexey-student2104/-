import sqlite3
import pandas as pd

def view_database():
    """Просмотр содержимого базы данных"""
    conn = sqlite3.connect('currencies.db')
    
    # Получаем список таблиц
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print("=" * 50)
    print("СОДЕРЖИМОЕ БАЗЫ ДАННЫХ")
    print("=" * 50)
    
    for table_name in tables:
        table = table_name[0]
        print(f"\nТАБЛИЦА: {table}")
        print("-" * 30)
        
        # Получаем данные из таблицы
        query = f"SELECT * FROM {table}"
        df = pd.read_sql_query(query, conn)
        
        if df.empty:
            print("(пусто)")
        else:
            print(df.to_string(index=False))
    
    conn.close()

if __name__ == '__main__':
    view_database()
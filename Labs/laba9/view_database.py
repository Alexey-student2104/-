#!/usr/bin/env python3
"""
Скрипт для просмотра содержимого базы данных
"""

import sqlite3
import sys

def view_database():
    """Просмотр содержимого базы данных"""
    try:
        conn = sqlite3.connect('currencies.db')
        cursor = conn.cursor()
        
        print("=" * 60)
        print("СОДЕРЖИМОЕ БАЗЫ ДАННЫХ currencies.db")
        print("=" * 60)
        
        # Получаем список таблиц
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        for table_name in tables:
            table = table_name[0]
            print(f"\nТАБЛИЦА: {table}")
            print("-" * 40)
            
            # Получаем структуру таблицы
            cursor.execute(f"PRAGMA table_info({table})")
            columns = cursor.fetchall()
            print("Структура:")
            for col in columns:
                print(f"  {col[1]} ({col[2]})")
            
            # Получаем данные из таблицы
            cursor.execute(f"SELECT * FROM {table}")
            rows = cursor.fetchall()
            
            if rows:
                print(f"\nДанные ({len(rows)} записей):")
                for row in rows:
                    print(f"  {row}")
            else:
                print("\n(пусто)")
        
        conn.close()
        
    except sqlite3.Error as e:
        print(f"Ошибка при работе с базой данных: {e}")
        sys.exit(1)

if __name__ == '__main__':
    view_database()
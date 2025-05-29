#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль для работы с базой данных приложения "Служба доставки".
Содержит функции для инициализации БД и работы с данными посылок.
"""

import sqlite3
import os
from datetime import datetime

DB_NAME = "delivery_service.db"

def initialize_db():
    """Инициализация базы данных, создание необходимых таблиц если они не существуют"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Создание таблицы для посылок
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS packages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tracking_number TEXT UNIQUE NOT NULL,
        description TEXT,
        status TEXT NOT NULL,
        sender TEXT,
        recipient TEXT,
        sender_address TEXT,
        recipient_address TEXT,
        created_at TIMESTAMP
    )
    ''')
    
    # Создание таблицы для курьеров
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS couriers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT,
        email TEXT,
        status TEXT NOT NULL DEFAULT 'Активен',
        created_at TIMESTAMP
    )
    ''')
    
    # Создание таблицы для отзывов
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tracking_number TEXT,
        customer_name TEXT,
        rating INTEGER NOT NULL,
        comment TEXT,
        created_at TIMESTAMP,
        FOREIGN KEY (tracking_number) REFERENCES packages(tracking_number)
    )
    ''')
    
    conn.commit()
    conn.close()

def create_package(tracking_number, description, sender, recipient, sender_address="", recipient_address=""):
    """
    Добавление новой посылки в базу данных
    
    Args:
        tracking_number (str): Номер отслеживания
        description (str): Описание посылки
        sender (str): Отправитель
        recipient (str): Получатель
        sender_address (str): Адрес отправителя
        recipient_address (str): Адрес получателя
        
    Returns:
        bool: True если посылка успешно добавлена, False в случае ошибки
    """
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO packages (tracking_number, description, status, sender, recipient, sender_address, recipient_address, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (tracking_number, description, "Отправлена", sender, recipient, sender_address, recipient_address, datetime.now())
        )
        
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        # Если номер отслеживания уже существует
        return False
    except Exception as e:
        print(f"Ошибка при создании посылки: {e}")
        return False

def get_package_by_tracking(tracking_number):
    """
    Получение информации о посылке по номеру отслеживания
    
    Args:
        tracking_number (str): Номер отслеживания
        
    Returns:
        dict: Информация о посылке или None если посылка не найдена
    """
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row  # Чтобы получать словарь вместо кортежа
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM packages WHERE tracking_number = ?", (tracking_number,))
        package = cursor.fetchone()
        
        conn.close()
        
        if package:
            # Конвертация Row в dict
            return dict(package)
        return None
    except Exception as e:
        print(f"Ошибка при получении данных посылки: {e}")
        return None

def update_package_status(tracking_number, new_status):
    """
    Обновление статуса посылки
    
    Args:
        tracking_number (str): Номер отслеживания
        new_status (str): Новый статус посылки
        
    Returns:
        bool: True если статус успешно обновлен, False в случае ошибки
    """
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE packages SET status = ? WHERE tracking_number = ?",
            (new_status, tracking_number)
        )
        
        success = cursor.rowcount > 0
        
        conn.commit()
        conn.close()
        
        return success
    except Exception as e:
        print(f"Ошибка при обновлении статуса посылки: {e}")
        return False

# Функции для работы с курьерами
def create_courier(name, phone, email):
    """
    Добавление нового курьера в базу данных
    
    Args:
        name (str): Имя курьера
        phone (str): Телефон курьера
        email (str): Email курьера
        
    Returns:
        bool: True если курьер успешно добавлен, False в случае ошибки
    """
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO couriers (name, phone, email, created_at) VALUES (?, ?, ?, ?)",
            (name, phone, email, datetime.now())
        )
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Ошибка при добавлении курьера: {e}")
        return False

def get_all_couriers():
    """
    Получение списка всех курьеров
    
    Returns:
        list: Список курьеров или пустой список в случае ошибки
    """
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM couriers ORDER BY name")
        couriers = cursor.fetchall()
        
        conn.close()
        
        return [dict(courier) for courier in couriers]
    except Exception as e:
        print(f"Ошибка при получении списка курьеров: {e}")
        return []

def delete_courier(courier_id):
    """
    Удаление курьера из базы данных
    
    Args:
        courier_id (int): ID курьера
        
    Returns:
        bool: True если курьер успешно удален, False в случае ошибки
    """
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM couriers WHERE id = ?", (courier_id,))
        
        success = cursor.rowcount > 0
        
        conn.commit()
        conn.close()
        
        return success
    except Exception as e:
        print(f"Ошибка при удалении курьера: {e}")
        return False

# Функции для работы с отзывами
def create_review(tracking_number, customer_name, rating, comment):
    """
    Добавление нового отзыва в базу данных
    
    Args:
        tracking_number (str): Номер отслеживания
        customer_name (str): Имя клиента
        rating (int): Рейтинг (1-5)
        comment (str): Комментарий
        
    Returns:
        bool: True если отзыв успешно добавлен, False в случае ошибки
    """
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO reviews (tracking_number, customer_name, rating, comment, created_at) VALUES (?, ?, ?, ?, ?)",
            (tracking_number, customer_name, rating, comment, datetime.now())
        )
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Ошибка при добавлении отзыва: {e}")
        return False

def get_all_reviews():
    """
    Получение списка всех отзывов
    
    Returns:
        list: Список отзывов или пустой список в случае ошибки
    """
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM reviews ORDER BY created_at DESC")
        reviews = cursor.fetchall()
        
        conn.close()
        
        return [dict(review) for review in reviews]
    except Exception as e:
        print(f"Ошибка при получении списка отзывов: {e}")
        return []

def get_all_packages():
    """
    Получение списка всех посылок
    
    Returns:
        list: Список посылок или пустой список в случае ошибки
    """
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM packages ORDER BY created_at DESC")
        packages = cursor.fetchall()
        
        conn.close()
        
        return [dict(package) for package in packages]
    except Exception as e:
        print(f"Ошибка при получении списка посылок: {e}")
        return []

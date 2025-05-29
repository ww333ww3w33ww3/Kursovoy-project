#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Модуль сервиса посылок для приложения "Служба доставки".
Содержит бизнес-логику для работы с посылками.
"""

import random
import string
from database import (create_package, get_package_by_tracking, update_package_status,
                     create_courier, get_all_couriers, delete_courier,
                     create_review, get_all_reviews)

def generate_tracking_number():
    """
    Генерация уникального номера отслеживания посылки
    
    Returns:
        str: Номер отслеживания в формате XX-999999
    """
    letters = ''.join(random.choices(string.ascii_uppercase, k=2))
    numbers = ''.join(random.choices(string.digits, k=6))
    return f"{letters}-{numbers}"

def send_package(description, sender, recipient, sender_address="", recipient_address=""):
    """
    Отправка новой посылки
    
    Args:
        description (str): Описание посылки
        sender (str): Отправитель
        recipient (str): Получатель
        sender_address (str): Адрес отправителя
        recipient_address (str): Адрес получателя
        
    Returns:
        tuple: (успех, номер_отслеживания/сообщение_об_ошибке)
    """
    if not description or not sender or not recipient:
        return False, "Заполните все обязательные поля"
    
    # Генерация уникального номера отслеживания
    tracking_number = generate_tracking_number()
    
    # Попытка создать посылку в БД
    success = create_package(tracking_number, description, sender, recipient, sender_address, recipient_address)
    
    if success:
        return True, tracking_number
    else:
        # Редкий случай коллизии номера отслеживания
        return False, "Ошибка при создании посылки. Пожалуйста, попробуйте еще раз."

def track_package(tracking_number):
    """
    Отслеживание посылки по номеру
    
    Args:
        tracking_number (str): Номер отслеживания
        
    Returns:
        tuple: (успех, информация_о_посылке/сообщение_об_ошибке)
    """
    if not tracking_number:
        return False, "Введите номер отслеживания"
    
    package_info = get_package_by_tracking(tracking_number)
    
    if package_info:
        return True, package_info
    else:
        return False, "Посылка с таким номером не найдена"

def update_status(tracking_number, new_status):
    """
    Обновление статуса посылки
    
    Args:
        tracking_number (str): Номер отслеживания
        new_status (str): Новый статус
        
    Returns:
        bool: True если статус успешно обновлен
    """
    return update_package_status(tracking_number, new_status)

# Функции для работы с курьерами
def add_courier(name, phone, email):
    """
    Добавление нового курьера
    
    Args:
        name (str): Имя курьера
        phone (str): Телефон курьера
        email (str): Email курьера
        
    Returns:
        tuple: (успех, сообщение)
    """
    if not name:
        return False, "Имя курьера обязательно для заполнения"
    
    success = create_courier(name, phone, email)
    
    if success:
        return True, "Курьер успешно добавлен"
    else:
        return False, "Ошибка при добавлении курьера"

def get_couriers():
    """
    Получение списка всех курьеров
    
    Returns:
        list: Список курьеров
    """
    return get_all_couriers()

def remove_courier(courier_id):
    """
    Удаление курьера
    
    Args:
        courier_id (int): ID курьера
        
    Returns:
        tuple: (успех, сообщение)
    """
    success = delete_courier(courier_id)
    
    if success:
        return True, "Курьер успешно удален"
    else:
        return False, "Ошибка при удалении курьера или курьер не найден"

# Функции для работы с отзывами
def add_review(tracking_number, customer_name, rating, comment):
    """
    Добавление нового отзыва
    
    Args:
        tracking_number (str): Номер отслеживания
        customer_name (str): Имя клиента
        rating (int): Рейтинг (1-5)
        comment (str): Комментарий
        
    Returns:
        tuple: (успех, сообщение)
    """
    if not customer_name or not rating:
        return False, "Имя клиента и рейтинг обязательны для заполнения"
    
    if not (1 <= rating <= 5):
        return False, "Рейтинг должен быть от 1 до 5"
    
    success = create_review(tracking_number, customer_name, rating, comment)
    
    if success:
        return True, "Отзыв успешно добавлен"
    else:
        return False, "Ошибка при добавлении отзыва"

def get_reviews():
    """
    Получение списка всех отзывов
    
    Returns:
        list: Список отзывов
    """
    return get_all_reviews()

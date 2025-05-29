#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Главный исполняемый файл приложения "Служба доставки".
Запускает основной интерфейс приложения.
"""

import tkinter as tk
from database import initialize_db
from gui import DeliveryServiceApp

def main():
    """Основная функция запуска приложения"""
    # Инициализация базы данных
    initialize_db()
    
    # Создание и запуск GUI приложения
    root = tk.Tk()
    app = DeliveryServiceApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

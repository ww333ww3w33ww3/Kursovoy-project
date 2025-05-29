#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Графический интерфейс пользователя для приложения "Служба доставки".
Реализует окна и виджеты для взаимодействия пользователя с приложением.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import package_service

# Определение цветовой схемы
COLORS = {
    "dark_red": "#8B0000",    # Темно-красный (бордовый)
    "red": "#B22222",         # Огненно-красный
    "light_red": "#CD5C5C",   # Светло-красный
    "bg_color": "#FFEBEE",    # Светло-розовый фон
    "text_color": "#2E0000",  # Очень темно-красный для текста
    "button_bg": "#C62828",   # Темно-красный для кнопок
    "button_fg": "#FFFFFF",   # Белый текст на кнопках
}

class DeliveryServiceApp:
    """Класс основного приложения службы доставки"""
    
    def __init__(self, root):
        """
        Инициализация главного окна приложения
        
        Args:
            root (tk.Tk): Корневой виджет tkinter
        """
        self.root = root
        self.root.title("Служба доставки")
        self.root.geometry("800x600")
        self.root.minsize(640, 480)
        
        # Настройка стилей
        self.setup_styles()
        
        # Создание главного меню
        self.create_main_menu()
        
        # Создание вкладок
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Создание вкладки для отправки посылки
        self.send_frame = ttk.Frame(self.notebook, style="TFrame")
        self.notebook.add(self.send_frame, text="Отправить посылку")
        self.setup_send_frame()
        
        # Создание вкладки для отслеживания посылки
        self.track_frame = ttk.Frame(self.notebook, style="TFrame")
        self.notebook.add(self.track_frame, text="Отследить посылку")
        self.setup_track_frame()
        
        # Создание вкладки для отзывов
        self.review_frame = ttk.Frame(self.notebook, style="TFrame")
        self.notebook.add(self.review_frame, text="Отзывы")
        self.setup_review_frame()
        
        # Создание вкладки для управления курьерами
        self.courier_frame = ttk.Frame(self.notebook, style="TFrame")
        self.notebook.add(self.courier_frame, text="Курьеры")
        self.setup_courier_frame()
        
        # Создание вкладки для карты доставки
        self.map_frame = ttk.Frame(self.notebook, style="TFrame")
        self.notebook.add(self.map_frame, text="Карта и адреса")
        self.setup_map_frame()
        
        # Статусная строка
        self.status_var = tk.StringVar()
        self.status_var.set("Готово к работе")
        status_bar = ttk.Label(
            self.root, 
            textvariable=self.status_var, 
            relief=tk.SUNKEN, 
            anchor=tk.W
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def setup_styles(self):
        """Настройка стилей для виджетов"""
        style = ttk.Style()
        
        # Основные стили
        style.configure("TFrame", background=COLORS["bg_color"])
        style.configure("TLabel", background=COLORS["bg_color"], foreground=COLORS["text_color"], font=("Arial", 10))
        style.configure("TEntry", background=COLORS["bg_color"], foreground=COLORS["text_color"])
        style.configure("TButton", 
                        background=COLORS["button_bg"], 
                        foreground=COLORS["button_fg"], 
                        font=("Arial", 10, "bold"))
        
        # Стиль для заголовков
        style.configure("Heading.TLabel", 
                        font=("Arial", 16, "bold"), 
                        foreground=COLORS["dark_red"], 
                        background=COLORS["bg_color"])
        
        # Стиль для подзаголовков
        style.configure("Subheading.TLabel", 
                        font=("Arial", 12, "bold"), 
                        foreground=COLORS["red"], 
                        background=COLORS["bg_color"])
        
        # Настройка вкладок
        style.configure("TNotebook", background=COLORS["bg_color"])
        style.configure("TNotebook.Tab", 
                        font=("Arial", 10, "bold"), 
                        padding=[10, 4], 
                        background=COLORS["light_red"], 
                        foreground=COLORS["text_color"])
        style.map("TNotebook.Tab", 
                  background=[("selected", COLORS["dark_red"])],
                  foreground=[("selected", "white")])
    
    def create_main_menu(self):
        """Создание главного меню приложения"""
        menubar = tk.Menu(self.root)
        
        # Меню "Файл"
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Выход", command=self.root.quit)
        menubar.add_cascade(label="Файл", menu=file_menu)
        
        # Меню "Справка"
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="О программе", command=self.show_about)
        menubar.add_cascade(label="Справка", menu=help_menu)
        
        self.root.config(menu=menubar)
    
    def setup_send_frame(self):
        """Настройка фрейма для отправки посылки"""
        # Заголовок
        header = ttk.Label(self.send_frame, text="Отправка посылки", style="Heading.TLabel")
        header.pack(pady=(20, 10))
        
        # Форма отправки
        form_frame = ttk.Frame(self.send_frame, style="TFrame")
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Отправитель
        sender_label = ttk.Label(form_frame, text="Отправитель:", style="TLabel")
        sender_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        self.sender_entry = ttk.Entry(form_frame, width=40)
        self.sender_entry.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Получатель
        recipient_label = ttk.Label(form_frame, text="Получатель:", style="TLabel")
        recipient_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        self.recipient_entry = ttk.Entry(form_frame, width=40)
        self.recipient_entry.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Адрес отправителя
        sender_address_label = ttk.Label(form_frame, text="Адрес отправителя:", style="TLabel")
        sender_address_label.grid(row=2, column=0, sticky=tk.W, pady=5)
        self.sender_address_entry = ttk.Entry(form_frame, width=40)
        self.sender_address_entry.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Адрес получателя
        recipient_address_label = ttk.Label(form_frame, text="Адрес получателя:", style="TLabel")
        recipient_address_label.grid(row=3, column=0, sticky=tk.W, pady=5)
        self.recipient_address_entry = ttk.Entry(form_frame, width=40)
        self.recipient_address_entry.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Описание посылки
        description_label = ttk.Label(form_frame, text="Описание посылки:", style="TLabel")
        description_label.grid(row=4, column=0, sticky=tk.W, pady=5)
        self.description_text = scrolledtext.ScrolledText(form_frame, width=30, height=4, wrap=tk.WORD)
        self.description_text.grid(row=4, column=1, sticky=tk.W+tk.E, pady=5)
        
        # Кнопка отправки
        send_button = tk.Button(
            form_frame, 
            text="Отправить", 
            command=self.send_package,
            bg=COLORS["button_bg"],
            fg=COLORS["button_fg"],
            font=("Arial", 10, "bold"),
            padx=20,
            pady=8,
            relief=tk.RAISED,
            cursor="hand2"
        )
        send_button.grid(row=4, column=1, sticky=tk.E, pady=20)
        
        # Результат отправки
        result_frame = ttk.Frame(self.send_frame, style="TFrame")
        result_frame.pack(fill=tk.X, padx=20, pady=10)
        
        result_label = ttk.Label(result_frame, text="Результат отправки:", style="Subheading.TLabel")
        result_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.result_var = tk.StringVar()
        self.result_var.set("Здесь будет показан результат отправки посылки")
        result_text = ttk.Label(result_frame, textvariable=self.result_var, style="TLabel")
        result_text.pack(anchor=tk.W, pady=5)
    
    def setup_track_frame(self):
        """Настройка фрейма для отслеживания посылки"""
        # Заголовок
        header = ttk.Label(self.track_frame, text="Отслеживание посылки", style="Heading.TLabel")
        header.pack(pady=(20, 10))
        
        # Форма отслеживания
        form_frame = ttk.Frame(self.track_frame, style="TFrame")
        form_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Номер отслеживания
        tracking_label = ttk.Label(form_frame, text="Номер отслеживания:", style="TLabel")
        tracking_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        self.tracking_entry = ttk.Entry(form_frame, width=40)
        self.tracking_entry.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Кнопка отслеживания
        track_button = tk.Button(
            form_frame, 
            text="Отследить", 
            command=self.track_package,
            bg=COLORS["button_bg"],
            fg=COLORS["button_fg"],
            font=("Arial", 10, "bold"),
            padx=20,
            pady=8,
            relief=tk.RAISED,
            cursor="hand2"
        )
        track_button.grid(row=0, column=2, sticky=tk.W, padx=10, pady=5)
        
        # Информация о посылке
        info_frame = ttk.Frame(self.track_frame, style="TFrame")
        info_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        info_label = ttk.Label(info_frame, text="Информация о посылке:", style="Subheading.TLabel")
        info_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Поля информации
        self.info_frame = ttk.Frame(info_frame, style="TFrame")
        self.info_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Статус посылки
        self.status_label = ttk.Label(self.info_frame, text="Статус: Информация не найдена", style="TLabel")
        self.status_label.pack(anchor=tk.W, pady=2)
        
        # Отправитель
        self.sender_label = ttk.Label(self.info_frame, text="Отправитель: Информация не найдена", style="TLabel")
        self.sender_label.pack(anchor=tk.W, pady=2)
        
        # Получатель
        self.recipient_label = ttk.Label(self.info_frame, text="Получатель: Информация не найдена", style="TLabel")
        self.recipient_label.pack(anchor=tk.W, pady=2)
        
        # Описание
        self.description_label = ttk.Label(self.info_frame, text="Описание:", style="TLabel")
        self.description_label.pack(anchor=tk.W, pady=2)
        
        self.description_info = scrolledtext.ScrolledText(self.info_frame, width=40, height=4, wrap=tk.WORD)
        self.description_info.pack(fill=tk.X, pady=5)
        self.description_info.insert(tk.END, "Информация не найдена")
        self.description_info.config(state=tk.DISABLED)
        
        # Дата отправки
        self.date_label = ttk.Label(self.info_frame, text="Дата отправки: Информация не найдена", style="TLabel")
        self.date_label.pack(anchor=tk.W, pady=2)
    
    def send_package(self):
        """Обработчик отправки посылки"""
        sender = self.sender_entry.get().strip()
        recipient = self.recipient_entry.get().strip()
        sender_address = self.sender_address_entry.get().strip()
        recipient_address = self.recipient_address_entry.get().strip()
        description = self.description_text.get("1.0", tk.END).strip()
        
        # Проверка на заполнение полей
        if not sender or not recipient or not description:
            messagebox.showerror("Ошибка", "Пожалуйста, заполните все обязательные поля.")
            return
        
        # Отправка посылки через сервис
        success, result = package_service.send_package(description, sender, recipient, sender_address, recipient_address)
        
        if success:
            self.result_var.set(f"Посылка успешно отправлена!\nНомер для отслеживания: {result}")
            self.status_var.set(f"Посылка отправлена. Номер: {result}")
            
            # Очистка полей формы
            self.sender_entry.delete(0, tk.END)
            self.recipient_entry.delete(0, tk.END)
            self.sender_address_entry.delete(0, tk.END)
            self.recipient_address_entry.delete(0, tk.END)
            self.description_text.delete("1.0", tk.END)
            
            messagebox.showinfo("Успех", f"Посылка успешно отправлена!\nНомер для отслеживания: {result}")
        else:
            self.result_var.set(f"Ошибка при отправке посылки: {result}")
            self.status_var.set("Ошибка при отправке посылки")
            messagebox.showerror("Ошибка", result)
    
    def track_package(self):
        """Обработчик отслеживания посылки"""
        tracking_number = self.tracking_entry.get().strip()
        
        if not tracking_number:
            messagebox.showerror("Ошибка", "Пожалуйста, введите номер отслеживания.")
            return
        
        # Получение информации о посылке через сервис
        success, result = package_service.track_package(tracking_number)
        
        if success and isinstance(result, dict):
            # Безопасное получение данных из словаря
            status = result.get('status', 'Не указано')
            sender = result.get('sender', 'Не указано')
            recipient = result.get('recipient', 'Не указано')
            description = result.get('description', 'Не указано')
            created_at = result.get('created_at', 'Не указано')
            
            # Обновление информации в интерфейсе
            self.status_label.config(text=f"Статус: {status}")
            self.sender_label.config(text=f"Отправитель: {sender}")
            self.recipient_label.config(text=f"Получатель: {recipient}")
            
            # Обновление описания в text widget
            self.description_info.config(state=tk.NORMAL)
            self.description_info.delete("1.0", tk.END)
            self.description_info.insert(tk.END, description)
            self.description_info.config(state=tk.DISABLED)
            
            # Форматирование даты отправки
            if created_at != 'Не указано':
                date_str = created_at.split('.')[0] if '.' in created_at else created_at
            else:
                date_str = created_at
            self.date_label.config(text=f"Дата отправки: {date_str}")
            
            self.status_var.set(f"Посылка {tracking_number} отслежена. Статус: {status}")
        else:
            # Сброс информации при ошибке
            self.status_label.config(text="Статус: Информация не найдена")
            self.sender_label.config(text="Отправитель: Информация не найдена")
            self.recipient_label.config(text="Получатель: Информация не найдена")
            
            self.description_info.config(state=tk.NORMAL)
            self.description_info.delete("1.0", tk.END)
            self.description_info.insert(tk.END, "Информация не найдена")
            self.description_info.config(state=tk.DISABLED)
            
            self.date_label.config(text="Дата отправки: Информация не найдена")
            
            self.status_var.set(f"Ошибка при отслеживании посылки {tracking_number}")
            
            if isinstance(result, str):
                messagebox.showerror("Ошибка", result)
            else:
                messagebox.showerror("Ошибка", "Посылка с таким номером не найдена")
    
    def setup_review_frame(self):
        """Настройка фрейма для отзывов"""
        # Заголовок
        header = ttk.Label(self.review_frame, text="Отзывы клиентов", style="Heading.TLabel")
        header.pack(pady=(20, 10))
        
        # Фрейм для добавления отзыва
        add_review_frame = tk.LabelFrame(self.review_frame, text="Добавить отзыв", 
                                       bg=COLORS["bg_color"], fg=COLORS["text_color"], 
                                       font=("Arial", 10, "bold"))
        add_review_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Номер отслеживания (необязательный)
        tracking_label = ttk.Label(add_review_frame, text="Номер отслеживания (необязательно):", style="TLabel")
        tracking_label.grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)
        self.review_tracking_entry = ttk.Entry(add_review_frame, width=30)
        self.review_tracking_entry.grid(row=0, column=1, sticky=tk.W, pady=5, padx=5)
        
        # Имя клиента
        customer_label = ttk.Label(add_review_frame, text="Ваше имя:", style="TLabel")
        customer_label.grid(row=1, column=0, sticky=tk.W, pady=5, padx=5)
        self.customer_name_entry = ttk.Entry(add_review_frame, width=30)
        self.customer_name_entry.grid(row=1, column=1, sticky=tk.W, pady=5, padx=5)
        
        # Рейтинг
        rating_label = ttk.Label(add_review_frame, text="Рейтинг (1-5):", style="TLabel")
        rating_label.grid(row=2, column=0, sticky=tk.W, pady=5, padx=5)
        self.rating_var = tk.StringVar(value="5")
        rating_combo = ttk.Combobox(add_review_frame, textvariable=self.rating_var, values=["1", "2", "3", "4", "5"], state="readonly", width=10)
        rating_combo.grid(row=2, column=1, sticky=tk.W, pady=5, padx=5)
        
        # Комментарий
        comment_label = ttk.Label(add_review_frame, text="Комментарий:", style="TLabel")
        comment_label.grid(row=3, column=0, sticky=tk.NW, pady=5, padx=5)
        self.review_comment_text = scrolledtext.ScrolledText(add_review_frame, width=40, height=4, wrap=tk.WORD)
        self.review_comment_text.grid(row=3, column=1, sticky=tk.W+tk.E, pady=5, padx=5)
        
        # Кнопка добавления отзыва
        add_review_button = tk.Button(
            add_review_frame,
            text="Добавить отзыв",
            command=self.add_review,
            bg=COLORS["button_bg"],
            fg=COLORS["button_fg"],
            font=("Arial", 10, "bold"),
            padx=15,
            pady=5,
            relief=tk.RAISED,
            cursor="hand2"
        )
        add_review_button.grid(row=4, column=1, sticky=tk.E, pady=10, padx=5)
        
        # Список отзывов
        reviews_label = ttk.Label(self.review_frame, text="Все отзывы:", style="Subheading.TLabel")
        reviews_label.pack(anchor=tk.W, padx=20, pady=(10, 5))
        
        # Фрейм со скроллом для отзывов
        reviews_scroll_frame = tk.Frame(self.review_frame)
        reviews_scroll_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.reviews_listbox = tk.Listbox(reviews_scroll_frame, height=10, font=("Arial", 9))
        scrollbar_reviews = tk.Scrollbar(reviews_scroll_frame, orient=tk.VERTICAL, command=self.reviews_listbox.yview)
        self.reviews_listbox.config(yscrollcommand=scrollbar_reviews.set)
        
        self.reviews_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_reviews.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Кнопка обновления списка отзывов
        refresh_reviews_button = tk.Button(
            self.review_frame,
            text="Обновить список",
            command=self.refresh_reviews,
            bg=COLORS["button_bg"],
            fg=COLORS["button_fg"],
            font=("Arial", 10, "bold"),
            padx=15,
            pady=5,
            relief=tk.RAISED,
            cursor="hand2"
        )
        refresh_reviews_button.pack(pady=10)
        
        # Загрузка отзывов при инициализации
        self.refresh_reviews()
    
    def setup_courier_frame(self):
        """Настройка фрейма для управления курьерами"""
        # Заголовок
        header = ttk.Label(self.courier_frame, text="Управление курьерами", style="Heading.TLabel")
        header.pack(pady=(20, 10))
        
        # Фрейм для добавления курьера
        add_courier_frame = tk.LabelFrame(self.courier_frame, text="Добавить курьера", 
                                        bg=COLORS["bg_color"], fg=COLORS["text_color"], 
                                        font=("Arial", 10, "bold"))
        add_courier_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Имя курьера
        name_label = ttk.Label(add_courier_frame, text="Имя курьера:", style="TLabel")
        name_label.grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)
        self.courier_name_entry = ttk.Entry(add_courier_frame, width=30)
        self.courier_name_entry.grid(row=0, column=1, sticky=tk.W, pady=5, padx=5)
        
        # Телефон
        phone_label = ttk.Label(add_courier_frame, text="Телефон:", style="TLabel")
        phone_label.grid(row=1, column=0, sticky=tk.W, pady=5, padx=5)
        self.courier_phone_entry = ttk.Entry(add_courier_frame, width=30)
        self.courier_phone_entry.grid(row=1, column=1, sticky=tk.W, pady=5, padx=5)
        
        # Email
        email_label = ttk.Label(add_courier_frame, text="Email:", style="TLabel")
        email_label.grid(row=2, column=0, sticky=tk.W, pady=5, padx=5)
        self.courier_email_entry = ttk.Entry(add_courier_frame, width=30)
        self.courier_email_entry.grid(row=2, column=1, sticky=tk.W, pady=5, padx=5)
        
        # Кнопка добавления курьера
        add_courier_button = tk.Button(
            add_courier_frame,
            text="Добавить курьера",
            command=self.add_courier,
            bg=COLORS["button_bg"],
            fg=COLORS["button_fg"],
            font=("Arial", 10, "bold"),
            padx=15,
            pady=5,
            relief=tk.RAISED,
            cursor="hand2"
        )
        add_courier_button.grid(row=3, column=1, sticky=tk.E, pady=10, padx=5)
        
        # Список курьеров
        couriers_label = ttk.Label(self.courier_frame, text="Список курьеров:", style="Subheading.TLabel")
        couriers_label.pack(anchor=tk.W, padx=20, pady=(10, 5))
        
        # Фрейм со скроллом для курьеров
        couriers_scroll_frame = tk.Frame(self.courier_frame)
        couriers_scroll_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.couriers_listbox = tk.Listbox(couriers_scroll_frame, height=8, font=("Arial", 9))
        scrollbar_couriers = tk.Scrollbar(couriers_scroll_frame, orient=tk.VERTICAL, command=self.couriers_listbox.yview)
        self.couriers_listbox.config(yscrollcommand=scrollbar_couriers.set)
        
        self.couriers_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_couriers.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Кнопки управления курьерами
        buttons_frame = tk.Frame(self.courier_frame)
        buttons_frame.pack(pady=10)
        
        refresh_couriers_button = tk.Button(
            buttons_frame,
            text="Обновить список",
            command=self.refresh_couriers,
            bg=COLORS["button_bg"],
            fg=COLORS["button_fg"],
            font=("Arial", 10, "bold"),
            padx=15,
            pady=5,
            relief=tk.RAISED,
            cursor="hand2"
        )
        refresh_couriers_button.pack(side=tk.LEFT, padx=5)
        
        delete_courier_button = tk.Button(
            buttons_frame,
            text="Удалить выбранного",
            command=self.delete_courier,
            bg=COLORS["dark_red"],
            fg=COLORS["button_fg"],
            font=("Arial", 10, "bold"),
            padx=15,
            pady=5,
            relief=tk.RAISED,
            cursor="hand2"
        )
        delete_courier_button.pack(side=tk.LEFT, padx=5)
        
        # Загрузка курьеров при инициализации
        self.refresh_couriers()
    
    def add_review(self):
        """Обработчик добавления отзыва"""
        tracking_number = self.review_tracking_entry.get().strip()
        customer_name = self.customer_name_entry.get().strip()
        rating = int(self.rating_var.get())
        comment = self.review_comment_text.get("1.0", tk.END).strip()
        
        if not customer_name:
            messagebox.showerror("Ошибка", "Пожалуйста, введите ваше имя.")
            return
        
        # Добавление отзыва через сервис
        success, result = package_service.add_review(tracking_number, customer_name, rating, comment)
        
        if success:
            self.status_var.set("Отзыв успешно добавлен")
            
            # Очистка полей формы
            self.review_tracking_entry.delete(0, tk.END)
            self.customer_name_entry.delete(0, tk.END)
            self.rating_var.set("5")
            self.review_comment_text.delete("1.0", tk.END)
            
            # Обновление списка отзывов
            self.refresh_reviews()
            
            messagebox.showinfo("Успех", result)
        else:
            self.status_var.set("Ошибка при добавлении отзыва")
            messagebox.showerror("Ошибка", result)
    
    def refresh_reviews(self):
        """Обновление списка отзывов"""
        self.reviews_listbox.delete(0, tk.END)
        reviews = package_service.get_reviews()
        
        for review in reviews:
            rating_stars = "★" * review['rating'] + "☆" * (5 - review['rating'])
            tracking_text = f" (Посылка: {review['tracking_number']})" if review['tracking_number'] else ""
            date_str = review['created_at'].split('.')[0] if '.' in review['created_at'] else review['created_at']
            
            review_text = f"{rating_stars} {review['customer_name']}{tracking_text} - {date_str}"
            if review['comment']:
                review_text += f"\n   {review['comment'][:60]}{'...' if len(review['comment']) > 60 else ''}"
            
            self.reviews_listbox.insert(tk.END, review_text)
    
    def add_courier(self):
        """Обработчик добавления курьера"""
        name = self.courier_name_entry.get().strip()
        phone = self.courier_phone_entry.get().strip()
        email = self.courier_email_entry.get().strip()
        
        if not name:
            messagebox.showerror("Ошибка", "Пожалуйста, введите имя курьера.")
            return
        
        # Добавление курьера через сервис
        success, result = package_service.add_courier(name, phone, email)
        
        if success:
            self.status_var.set("Курьер успешно добавлен")
            
            # Очистка полей формы
            self.courier_name_entry.delete(0, tk.END)
            self.courier_phone_entry.delete(0, tk.END)
            self.courier_email_entry.delete(0, tk.END)
            
            # Обновление списка курьеров
            self.refresh_couriers()
            
            messagebox.showinfo("Успех", result)
        else:
            self.status_var.set("Ошибка при добавлении курьера")
            messagebox.showerror("Ошибка", result)
    
    def refresh_couriers(self):
        """Обновление списка курьеров"""
        self.couriers_listbox.delete(0, tk.END)
        couriers = package_service.get_couriers()
        
        for courier in couriers:
            courier_text = f"ID: {courier['id']} | {courier['name']}"
            if courier['phone']:
                courier_text += f" | Тел: {courier['phone']}"
            if courier['email']:
                courier_text += f" | Email: {courier['email']}"
            
            self.couriers_listbox.insert(tk.END, courier_text)
    
    def delete_courier(self):
        """Обработчик удаления курьера"""
        selection = self.couriers_listbox.curselection()
        
        if not selection:
            messagebox.showerror("Ошибка", "Пожалуйста, выберите курьера для удаления.")
            return
        
        # Получение ID курьера из выбранной строки
        selected_text = self.couriers_listbox.get(selection[0])
        courier_id = int(selected_text.split(" | ")[0].replace("ID: ", ""))
        
        # Подтверждение удаления
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить этого курьера?"):
            success, result = package_service.remove_courier(courier_id)
            
            if success:
                self.status_var.set("Курьер успешно удален")
                self.refresh_couriers()
                messagebox.showinfo("Успех", result)
            else:
                self.status_var.set("Ошибка при удалении курьера")
                messagebox.showerror("Ошибка", result)

    def setup_map_frame(self):
        """Настройка фрейма для карты доставки"""
        # Заголовок
        header = ttk.Label(self.map_frame, text="Карта и адреса", style="Heading.TLabel")
        header.pack(pady=(20, 10))
        
        # Простая форма для поиска адреса
        search_frame = tk.LabelFrame(self.map_frame, text="Найти адрес на карте", 
                                   bg=COLORS["bg_color"], fg=COLORS["text_color"], 
                                   font=("Arial", 10, "bold"))
        search_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Поле для ввода адреса
        address_label = ttk.Label(search_frame, text="Введите адрес:", style="TLabel")
        address_label.grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)
        self.address_entry = ttk.Entry(search_frame, width=40)
        self.address_entry.grid(row=0, column=1, sticky=tk.W, pady=5, padx=5)
        
        # Кнопка поиска на карте
        search_button = tk.Button(
            search_frame,
            text="Найти на карте",
            command=self.search_address,
            bg=COLORS["button_bg"],
            fg=COLORS["button_fg"],
            font=("Arial", 10, "bold"),
            padx=15,
            pady=5,
            relief=tk.RAISED,
            cursor="hand2"
        )
        search_button.grid(row=0, column=2, sticky=tk.W, padx=10, pady=5)
        
        # Информация об адресах посылок
        packages_frame = tk.LabelFrame(self.map_frame, text="Адреса посылок", 
                                     bg=COLORS["bg_color"], fg=COLORS["text_color"], 
                                     font=("Arial", 10, "bold"))
        packages_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Список посылок с адресами
        self.packages_listbox = tk.Listbox(packages_frame, height=8, font=("Arial", 9))
        scrollbar_packages = tk.Scrollbar(packages_frame, orient=tk.VERTICAL, command=self.packages_listbox.yview)
        self.packages_listbox.config(yscrollcommand=scrollbar_packages.set)
        
        self.packages_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar_packages.pack(side=tk.RIGHT, fill=tk.Y, pady=10)
        
        # Кнопки
        buttons_frame = tk.Frame(self.map_frame)
        buttons_frame.pack(pady=10)
        
        refresh_button = tk.Button(
            buttons_frame,
            text="Обновить список",
            command=self.refresh_packages_list,
            bg=COLORS["button_bg"],
            fg=COLORS["button_fg"],
            font=("Arial", 10, "bold"),
            padx=15,
            pady=5,
            relief=tk.RAISED,
            cursor="hand2"
        )
        refresh_button.pack(side=tk.LEFT, padx=5)
        
        show_selected_button = tk.Button(
            buttons_frame,
            text="Показать выбранный адрес",
            command=self.show_selected_address,
            bg=COLORS["dark_red"],
            fg=COLORS["button_fg"],
            font=("Arial", 10, "bold"),
            padx=15,
            pady=5,
            relief=tk.RAISED,
            cursor="hand2"
        )
        show_selected_button.pack(side=tk.LEFT, padx=5)
        
        # Загрузка списка при инициализации
        self.refresh_packages_list()
    
    def search_address(self):
        """Поиск адреса на Яндекс.Картах"""
        address = self.address_entry.get().strip()
        
        if not address:
            messagebox.showerror("Ошибка", "Пожалуйста, введите адрес для поиска.")
            return
        
        import webbrowser
        import urllib.parse
        
        # Формирование URL для поиска адреса в Яндекс.Картах
        encoded_address = urllib.parse.quote(address)
        yandex_url = f"https://yandex.ru/maps/?text={encoded_address}"
        
        try:
            webbrowser.open(yandex_url)
            self.status_var.set(f"Адрес '{address}' открыт в Яндекс.Картах")
            messagebox.showinfo("Успех", f"Адрес '{address}' открыт в Яндекс.Картах!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось открыть браузер: {e}")
    
    def refresh_packages_list(self):
        """Обновление списка посылок с адресами"""
        try:
            from database import get_all_packages
        except ImportError:
            # Если функция не существует, создадим её
            self.packages_listbox.delete(0, tk.END)
            self.packages_listbox.insert(tk.END, "Список посылок недоступен")
            return
        
        self.packages_listbox.delete(0, tk.END)
        packages = get_all_packages()
        
        if not packages:
            self.packages_listbox.insert(tk.END, "Нет посылок с адресами")
            return
        
        for package in packages:
            sender_address = package.get('sender_address', 'Не указан')
            recipient_address = package.get('recipient_address', 'Не указан')
            
            package_text = f"Посылка {package['tracking_number']}"
            if sender_address and sender_address != 'Не указан':
                package_text += f" | От: {sender_address[:30]}..."
            if recipient_address and recipient_address != 'Не указан':
                package_text += f" | До: {recipient_address[:30]}..."
            
            self.packages_listbox.insert(tk.END, package_text)
    
    def show_selected_address(self):
        """Показать выбранный адрес на карте"""
        selection = self.packages_listbox.curselection()
        
        if not selection:
            messagebox.showerror("Ошибка", "Пожалуйста, выберите посылку из списка.")
            return
        
        selected_text = self.packages_listbox.get(selection[0])
        
        if "Нет посылок" in selected_text or "недоступен" in selected_text:
            messagebox.showinfo("Информация", "Выберите реальную посылку из списка.")
            return
        
        # Извлечение номера посылки
        tracking_number = selected_text.split()[1]  # "Посылка XX-123456"
        
        # Получение информации о посылке
        success, result = package_service.track_package(tracking_number)
        
        if success and isinstance(result, dict):
            sender_address = result.get('sender_address', '')
            recipient_address = result.get('recipient_address', '')
            
            if sender_address or recipient_address:
                # Показываем адрес получателя приоритетно, если есть
                address_to_show = recipient_address if recipient_address else sender_address
                self.address_entry.delete(0, tk.END)
                self.address_entry.insert(0, address_to_show)
                self.search_address()
            else:
                messagebox.showinfo("Информация", "Для этой посылки не указаны адреса.")
        else:
            messagebox.showerror("Ошибка", "Не удалось найти информацию о посылке.")

    def show_about(self):
        """Показывает информацию о программе"""
        about_text = "Служба доставки\n\nВерсия 1.0\n\nПростое приложение для отправки и отслеживания посылок,\nуправления курьерами, работы с отзывами клиентов\nи интеграцией с Яндекс.Картами"
        messagebox.showinfo("О программе", about_text)

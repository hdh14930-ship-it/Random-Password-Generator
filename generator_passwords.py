import tkinter as tk
from tkinter import ttk, messagebox
import json
import random

# Основное окно
root = tk.Tk()
root.title("Random Password Generator")
root.geometry("600x400")

# Переменные для настроек
length_var = tk.IntVar(value=12)
include_digits = tk.BooleanVar(value=True)
include_letters = tk.BooleanVar(value=True)
include_symbols = tk.BooleanVar(value=False)

# Функции генерации пароля
def generate_password():
    length = length_var.get()
    if length < 4 or length > 64:
        messagebox.showerror("Ошибка", "Длина пароля должна быть от 4 до 64")
        return
    
    chars = ""
    if include_digits.get():
        chars += "0123456789"
    if include_letters.get():
        chars += "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if include_symbols.get():
        chars += "!@#$%^&*()_+-=<>?"

    if not chars:
        messagebox.showerror("Ошибка", "Выберите хотя бы один тип символов")
        return
    
    password = "".join(random.choice(chars) for _ in range(length))
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)
    
    # Запись в историю
    add_to_history(password)

# История
history = []

def add_to_history(pwd):
    history.append(pwd)
    update_history_table()
    save_history()

def update_history_table():
    for item in tree.get_children():
        tree.delete(item)
    for pwd in reversed(history):  # отображаем последние сверху
        tree.insert("", tk.END, values=(pwd,))

# Сохранение истории в JSON
def save_history():
    with open("history.json", "w") as f:
        json.dump(history, f)

# Загрузка истории
def load_history():
    global history
    try:
        with open("history.json", "r") as f:
            history = json.load(f)
    except FileNotFoundError:
        history = []

# Интерфейсные компоненты
# Ползунок длины
tk.Label(root, text="Длина пароля").pack()
length_scale = tk.Scale(root, from_=4, to=64, orient=tk.HORIZONTAL, variable=length_var)
length_scale.pack()

# Чекбоксы
checkbox_frame = tk.Frame(root)
checkbox_frame.pack()

tk.Checkbutton(checkbox_frame, text="Цифры", variable=include_digits).grid(row=0, column=0)
tk.Checkbutton(checkbox_frame, text="Буквы", variable=include_letters).grid(row=0, column=1)
tk.Checkbutton(checkbox_frame, text="Спецсимволы", variable=include_symbols).grid(row=0, column=2)

# Генератор
generate_button = tk.Button(root, text="Генерировать", command=generate_password)
generate_button.pack(pady=10)

# Поле для отображения пароля
tk.Label(root, text="Пароль:").pack()
password_entry = tk.Entry(root, width=40)
password_entry.pack()

# Таблица истории
tk.Label(root, text="История:").pack()
columns = ("Пароль",)
tree = ttk.Treeview(root, columns=columns, show="headings")
tree.heading("Пароль", text="Пароль")
tree.pack(fill=tk.BOTH, expand=True)

# Загрузка истории при запуске
load_history()
update_history_table()

# Запуск
root.mainloop()

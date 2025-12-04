import tkinter as tk
from tkinter import ttk
import re

# Константы
MAX_LENGTH = 20
VALID_BASES = [2, 8, 10, 16]
DIGITS = "0123456789ABCDEF"

# Настройка цветовой схемы
COLORS = {
    'bg': '#f0f4f8',
    'fg': '#2d3748',
    'accent': '#4299e1',
    'secondary': '#718096',
    'success': '#48bb78',
    'error': '#f56565',
    'card_bg': '#ffffff',
    'border': '#e2e8f0'
}

def decimal_to_base(num, base):
    """Перевод десятичного числа в указанную систему счисления."""
    if num == 0:
        return "0"
    result = ""
    while num > 0:
        digit = num % base
        result = DIGITS[digit] + result
        num = num // base
    return result

def base_to_decimal(number, base):
    """Перевод числа из указанной системы в десятичную."""
    number = str(number).upper()
    result = 0
    for char in number:
        if char not in DIGITS[:base]:
            return None
        digit = DIGITS.index(char)
        result = result * base + digit
    return result

def validate_number(number, base):
    """Валидация числа для указанной системы счисления."""
    if not number:
        return False, "Введите число"
    
    if len(number) > MAX_LENGTH:
        return False, f"Максимальная длина: {MAX_LENGTH} символов"
    
    pattern = {
        2: r'^[01]+$',
        8: r'^[0-7]+$',
        10: r'^[0-9]+$',
        16: r'^[0-9A-Fa-f]+$'
    }.get(base)
    
    if not pattern:
        return False, "Некорректная система счисления"
    
    if not re.match(pattern, number.upper()):
        error_messages = {
            2: "только 0 и 1",
            8: "цифры 0-7",
            10: "цифры 0-9",
            16: "цифры 0-9 и буквы A-F"
        }
        return False, f"Для системы с основанием {base} допустимы: {error_messages[base]}"
    
    return True, ""

def convert_number():
    """Основная функция конвертации."""
    # Получение данных
    number = entry_number.get().strip().upper()
    base_from = combo_base_from.get()
    base_to = combo_base_to.get()
    
    # Проверка на пустые поля
    if not number:
        show_result("Введите число для конвертации", "error")
        return
    
    if not base_from or not base_to:
        show_result("Выберите системы счисления", "error")
        return
    
    try:
        base_from = int(base_from)
        base_to = int(base_to)
    except ValueError:
        show_result("Некорректная система счисления", "error")
        return
    
    # Валидация
    is_valid, error_msg = validate_number(number, base_from)
    if not is_valid:
        show_result(error_msg, "error")
        return
    
    # Конвертация
    decimal_number = base_to_decimal(number, base_from)
    
    if decimal_number is None:
        show_result("Ошибка при конвертации", "error")
        return
    
    result = decimal_to_base(decimal_number, base_to)
    show_result(f"{number} ({base_from}) = {result} ({base_to})", "success")
    
    # Добавляем в историю
    add_to_history(number, base_from, result, base_to)

def show_result(message, msg_type="success"):
    """Отображение результата с цветом в зависимости от типа."""
    colors = {
        "success": COLORS['success'],
        "error": COLORS['error'],
        "info": COLORS['accent']
    }
    result_label.config(text=message, foreground=colors.get(msg_type, COLORS['fg']))

def clear_fields():
    """Очистка всех полей."""
    entry_number.delete(0, tk.END)
    combo_base_from.set('')
    combo_base_to.set('')
    show_result("Поля очищены", "info")

def add_to_history(original, from_base, converted, to_base):
    """Добавление результата в историю."""
    history_text = f"{original} ({from_base}) → {converted} ({to_base})"
    history_listbox.insert(0, history_text)
    
    # Ограничиваем историю последними 10 операциями
    if history_listbox.size() > 10:
        history_listbox.delete(10, tk.END)

def copy_to_clipboard():
    """Копирование результата в буфер обмена."""
    result = result_label.cget("text")
    if result and not result.startswith("Поля"):
        window.clipboard_clear()
        window.clipboard_append(result.split(" = ")[-1].split(" (")[0] if " = " in result else result)
        status_label.config(text="Результат скопирован!", foreground=COLORS['success'])
        window.after(2000, lambda: status_label.config(text="Готов", foreground=COLORS['secondary']))

def swap_bases():
    """Обмен значениями систем счисления."""
    from_val = combo_base_from.get()
    to_val = combo_base_to.get()
    combo_base_from.set(to_val)
    combo_base_to.set(from_val)

def on_key_release(event):
    """Обработка нажатия Enter для конвертации."""
    if event.keysym == 'Return':
        convert_number()

# Создание основного окна
window = tk.Tk()
window.title("Конвертер систем счисления")
window.configure(bg=COLORS['bg'])
window.geometry("620x920")  # Увеличенная высота окна

# Стили для ttk
style = ttk.Style()
style.theme_use('clam')

# Настраиваем цвета для виджетов
style.configure('TLabel', background=COLORS['bg'], foreground=COLORS['fg'], font=('Segoe UI', 10))
style.configure('TButton', font=('Segoe UI', 10))
style.configure('TCombobox', font=('Segoe UI', 10))

# Главный контейнер
main_container = tk.Frame(window, bg=COLORS['bg'])
main_container.pack(fill=tk.BOTH, expand=True, padx=25, pady=25)

# Заголовок
title_frame = tk.Frame(main_container, bg=COLORS['bg'])
title_frame.pack(fill=tk.X, pady=(0, 25))

title_label = tk.Label(
    title_frame,
    text="🔢 Конвертер систем счисления",
    font=('Segoe UI', 20, 'bold'),
    fg=COLORS['accent'],
    bg=COLORS['bg']
)
title_label.pack()

subtitle_label = tk.Label(
    title_frame,
    text="Преобразование чисел между различными системами счисления",
    font=('Segoe UI', 11),
    fg=COLORS['secondary'],
    bg=COLORS['bg']
)
subtitle_label.pack()

# Карточка ввода
input_card = tk.Frame(
    main_container,
    bg=COLORS['card_bg'],
    relief=tk.RAISED,
    bd=0,
    highlightbackground=COLORS['border'],
    highlightthickness=1
)
input_card.pack(fill=tk.X, pady=(0, 25))

# Внутренний отступ карточки
input_content = tk.Frame(input_card, bg=COLORS['card_bg'], padx=25, pady=25)
input_content.pack(fill=tk.BOTH, expand=True)

# Поле для ввода числа
tk.Label(
    input_content,
    text="Введите число:",
    font=('Segoe UI', 12, 'bold'),
    fg=COLORS['fg'],
    bg=COLORS['card_bg']
).grid(row=0, column=0, sticky='w', pady=(0, 10))

entry_number = ttk.Entry(
    input_content,
    font=('Segoe UI', 12),
    width=35
)
entry_number.grid(row=1, column=0, columnspan=3, sticky='ew', pady=(0, 25))
entry_number.bind('<KeyRelease>', on_key_release)

# Системы счисления
base_frame = tk.Frame(input_content, bg=COLORS['card_bg'])
base_frame.grid(row=2, column=0, columnspan=3, sticky='ew', pady=(0, 25))

# Исходная система
from_label = tk.Label(
    base_frame,
    text="Из системы:",
    font=('Segoe UI', 12, 'bold'),
    fg=COLORS['fg'],
    bg=COLORS['card_bg']
)
from_label.grid(row=0, column=0, sticky='w', padx=(0, 20))

combo_base_from = ttk.Combobox(
    base_frame,
    values=VALID_BASES,
    font=('Segoe UI', 12),
    width=10,
    state='readonly'
)
combo_base_from.grid(row=1, column=0, sticky='w', padx=(0, 20))

# Кнопка обмена
swap_btn = tk.Button(
    base_frame,
    text="⇄",
    font=('Segoe UI', 11),
    fg='white',
    bg=COLORS['secondary'],
    bd=0,
    padx=15,
    pady=5,
    cursor='hand2',
    command=swap_bases
)
swap_btn.grid(row=1, column=1, padx=15)

# Целевая система
to_label = tk.Label(
    base_frame,
    text="В систему:",
    font=('Segoe UI', 12, 'bold'),
    fg=COLORS['fg'],
    bg=COLORS['card_bg']
)
to_label.grid(row=0, column=3, sticky='w')

combo_base_to = ttk.Combobox(
    base_frame,
    values=VALID_BASES,
    font=('Segoe UI', 12),
    width=10,
    state='readonly'
)
combo_base_to.grid(row=1, column=3, sticky='w')

# Выравниваем колонки
base_frame.grid_columnconfigure(0, weight=1)
base_frame.grid_columnconfigure(1, weight=0)
base_frame.grid_columnconfigure(2, weight=1)

# Кнопки действий - теперь в одну строку с равномерным распределением
button_frame = tk.Frame(input_content, bg=COLORS['card_bg'])
button_frame.grid(row=3, column=0, columnspan=3, sticky='ew', pady=(10, 0))

# Настройка колонок для равномерного распределения
button_frame.grid_columnconfigure(0, weight=1)
button_frame.grid_columnconfigure(1, weight=1)
button_frame.grid_columnconfigure(2, weight=1)

# Кнопка конвертации
convert_btn = tk.Button(
    button_frame,
    text="🔄 Конвертировать",
    font=('Segoe UI', 11, 'bold'),
    fg='white',
    bg=COLORS['accent'],
    bd=0,
    padx=20,
    pady=12,
    cursor='hand2',
    command=convert_number
)
convert_btn.grid(row=0, column=0, sticky='ew', padx=(0, 10))

# Кнопка очистки
clear_btn = tk.Button(
    button_frame,
    text="🗑️ Очистить",
    font=('Segoe UI', 11),
    fg='white',
    bg=COLORS['secondary'],
    bd=0,
    padx=20,
    pady=12,
    cursor='hand2',
    command=clear_fields
)
clear_btn.grid(row=0, column=1, sticky='ew', padx=5)

# Кнопка копирования
copy_btn = tk.Button(
    button_frame,
    text="📋 Копировать",
    font=('Segoe UI', 11),
    fg='white',
    bg=COLORS['secondary'],
    bd=0,
    padx=20,
    pady=12,
    cursor='hand2',
    command=copy_to_clipboard
)
copy_btn.grid(row=0, column=2, sticky='ew', padx=(10, 0))

# Карточка результата
result_card = tk.Frame(
    main_container,
    bg=COLORS['card_bg'],
    relief=tk.RAISED,
    bd=0,
    highlightbackground=COLORS['border'],
    highlightthickness=1
)
result_card.pack(fill=tk.X, pady=(0, 25))

result_content = tk.Frame(result_card, bg=COLORS['card_bg'], padx=25, pady=25)
result_content.pack(fill=tk.BOTH, expand=True)

tk.Label(
    result_content,
    text="Результат:",
    font=('Segoe UI', 12, 'bold'),
    fg=COLORS['fg'],
    bg=COLORS['card_bg']
).pack(anchor='w', pady=(0, 15))

result_label = tk.Label(
    result_content,
    text="Здесь будет результат...",
    font=('Segoe UI', 14),
    fg=COLORS['secondary'],
    bg=COLORS['card_bg'],
    wraplength=550,
    height=2
)
result_label.pack(fill=tk.X, pady=(0, 10))

# Карточка истории
history_card = tk.Frame(
    main_container,
    bg=COLORS['card_bg'],
    relief=tk.RAISED,
    bd=0,
    highlightbackground=COLORS['border'],
    highlightthickness=1
)
history_card.pack(fill=tk.BOTH, expand=True)

history_content = tk.Frame(history_card, bg=COLORS['card_bg'], padx=25, pady=25)
history_content.pack(fill=tk.BOTH, expand=True)

tk.Label(
    history_content,
    text="📋 История конвертаций:",
    font=('Segoe UI', 12, 'bold'),
    fg=COLORS['fg'],
    bg=COLORS['card_bg']
).pack(anchor='w', pady=(0, 15))

# Создаем Scrollbar и Listbox для истории
history_frame = tk.Frame(history_content, bg=COLORS['card_bg'])
history_frame.pack(fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(history_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

history_listbox = tk.Listbox(
    history_frame,
    yscrollcommand=scrollbar.set,
    bg='white',
    fg=COLORS['fg'],
    font=('Segoe UI', 10),
    bd=0,
    highlightthickness=0,
    selectbackground=COLORS['accent'],
    height=5  # Увеличенная высота списка
)
history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar.config(command=history_listbox.yview)

# Статус бар
status_frame = tk.Frame(main_container, bg=COLORS['bg'])
status_frame.pack(fill=tk.X, pady=(15, 0))

status_label = tk.Label(
    status_frame,
    text="Готов к работе",
    font=('Segoe UI', 10),
    fg=COLORS['secondary'],
    bg=COLORS['bg']
)
status_label.pack(side=tk.LEFT)

length_label = tk.Label(
    status_frame,
    text=f"Максимальная длина числа: {MAX_LENGTH} символов",
    font=('Segoe UI', 10),
    fg=COLORS['secondary'],
    bg=COLORS['bg']
)
length_label.pack(side=tk.RIGHT)

# Подсказки при наведении
tooltips = {
    entry_number: "Введите число для конвертации (допустимы цифры 0-9 и буквы A-F)",
    combo_base_from: "Выберите исходную систему счисления (2, 8, 10, 16)",
    combo_base_to: "Выберите целевую систему счисления (2, 8, 10, 16)",
    convert_btn: "Выполнить конвертацию (также можно нажать Enter)",
    swap_btn: "Поменять системы счисления местами",
    clear_btn: "Очистить все поля ввода",
    copy_btn: "Копировать результат в буфер обмена",
    history_listbox: "Последние 10 конвертаций (кликните для выбора)"
}

def show_tooltip(event):
    widget = event.widget
    if widget in tooltips:
        status_label.config(text=tooltips[widget])

def hide_tooltip(event):
    status_label.config(text="Готов")

# Привязка событий для tooltips
for widget in tooltips:
    widget.bind('<Enter>', show_tooltip)
    widget.bind('<Leave>', hide_tooltip)

# Фокус на поле ввода при запуске
window.after(100, entry_number.focus)

# Запуск приложения
window.mainloop()
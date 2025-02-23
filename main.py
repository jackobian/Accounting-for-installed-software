import datetime
import os
import tkinter as tk
from tkinter import messagebox, simpledialog

# Файл для хранения данных о ПО
software_file = 'software.txt'
log_file = 'log.txt'
etxt_file = 'ETXT'

# Функция для записи лога
def write_log(action):
    with open(log_file, 'a') as log:
        log.write(f"{datetime.datetime.now().strftime('%d.%m.%y %H:%M')} - {action}\n")

# Функция для чтения данных из файла
def read_software_data():
    if not os.path.exists(software_file):
        return []
    with open(software_file, 'r') as file:
        lines = file.readlines()
    software_list = []
    for line in lines:
        name, purpose, install_date, version = line.strip().split(',')
        software_list.append({'name': name, 'purpose': purpose, 'install_date': install_date, 'version': version})
    return software_list

# Функция для записи данных в файл
def write_software_data(software_list):
    with open(software_file, 'w') as file:
        for software in software_list:
            file.write(f"{software['name']},{software['purpose']},{software['install_date']},{software['version']}\n")

# Функция для отображения списка ПО
def display_software(software_list):
    software_text.delete(1.0, tk.END)
    for software in software_list:
        software_text.insert(tk.END, f"{software['name']} - {software['purpose']} (Установлено: {software['install_date']}, Версия: {software['version']})\n")

# Функция для добавления ПО
def add_software():
    name = simpledialog.askstring("Добавить ПО", "Введите наименование ПО:")
    purpose = simpledialog.askstring("Добавить ПО", "Введите назначение ПО:")
    install_date = simpledialog.askstring("Добавить ПО", "Введите дату установки (dd.mm.yy):")
    version = simpledialog.askstring("Добавить ПО", "Введите версию ПО:")
    if name and purpose and install_date and version:
        software_list.append({'name': name, 'purpose': purpose, 'install_date': install_date, 'version': version})
        write_software_data(software_list)
        write_log(f"Добавлено ПО: {name}")
        display_software(software_list)

# Функция для удаления ПО
def delete_software():
    name = simpledialog.askstring("Удалить ПО", "Введите наименование ПО для удаления:")
    if name:
        global software_list
        software_list = [software for software in software_list if software['name'] != name]
        write_software_data(software_list)
        write_log(f"Удалено ПО: {name}")
        display_software(software_list)

# Функция для обновления ПО
def update_software():
    name = simpledialog.askstring("Обновить ПО", "Введите наименование ПО для обновления:")
    if name:
        for software in software_list:
            if software['name'] == name:
                software['purpose'] = simpledialog.askstring("Обновить ПО", "Введите новое назначение ПО:")
                software['install_date'] = simpledialog.askstring("Обновить ПО", "Введите новую дату установки (dd.mm.yy):")
                software['version'] = simpledialog.askstring("Обновить ПО", "Введите новую версию ПО:")
                write_software_data(software_list)
                write_log(f"Обновлено ПО: {name}")
                display_software(software_list)
                break

# Функция для проверки файла ETXT
def check_etxt():
    if os.path.exists(etxt_file):
        with open(etxt_file, 'r') as file:
            content = file.read()
        messagebox.showinfo("Проверка ETXT", f"Файл ETXT существует и содержит:\n{content}")
    else:
        messagebox.showwarning("Проверка ETXT", "Файл ETXT не найден.")

# Основная функция программы
def main():
    global software_list
    software_list = read_software_data()
    write_log(f"Запуск программы. Количество установленного ПО: {len(software_list)}")
    display_software(software_list)

# Создание GUI
root = tk.Tk()
root.title("Учет программного обеспечения")

software_text = tk.Text(root, height=20, width=50)
software_text.pack()

button_frame = tk.Frame(root)
button_frame.pack()

add_button = tk.Button(button_frame, text="Добавить ПО", command=add_software)
add_button.pack(side=tk.LEFT)

delete_button = tk.Button(button_frame, text="Удалить ПО", command=delete_software)
delete_button.pack(side=tk.LEFT)

update_button = tk.Button(button_frame, text="Обновить ПО", command=update_software)
update_button.pack(side=tk.LEFT)

check_etxt_button = tk.Button(button_frame, text="Проверить ETXT", command=check_etxt)
check_etxt_button.pack(side=tk.LEFT)

main()
root.mainloop()

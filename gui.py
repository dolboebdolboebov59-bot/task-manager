"""Графический интерфейс приложения "Менеджер задач" на Tkinter."""

import tkinter as tk
from tkinter import messagebox

from classes import Task, TaskManager

# Календарь берём из tkcalendar (виджет на базе ttk).
# Если библиотека не установлена, используем обычное поле Entry.
try:
    from tkcalendar import DateEntry
    HAS_CALENDAR = True
except ImportError:
    HAS_CALENDAR = False


class TaskManagerApp:
    """Главное окно приложения."""

    def __init__(self, root):
        self.manager = TaskManager()
        self.root = root
        self.root.title("Менеджер задач")
        self.setup_ui()

    def setup_ui(self):
        # Поля ввода
        tk.Label(self.root, text="Название").grid(
            row=0, column=0, padx=5, pady=5, sticky="w"
        )
        self.title_entry = tk.Entry(self.root, width=40)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Описание").grid(
            row=1, column=0, padx=5, pady=5, sticky="nw"
        )
        self.desc_text = tk.Text(self.root, height=3, width=30)
        self.desc_text.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Срок выполнения").grid(
            row=2, column=0, padx=5, pady=5, sticky="w"
        )
        if HAS_CALENDAR:
            self.date_entry = DateEntry(
                self.root, width=17, background="darkblue",
                foreground="white", borderwidth=2, date_pattern="yyyy-mm-dd",
            )
        else:
            self.date_entry = tk.Entry(self.root, width=40)
        self.date_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # Кнопки
        tk.Button(self.root, text="Добавить задачу", command=self.add_task).grid(
            row=3, column=0, padx=5, pady=5
        )
        tk.Button(self.root, text="Удалить задачу", command=self.delete_task).grid(
            row=3, column=1, padx=5, pady=5
        )

        # Список задач
        self.tasks_listbox = tk.Listbox(self.root, width=60, height=12)
        self.tasks_listbox.grid(
            row=4, column=0, columnspan=2, padx=5, pady=5, sticky="ew"
        )
        self.update_listbox()

    def add_task(self):
        """Создаёт задачу из полей ввода и добавляет её в менеджер."""
        title = self.title_entry.get()
        description = self.desc_text.get("1.0", tk.END).strip()
        due_date = self.date_entry.get()
        if title and description and due_date:
            task = Task(title, description, due_date)
            self.manager.add_task(task)
            self.update_listbox()
            self.clear_inputs()
        else:
            messagebox.showwarning("Ошибка", "Заполните все поля!")

    def delete_task(self):
        """Удаляет выбранную в списке задачу."""
        selected = self.tasks_listbox.curselection()
        if selected:
            self.manager.delete_task(selected[0])
            self.update_listbox()
        else:
            messagebox.showinfo("Информация", "Выберите задачу для удаления.")

    def update_listbox(self):
        """Перерисовывает список задач."""
        self.tasks_listbox.delete(0, tk.END)
        for task in self.manager.tasks:
            self.tasks_listbox.insert(tk.END, str(task))

    def clear_inputs(self):
        """Очищает поля формы после добавления задачи."""
        self.title_entry.delete(0, tk.END)
        self.desc_text.delete("1.0", tk.END)
        if not HAS_CALENDAR:
            self.date_entry.delete(0, tk.END)


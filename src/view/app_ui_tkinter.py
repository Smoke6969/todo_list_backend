import tkinter as tk
from tkinter import simpledialog, messagebox, Menu
import customtkinter as ctk
from datetime import datetime
import json
from src.models.task import Task
from src.models.sub_task import SubTask

class TodoApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Todo App - CustomTkinter")
        self.geometry("800x500")

        # Sample tasks with subtasks
        self.tasks = [Task(f"Task {i+1}", "Description", "2023-12-31") for i in range(5)]
        for task in self.tasks:
            task.add_subtask(SubTask(f"Subtask of {task.title}", "Subtask Description", "2023-12-31"))

        # Layout configuration
        self.grid_columnconfigure(1, weight=1)
        self.left_panel = ctk.CTkFrame(self, width=200)
        self.left_panel.grid(column=0, row=0, sticky="nswe", padx=20, pady=20)

        self.right_panel = ctk.CTkFrame(self)
        self.right_panel.grid(column=1, row=0, sticky="nswe", padx=20, pady=20)
        self.right_panel.grid_rowconfigure(0, weight=1)
        self.right_panel.grid_columnconfigure(0, weight=1)
        self.task_mapping = {}
        self.create_left_panel_controls()
        self.create_task_list()


    def create_left_panel_controls(self):
        add_task_button = ctk.CTkButton(self.left_panel, text="Add Task", command=self.open_add_task_window)
        add_task_button.pack(pady=(0, 10))

        filter_label = ctk.CTkLabel(self.left_panel, text="Show:")
        filter_label.pack(pady=(10, 5))

        self.filter_var = ctk.StringVar(value="all")
        all_tasks_rb = ctk.CTkRadioButton(self.left_panel, text="All tasks", variable=self.filter_var, value="all")
        in_progress_rb = ctk.CTkRadioButton(self.left_panel, text="In Progress", variable=self.filter_var, value="in_progress")
        completed_rb = ctk.CTkRadioButton(self.left_panel, text="Completed", variable=self.filter_var, value="completed")

        all_tasks_rb.pack()
        in_progress_rb.pack(pady=(5, 0))
        completed_rb.pack(pady=(5, 0))

    def create_task_list(self):
        self.task_listbox = tk.Listbox(self.right_panel)
        self.task_listbox.grid(row=0, column=0, sticky="nswe", padx=5, pady=5)
        self.task_listbox.bind("<Double-Button-1>", self.on_task_double_click)
        self.task_listbox.bind("<Button-3>", self.on_task_right_click)  # Right-click
        self.refresh_task_list()

    def refresh_task_list(self):
        self.task_listbox.delete(0, tk.END)
        self.task_mapping.clear()
        listbox_index = 0

        for task in self.tasks:
            display_text = f"{task.title} - Due: {task.due_date}"
            self.task_listbox.insert(tk.END, display_text)
            self.task_mapping[listbox_index] = task
            listbox_index += 1

            for subtask in task.subtasks:
                subtask_text = f"    → {subtask.title} - Due: {subtask.due_date}"
                self.task_listbox.insert(tk.END, subtask_text)
                # For simplicity, subtasks are also mapped, even though they're not editable here
                self.task_mapping[listbox_index] = subtask
                listbox_index += 1

    def open_add_task_window(self, task=None, is_subtask=False):
        def save():
            title = title_entry.get()
            description = description_entry.get()
            due_date = due_date_entry.get()
            if not title:
                messagebox.showerror("Error", "Title is required.")
                return

            # Validate date format
            try:
                datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD.")
                return

            if task and not is_subtask:
                task.title = title
                task.description = description
                task.due_date = due_date
            elif task and is_subtask:
                task.add_subtask(SubTask(title, description, due_date))
            else:
                self.tasks.append(Task(title, description, due_date))
            task_window.destroy()
            self.refresh_task_list()

        task_window = ctk.CTkToplevel(self)
        task_window.title("Add/Edit Task")
        task_window.geometry("300x300")

        ctk.CTkLabel(task_window, text="Title:").pack(pady=(10, 5))
        title_entry = ctk.CTkEntry(task_window)
        title_entry.pack()

        ctk.CTkLabel(task_window, text="Description:").pack(pady=(10, 5))
        description_entry = ctk.CTkEntry(task_window)
        description_entry.pack()

        ctk.CTkLabel(task_window, text="Due Date (YYYY-MM-DD):").pack(pady=(10, 5))
        due_date_entry = ctk.CTkEntry(task_window)
        due_date_entry.pack()

        if task:
            title_entry.insert(0, task.title)
            description_entry.insert(0, task.description if task.description else "")
            due_date_entry.insert(0, task.due_date if task.due_date else "")

        ctk.CTkButton(task_window, text="Save", command=save).pack(pady=(20, 10))

    def on_task_double_click(self, event):
        selection = self.task_listbox.curselection()
        if selection:
            index = selection[0]
            if index in self.task_mapping:
                selected_task = self.task_mapping[index]
                self.open_add_task_window(selected_task)

    def on_task_right_click(self, event):
        def add_subtask():
            selected_task = self.tasks[selection[0]]
            self.open_add_task_window(selected_task, is_subtask=True)

        def delete_task():
            if selection:
                del self.tasks[selection[0]]
                self.refresh_task_list()

        selection = self.task_listbox.curselection()
        if selection:
            menu = Menu(self, tearoff=0)
            menu.add_command(label="Add Subtask", command=add_subtask)
            menu.add_command(label="Delete", command=delete_task)
            menu.tk_popup(event.x_root, event.y_root)

if __name__ == "__main__":
    app = TodoApp()
    app.mainloop()

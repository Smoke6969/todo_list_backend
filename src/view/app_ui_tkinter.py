import tkinter as tk
from tkinter import simpledialog, messagebox, Menu
import customtkinter as ctk
from datetime import datetime
from src.models.task import Task
from src.models.sub_task import SubTask
from src.controllers.tasks_controller import TasksController
from tkcalendar import DateEntry
import customtkinter as ctk


class TodoApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Todo App")
        self.geometry("800x500")

        self.tasks_controller = TasksController("../../data/tasks.json")
        self.tasks = self.tasks_controller.tasks

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

        # filter_label = ctk.CTkLabel(self.left_panel, text="Show:")
        # filter_label.pack(pady=(10, 5))
        #
        # self.filter_var = ctk.StringVar(value="all")
        # all_tasks_rb = ctk.CTkRadioButton(self.left_panel, text="All tasks", variable=self.filter_var, value="all")
        # in_progress_rb = ctk.CTkRadioButton(self.left_panel, text="In Progress", variable=self.filter_var,
        #                                     value="in_progress")
        # completed_rb = ctk.CTkRadioButton(self.left_panel, text="Completed", variable=self.filter_var,
        #                                   value="completed")

        # all_tasks_rb.pack()
        # in_progress_rb.pack(pady=(5, 0))
        # completed_rb.pack(pady=(5, 0))

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
            display_text = f"{task.title} - Due: {task.due_date} {'Completed' if task.completed else ''}"
            self.task_listbox.insert(tk.END, display_text)
            self.task_mapping[listbox_index] = task
            listbox_index += 1

            for subtask in task.subtasks:
                subtask_text = f"    → {subtask.title} - Due: {subtask.due_date} {'Completed' if subtask.completed else ''}"
                self.task_listbox.insert(tk.END, subtask_text)
                self.task_mapping[listbox_index] = subtask
                listbox_index += 1

    def open_add_task_window(self, task=None, is_subtask=False, parent_task=None):
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

            if is_subtask:
                # Edit or add subtask
                if task and parent_task:  # Editing an existing subtask
                    for st in parent_task.subtasks:
                        if st.title == task.title:  # Identify the subtask by title
                            st.title = title
                            st.description = description
                            st.due_date = due_date
                            break
                else:  # Adding a new subtask
                    task.add_subtask(SubTask(title, description, due_date))
                self.tasks_controller.save_tasks(self.tasks)
            else:
                # Edit or add task
                if task:  # Editing an existing task
                    self.tasks_controller.edit_task(task.title, title, description, due_date)
                else:  # Adding a new task
                    self.tasks_controller.add_task(Task(title, description, due_date))

            task_window.destroy()
            self.refresh_task_list()

        task_window = ctk.CTkToplevel(self)
        task_window.title("Add/Edit Task")
        task_window.geometry("300x300")

        # Position the new window at the center of the main window
        window_width = 300
        window_height = 300
        position_right = int(self.winfo_screenwidth() / 2 - window_width / 2)
        position_down = int(self.winfo_screenheight() / 2 - window_height / 2)
        task_window.geometry("+{}+{}".format(position_right, position_down))

        # Set the new window as a transient window of the main application window
        task_window.transient(self)

        # Make the new window modal
        task_window.grab_set()

        # Entry fields for task/subtask details
        ctk.CTkLabel(task_window, text="Title:").pack(pady=(10, 5))
        title_entry = ctk.CTkEntry(task_window)
        title_entry.pack()

        ctk.CTkLabel(task_window, text="Description:").pack(pady=(10, 5))
        description_entry = ctk.CTkEntry(task_window)
        description_entry.pack()

        ctk.CTkLabel(task_window, text="Due Date (YYYY-MM-DD):").pack(pady=(10, 5))
        due_date_entry = DateEntry(task_window, date_pattern='y-mm-dd', width=12)
        due_date_entry.pack()

        if task and is_subtask and not parent_task:
            pass
        # Pre-fill fields if editing an existing task or subtask
        elif task:
            title_entry.insert(0, task.title)
            description_entry.insert(0, task.description if task.description else "")
            due_date_entry.insert(0, task.due_date if task.due_date else "")

        ctk.CTkButton(task_window, text="Save", command=save).pack(pady=(20, 10))

    def on_task_double_click(self, event):
        selection = self.task_listbox.curselection()
        if selection:
            index = selection[0]
            if index in self.task_mapping:
                selected_item = self.task_mapping[index]
                if isinstance(selected_item, SubTask):
                    # Find the parent task of the selected subtask
                    for task in self.tasks:
                        if selected_item in task.subtasks:
                            parent_task = task
                            break
                    self.open_add_task_window(task=selected_item, is_subtask=True, parent_task=parent_task)
                else:
                    # Edit a main task
                    self.open_add_task_window(task=selected_item, is_subtask=False)

    def delete_task(self):
        selection = self.task_listbox.curselection()
        if selection:
            index = selection[0]
            if index in self.task_mapping:
                selected_item = self.task_mapping[index]

                if isinstance(selected_item, Task):
                    self.tasks = self.tasks_controller.remove_task(selected_item.title)

                elif isinstance(selected_item, SubTask):
                    for task in self.tasks:
                        if selected_item in task.subtasks:
                            task.subtasks.remove(selected_item)
                            break
                    self.tasks_controller.save_tasks(self.tasks)

                self.refresh_task_list()

    def complete_task(self, selected_item):
        selected_item.completed = True
        self.tasks_controller.save_tasks(self.tasks)
        self.refresh_task_list()

    def on_task_right_click(self, event):
        try:
            self.task_listbox.selection_clear(0, tk.END)
            selection = self.task_listbox.nearest(event.y)
            self.task_listbox.selection_set(selection)
            selected_item = self.task_mapping.get(selection)

            menu = Menu(self, tearoff=0)
            menu.add_command(label="View/Edit", command=lambda: self.open_add_task_window(selected_item))
            menu.add_command(label="Delete", command=self.delete_task)
            menu.add_command(label="Complete", command=lambda: self.complete_task(selected_item))

            if isinstance(selected_item, Task):  # Add subtask option only for main tasks
                menu.add_command(label="Add Subtask",
                                 command=lambda: self.open_add_task_window(selected_item, is_subtask=True))

            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()


if __name__ == "__main__":
    app = TodoApp()
    app.mainloop()

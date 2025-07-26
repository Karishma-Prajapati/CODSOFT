import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

TASKS_FILE = "tasks.json"

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List App")
        self.tasks = []

        self.frame = tk.Frame(root)
        self.frame.pack(padx=10, pady=10)

        self.task_entry = tk.Entry(self.frame, width=40)
        self.task_entry.grid(row=0, column=0, padx=5, pady=5)

        self.priority_var = tk.StringVar(value="Medium")
        self.priority_menu = tk.OptionMenu(self.frame, self.priority_var, "High", "Medium", "Low")
        self.priority_menu.grid(row=0, column=1)

        self.add_btn = tk.Button(self.frame, text="Add Task", command=self.add_task)
        self.add_btn.grid(row=0, column=2, padx=5)

        self.task_listbox = tk.Listbox(self.frame, width=60, height=10)
        self.task_listbox.grid(row=1, column=0, columnspan=3, pady=10)

        self.complete_btn = tk.Button(self.frame, text="Mark as Completed", command=self.mark_completed)
        self.complete_btn.grid(row=2, column=0)

        self.edit_btn = tk.Button(self.frame, text="Edit Task", command=self.edit_task)
        self.edit_btn.grid(row=2, column=1)

        self.delete_btn = tk.Button(self.frame, text="Delete Task", command=self.delete_task)
        self.delete_btn.grid(row=2, column=2)

        self.load_tasks()

    def add_task(self):
        title = self.task_entry.get()
        priority = self.priority_var.get()

        if title.strip() == "":
            messagebox.showwarning("Input Error", "Task title cannot be empty.")
            return

        task = {"title": title, "priority": priority, "completed": False}
        self.tasks.append(task)
        self.update_listbox()
        self.save_tasks()
        self.task_entry.delete(0, tk.END)

    def update_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for idx, task in enumerate(self.tasks):
            status = "✓" if task["completed"] else "✗"
            display_text = f"{idx+1}. [{status}] {task['title']} (Priority: {task['priority']})"
            self.task_listbox.insert(tk.END, display_text)

    def delete_task(self):
        selected = self.task_listbox.curselection()
        if not selected:
            messagebox.showwarning("Select Task", "Please select a task to delete.")
            return
        del self.tasks[selected[0]]
        self.update_listbox()
        self.save_tasks()

    def mark_completed(self):
        selected = self.task_listbox.curselection()
        if not selected:
            messagebox.showwarning("Select Task", "Please select a task to mark.")
            return
        idx = selected[0]
        self.tasks[idx]["completed"] = not self.tasks[idx]["completed"]
        self.update_listbox()
        self.save_tasks()

    def edit_task(self):
        selected = self.task_listbox.curselection()
        if not selected:
            messagebox.showwarning("Select Task", "Please select a task to edit.")
            return
        idx = selected[0]
        new_title = simpledialog.askstring("Edit Task", "Update task title:", initialvalue=self.tasks[idx]["title"])
        if new_title:
            self.tasks[idx]["title"] = new_title
            self.update_listbox()
            self.save_tasks()

    def save_tasks(self):
        with open(TASKS_FILE, "w") as f:
            json.dump(self.tasks, f)

    def load_tasks(self):
        if os.path.exists(TASKS_FILE):
            with open(TASKS_FILE, "r") as f:
                self.tasks = json.load(f)
                self.update_listbox()


if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
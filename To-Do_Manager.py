import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

TASKS_FILE = "tasks.json"

def load_tasks():
    if os.path.exists(TASKS_FILE) and os.path.getsize(TASKS_FILE) > 0:
        with open(TASKS_FILE, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []

def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)

def update_task_list():
    task_list.delete(*task_list.get_children())
    for i, task in enumerate(tasks, start=1):
        task_list.insert("", "end", values=(i, task["name"], task["Description"], task["status"]))

def add_task():
    name = name_var.get()
    category = category_var.get()
    status = status_var.get()
    if name:
        tasks.append({"name": name, "category": category, "status": status})
        save_tasks(tasks)
        update_task_list()
        name_var.set("")
        category_var.set("")
        status_var.set("Pending")
        messagebox.showinfo("Success", f"Task '{name}' added!")
    else:
        messagebox.showwarning("Missing Info", "Task name is required.")

def delete_task():
    selected = task_list.selection()
    if selected:
        index = int(task_list.item(selected[0])["values"][0]) - 1
        removed = tasks.pop(index)
        save_tasks(tasks)
        update_task_list()
        messagebox.showinfo("Deleted", f"Task '{removed['name']}' deleted.")
    else:
        messagebox.showwarning("No Selection", "Select a task to delete.")

def update_task():
    selected = task_list.selection()
    if selected:
        index = int(task_list.item(selected[0])["values"][0]) - 1
        task = tasks[index]
        new_name = name_var.get()
        new_category = category_var.get()
        new_status = status_var.get()
        if new_name:
            task["name"] = new_name
        if new_category:
            task["category"] = new_category
        if new_status:
            task["status"] = new_status
        save_tasks(tasks)
        update_task_list()
        name_var.set("")
        category_var.set("")
        status_var.set("Pending")
        messagebox.showinfo("Updated", "Task updated successfully.")
    else:
        messagebox.showwarning("No Selection", "Select a task to update.")

# GUI setup
root = tk.Tk()
root.title("✨ TaskTact - Intelligent To-Do Manager")
root.geometry("700x500")
root.configure(bg="#f0f4f7")

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
style.configure("Treeview", font=("Segoe UI", 10), rowheight=25)

# Title
title_label = tk.Label(root, text="TaskTact 🧠", font=("Segoe UI", 20, "bold"), bg="#f0f4f7", fg="#333")
title_label.pack(pady=10)

# Input Frame
input_frame = ttk.LabelFrame(root, text="Add / Update Task", padding=10)
input_frame.pack(fill="x", padx=10, pady=10)

name_var = tk.StringVar()
category_var = tk.StringVar()
status_var = tk.StringVar(value="Pending")

ttk.Label(input_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
ttk.Entry(input_frame, textvariable=name_var, width=40).grid(row=0, column=1, padx=5, pady=5)

ttk.Label(input_frame, text="Category:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
ttk.Entry(input_frame, textvariable=category_var, width=40).grid(row=1, column=1, padx=5, pady=5)

ttk.Label(input_frame, text="Status:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
ttk.Combobox(input_frame, textvariable=status_var, values=["Pending", "In Progress", "Completed"], width=37).grid(row=2, column=1, padx=5, pady=5)

ttk.Button(input_frame, text="Add Task", command=add_task).grid(row=3, column=0, padx=5, pady=10)
ttk.Button(input_frame, text="Update Task", command=update_task).grid(row=3, column=1, padx=5, pady=10, sticky="w")

# Task List Frame
list_frame = ttk.LabelFrame(root, text="Your Tasks", padding=10)
list_frame.pack(fill="both", expand=True, padx=10, pady=5)

columns = ("#", "Name", "Category", "Status")
task_list = ttk.Treeview(list_frame, columns=columns, show="headings")
for col in columns:
    task_list.heading(col, text=col)
    task_list.column(col, anchor="center")

task_list.pack(fill="both", expand=True)

ttk.Button(root, text="Delete Selected Task", command=delete_task).pack(pady=10)

# Load tasks
tasks = load_tasks()
update_task_list()

root.mainloop()


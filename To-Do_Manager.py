import tkinter as tk
from tkinter import ttk, messagebox

# Task storage
tasks = []

# Add task
def add_task():
    title = title_var.get()
    desc = desc_var.get()
    if title:
        tasks.append({"title": title, "description": desc})
        update_task_list()
        title_var.set("")
        desc_var.set("")
        messagebox.showinfo("Success", "Task added successfully!")
    else:
        messagebox.showwarning("Missing Title", "Please enter a task title.")

# Update task list display
def update_task_list():
    task_list.delete(*task_list.get_children())
    for i, task in enumerate(tasks, start=1):
        task_list.insert("", "end", values=(i, task["title"], task["description"]))

# Delete selected task
def delete_task():
    selected = task_list.selection()
    if selected:
        index = int(task_list.item(selected[0])["values"][0]) - 1
        deleted = tasks.pop(index)
        update_task_list()
        messagebox.showinfo("Deleted", f"Task '{deleted['title']}' deleted.")
    else:
        messagebox.showwarning("No Selection", "Select a task to delete.")

# Update selected task
def update_task():
    selected = task_list.selection()
    if selected:
        index = int(task_list.item(selected[0])["values"][0]) - 1
        new_title = title_var.get()
        new_desc = desc_var.get()
        if new_title:
            tasks[index]["title"] = new_title
        if new_desc:
            tasks[index]["description"] = new_desc
        update_task_list()
        title_var.set("")
        desc_var.set("")
        messagebox.showinfo("Updated", "Task updated successfully.")
    else:
        messagebox.showwarning("No Selection", "Select a task to update.")

# Main window
root = tk.Tk()
root.title("✨ Task Manager")
root.geometry("600x400")
root.configure(bg="#f0f4f7")

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
style.configure("Treeview", font=("Segoe UI", 10), rowheight=25)

# Input frame
input_frame = ttk.LabelFrame(root, text="Add / Update Task", padding=10)
input_frame.pack(fill="x", padx=10, pady=10)

title_var = tk.StringVar()
desc_var = tk.StringVar()

ttk.Label(input_frame, text="Title:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
ttk.Entry(input_frame, textvariable=title_var, width=40).grid(row=0, column=1, padx=5, pady=5)

ttk.Label(input_frame, text="Description:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
ttk.Entry(input_frame, textvariable=desc_var, width=40).grid(row=1, column=1, padx=5, pady=5)

ttk.Button(input_frame, text="Add Task", command=add_task).grid(row=2, column=0, padx=5, pady=10)
ttk.Button(input_frame, text="Update Task", command=update_task).grid(row=2, column=1, padx=5, pady=10, sticky="w")

# Task list frame
list_frame = ttk.LabelFrame(root, text="Your Tasks", padding=10)
list_frame.pack(fill="both", expand=True, padx=10, pady=5)

columns = ("#", "Title", "Description")
task_list = ttk.Treeview(list_frame, columns=columns, show="headings")
for col in columns:
    task_list.heading(col, text=col)
    task_list.column(col, anchor="center")

task_list.pack(fill="both", expand=True)

ttk.Button(root, text="Delete Selected Task", command=delete_task).pack(pady=10)

root.mainloop()

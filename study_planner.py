import tkinter as tk
from tkinter import messagebox, ttk
import json, csv
from datetime import datetime, timedelta
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import os

TASK_FILE = "tasks.json"
STUDY_FILE = "Studytime.csv"

def load_tasks():
    try:
        with open(TASK_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_tasks(tasks):
    with open(TASK_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

root = tk.Tk()
root.title("Study Planner & Productivity Tracker")
root.geometry("1200x700")
root.configure(bg="#020617")

sidebar = tk.Frame(root, width=260, bg="#0f172a")
sidebar.pack(side=tk.LEFT, fill=tk.Y)

content = tk.Frame(root, bg="#020617")
content.pack(fill=tk.BOTH, expand=True)

tk.Label(
    content,
    text="Study Planner & Productivity Tracker",
    fg="white",
    bg="#020617",
    font=("Segoe UI", 20, "bold")
).pack(pady=15)

card_frame = tk.Frame(content, bg="#020617")
card_frame.pack(pady=10)

def draw_card(color, title, value):
    frame = tk.Frame(card_frame, bg=color, width=160, height=80)
    frame.pack(side=tk.LEFT, padx=15)
    frame.pack_propagate(False)
    tk.Label(frame, text=title, bg=color, fg="white").pack(pady=5)
    tk.Label(frame, text=value, bg=color, fg="white",
             font=("Segoe UI", 14, "bold")).pack()

def refresh_cards():
    for w in card_frame.winfo_children():
        w.destroy()

    tasks = load_tasks()
    completed = [t for t in tasks if t["status"] == "completed"]

    hours = 0
    try:
        with open(STUDY_FILE, "r") as f:
            reader = csv.DictReader(f)
            for r in reader:
                hours += float(r["Hours"])
    except:
        pass

    draw_card("#22c55e", "Total Tasks", len(tasks))
    draw_card("#f59e0b", "Completed", len(completed))
    draw_card("#6366f1", "Study Hours", f"{hours:.1f}")

refresh_cards()

display = tk.Frame(content, bg="white")
display.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)

def clear_display():
    for w in display.winfo_children():
        w.destroy()

def add_task():
    clear_display()
    tk.Label(display, text="Add Task", font=("Segoe UI", 16)).pack(pady=10)

    title = tk.Entry(display, width=30)
    title.pack(pady=5)

    deadline = tk.Entry(display, width=30)
    deadline.insert(0, "DD-MM-YYYY")
    deadline.pack(pady=5)

    def save():
        tasks = load_tasks()
        tasks.append({
            "id": len(tasks) + 1,
            "title": title.get(),
            "added_date": datetime.now().strftime("%Y-%m-%d"),
            "deadline": deadline.get(),
            "status": "pending"
        })
        save_tasks(tasks)
        refresh_cards()
        messagebox.showinfo("Success", "Task Added")

    tk.Button(display, text="Save Task", command=save).pack(pady=10)

def view_tasks(only_completed=False):
    clear_display()
    tree = ttk.Treeview(display, columns=("ID", "Title", "Status"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Title", text="Title")
    tree.heading("Status", text="Status")
    tree.pack(fill=tk.BOTH, expand=True)

    for t in load_tasks():
        if only_completed and t["status"] != "completed":
            continue
        tree.insert("", tk.END, values=(t["id"], t["title"], t["status"]))

def mark_completed():
    clear_display()
    tk.Label(display, text="Enter Task ID").pack(pady=10)
    entry = tk.Entry(display)
    entry.pack()

    def complete():
        tasks = load_tasks()
        for t in tasks:
            if t["id"] == int(entry.get()):
                t["status"] = "completed"
                save_tasks(tasks)
                refresh_cards()
                messagebox.showinfo("Done", "Task Completed")
                return
        messagebox.showerror("Error", "Task Not Found")

    tk.Button(display, text="Mark Completed", command=complete).pack(pady=10)

def delete_task():
    clear_display()
    tk.Label(display, text="Enter Task ID").pack(pady=10)
    entry = tk.Entry(display)
    entry.pack()

    def delete():
        tasks = [t for t in load_tasks() if t["id"] != int(entry.get())]
        for i, t in enumerate(tasks):
            t["id"] = i + 1
        save_tasks(tasks)
        refresh_cards()
        messagebox.showinfo("Deleted", "Task Removed")

    tk.Button(display, text="Delete Task", command=delete).pack(pady=10)

def log_study_time():
    clear_display()
    tk.Label(display, text="Log Study Time", font=("Segoe UI", 16)).pack(pady=10)

    hours_entry = tk.Entry(display)
    hours_entry.pack(pady=5)
    hours_entry.insert(0, "Hours")

    category = tk.StringVar(value="Python")
    ttk.Combobox(display, textvariable=category,
                 values=["Python", "DSA", "GATE", "Project", "Others"],
                 state="readonly").pack(pady=5)

    def save():
        try:
            hrs = float(hours_entry.get())
            with open(STUDY_FILE, "a", newline="") as f:
                writer = csv.writer(f)
                if f.tell() == 0:
                    writer.writerow(["Date", "Category", "Hours"])
                writer.writerow([
                    datetime.now().strftime("%Y-%m-%d"),
                    category.get(),
                    hrs
                ])
            refresh_cards()
            weekly_analytics()
            messagebox.showinfo("Saved", "Study Time Logged")
        except:
            messagebox.showerror("Error", "Invalid input")

    tk.Button(display, text="Save", command=save).pack(pady=10)
    
def weekly_analytics():
    clear_display()
    data = {}

    try:
        with open(STUDY_FILE, "r") as f:
            reader = csv.DictReader(f)
            last_7 = datetime.now() - timedelta(days=7)
            for r in reader:
                d = datetime.strptime(r["Date"], "%Y-%m-%d")
                if d >= last_7:
                    data[r["Category"]] = data.get(r["Category"], 0) + float(r["Hours"])
    except:
        pass

    if not data:
        tk.Label(display, text="No data for last 7 days").pack()
        return

    fig = Figure(figsize=(7,4))
    ax = fig.add_subplot(111)
    ax.bar(data.keys(), data.values())
    ax.set_title("Weekly Study Analytics")

    canvas = FigureCanvasTkAgg(fig, display)
    canvas.draw()
    canvas.get_tk_widget().pack()

def side_btn(text, cmd):
    tk.Button(sidebar, text=text, command=cmd,
              bg="#1e293b", fg="white",
              height=2).pack(fill=tk.X, padx=20, pady=6)

side_btn("Add Task", add_task)
side_btn("View All Tasks", lambda: view_tasks(False))
side_btn("View Completed Tasks", lambda: view_tasks(True))
side_btn("Mark Task Completed", mark_completed)
side_btn("Delete Task", delete_task)
side_btn("Log Study Time", log_study_time)
side_btn("Weekly Analytics", weekly_analytics)
side_btn("Exit", root.destroy)

weekly_analytics()
root.mainloop()

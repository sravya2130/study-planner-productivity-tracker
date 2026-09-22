import json
import csv
import matplotlib.pyplot as plt
from datetime import timedelta
from datetime import datetime
TASK_FILE = "tasks.json"
STUDY_FILE = "Studytime.csv"

#opens json file to save added tasks
def existing_tasks():
    try:
        with open(TASK_FILE, "r") as f:
            return json.load(f)
    except:
        return []
    
#added tasks are saved in json
def save_tasks(tasks):
    with open(TASK_FILE, "w") as f:
        json.dump(tasks, f, indent=4)
        
#to added tasks
def addtask():
    tasks = existing_tasks()

    title = input("Enter task title: ")

    if not title.strip():
        print("Task title cannot be empty.")
        return

    input_date = input("Enter deadline (DD-MM-YYYY): ")

    try:
        input_datetime = datetime.strptime(input_date, "%d-%m-%Y")
    except ValueError:
        print("Invalid date format.")
        return

    if input_datetime < datetime.now():
        print("Deadline cannot be in the past.")
        return

    added_date = datetime.now().strftime("%Y-%m-%d")

    new_id = max([task["id"] for task in tasks], default=0) + 1

    task = {
        "id": new_id,
        "title": title.strip(),
        "added_date": added_date,
        "deadline": input_date,
        "status": "pending"
    }

    tasks.append(task)
    save_tasks(tasks)

    print("Task added successfully!")

#to view all the existing tasks
def viewtasks():
    tasks=existing_tasks()
    if not tasks:
        print("task not found")
        return
    print("all tasks ")
    for task in tasks:
        print(f"ID            : {task['id']}")
        print(f"Title         : {task['title']}")
        print(f"Task Added On : {task.get('added_date', 'N/A')}")
        print(f"Deadline      : {task['deadline']}")
        print(f"Status        : {task['status'].capitalize()}")
        print("-" * 30)

#to know which tasks are completed
def viewcompletedtasks():
    tasks=existing_tasks()
    complete=[task for task in tasks if task["status"]=="completed"]
    if not complete:
        print("no completed tasks yet")
        return
    print("completed tasks")
    for task in complete:
        print(f"ID       : {task['id']}")
        print(f"Title    : {task['title']}")
        print(f"Task Added On : {task.get('added_date', 'N/A')}")
        print(f"Deadline : {task['deadline']}")
        print("-" * 30)

#to mark task completed if done doing
def completetask():
    tasks = existing_tasks()
    if not tasks:
        print("no task available")
        return
    id = int(input("enter task id to mark as completed: "))
    for task in tasks:
        if task["id"] == id:
            task["status"] = "completed"
            save_tasks(tasks)
            print("task marked as completed")
            return
    print("task not found")

#to remove task 
def deltask():
    tasks=existing_tasks()
    if not tasks:
        print("no task to delete")
        return   
    id=int(input("enter task id to delete: "))
    for task in tasks:
        if task["id"]==id:
            tasks.remove(task)
            save_tasks(tasks)
            print("task deleted successfully!")
            return
    print("task id not found")

#to add num of hours spent for a perticular task
def time():
    studyhr=float(input("Enter study hours"))
    if studyhr<= 0:
        print("Study hours must be positive ")
        return 
    print("Select category:" )
    print("1.pyhton \n2.DSA \n3.GATE \n4.Project \n5.Others")
    choice=input("Enter Category number: ")
    if choice == "1":
           category = "python"
    elif choice =="2":
           category = "DSA"
    elif choice == "3":
           category = "GATE"
    elif choice == "4":
           category = "Project"
    elif choice == "5":
           category = "Others"
    else:
           print("Invaild category choice.")
           return
    date = datetime.now().strftime("%Y-%m-%d")
    with open(STUDY_FILE, "a", newline="") as f:
        writer=csv.writer(f)
        if f.tell() == 0:
            writer.writerow(["Date","Category","Hours"])
        writer.writerow([date,category,studyhr])
    print("Study time logged successfully")

def weekly_analytics():
    try:
        with open(STUDY_FILE, "r") as f:
            reader = csv.DictReader(f)
            last_7_days = datetime.now() - timedelta(days=7)
            summary = {}
            for row in reader:
                date = datetime.strptime(row["Date"], "%Y-%m-%d")
                if date >= last_7_days:
                    category = row["Category"]
                    hours = float(row["Hours"])
                    summary[category] = summary.get(category, 0) + hours
        if not summary:
            print("No data for last 7 days")
            return
        categories = list(summary.keys())
        hours = list(summary.values())

        plt.bar(categories, hours)
        plt.xlabel("Category")
        plt.ylabel("Study Hours")
        plt.title("Weekly Study Analytics")
        plt.show()

    except FileNotFoundError:
        print("No study data found")

def load_users():
    try:
        with open("users.json", "r") as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f, indent=4)

def register():
    username = input("Enter username: ")
    password = input("Enter password: ")

    users = load_users()

    if username in users:
        print("User already exists")
        return

    users[username] = {"password": password}
    save_users(users)

    print("Registration successful")

def login():
    username = input("Username: ")
    password = input("Password: ")

    users = load_users()

    if username in users and users[username]["password"] == password:
        print("Login successful")
        return username
    else:
        print("Invalid credentials")
        return None


#the opening menu         
def menu():
    print("\nSTUDY PLANNER & PRODUCTIVITY TRACKER")
    print("1. Add Study Task")
    print("2. View all Tasks")
    print("3. View completed task")
    print("4. Mark task as completed")
    print("5. Delete task")
    print("6. Log Study Time")
    print("7. Weekly Analytics")
    print("8. Exit")

current_user = None

while current_user is None:
    print("1. Login")
    print("2. Register")
    print("3. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        current_user = login()

    if current_user:
        TASK_FILE = f"{current_user}_tasks.json"
        STUDY_FILE = f"{current_user}_Studytime.csv"

    elif choice == "2":
        register()
    elif choice == "3":
        exit()
    else:
        print("Invalid choice")

while True:
    menu()
    choice = input("Enter your choice: ")
    if choice == "1":
        addtask()
    elif choice=="2":
        viewtasks()
    elif choice == "3":
        viewcompletedtasks()
    elif choice == "4":
        completetask()
    elif choice == "5":
        deltask()
    elif choice == "6":
        time()
    elif choice == "7":
        weekly_analytics()
    elif choice == "8":
        print("Exiting... Byeeee...!")
        break
    else:
        print("Invalid choice. Try again.")
import tkinter as tk
from tkinter import ttk, messagebox
import csv

class FileManager:
    def __init__(self, file_name, fieldnames):
        self.file_name = file_name
        self.fieldnames = fieldnames

    def load_data(self):
        data = []
        try:
            with open(self.file_name, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    data.append(row)
        except FileNotFoundError:
            pass
        return data

    def save_data(self, data):
        with open(self.file_name, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            writer.writeheader()
            writer.writerows(data)

class UserManager:
    def __init__(self, file_name):
        self.file_manager = FileManager(file_name, ["username", "password"])
        self.users = self.file_manager.load_data()

    def register_user(self, username, password, confirm_password):
        for user in self.users:
            if user['username'] == username:
                return "Username sudah terdaftar."
        if password != confirm_password:
            return "Password tidak cocok."
        new_user = {"username": username, "password": password}
        self.users.append(new_user)
        self.file_manager.save_data(self.users)
        return "Registrasi berhasil."

    def login_user(self, username, password):
        for user in self.users:
            if user['username'] == username and user['password'] == password:
                return True
        return False

class Activity:
    def __init__(self, file_name, fieldnames):
        self.file_manager = FileManager(file_name, fieldnames)
        self.data = self.file_manager.load_data()

    def add_item(self, **kwargs):
        new_item = {"id": str(len(self.data) + 1), **kwargs}
        self.data.append(new_item)
        self.file_manager.save_data(self.data)

    def view_items(self):
        return self.data

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi GUI")
        self.root.geometry("600x400")
        self.root.configure(bg="#f0f0f0")  # Warna latar belakang

        # Styling
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Arial", 12), padding=5)
        self.style.configure("TLabel", font=("Arial", 12), background="#f0f0f0")
        self.style.configure("TFrame", background="#f0f0f0")

        self.user_manager = UserManager('users.csv')
        self.activities = {
            "Tempat": Activity('place_activity.csv', ["id", "name", "description"]),
            "Event": Activity('event_activity.csv', ["id", "name", "date"]),
            "Galeri": Activity('gallery_activity.csv', ["id", "title", "file_name"]),
            "Oleh-Oleh": Activity('oleh_oleh_activity.csv', ["id", "store_name", "item"]),
            "Transportasi": Activity('transport_activity.csv', ["id", "name", "price"]),
            "Hotel": Activity('hotel_activity.csv', ["id", "name", "price"]),
            "Layanan Publik": Activity('public_service.csv', ["id", "service_name"]),
            "Restoran": Activity('restaurant_activity.csv', ["id", "name", "price"]),
            "Wisata": Activity('tourism_activity.csv', ["id", "name", "type"])
        }
        self.show_login()

    def show_login(self):
        self.clear_frame()
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True)

        ttk.Label(frame, text="Login", font=("Arial", 16)).pack(pady=10)
        ttk.Label(frame, text="Username:").pack()
        self.username_entry = ttk.Entry(frame)
        self.username_entry.pack()

        ttk.Label(frame, text="Password:").pack()
        self.password_entry = ttk.Entry(frame, show="*")
        self.password_entry.pack()

        ttk.Button(frame, text="Login", command=self.login).pack(pady=5)
        ttk.Button(frame, text="Register", command=self.show_register).pack()

    def show_register(self):
        self.clear_frame()
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True)

        ttk.Label(frame, text="Register", font=("Arial", 16)).pack(pady=10)
        ttk.Label(frame, text="Username:").pack()
        self.username_entry = ttk.Entry(frame)
        self.username_entry.pack()

        ttk.Label(frame, text="Password:").pack()
        self.password_entry = ttk.Entry(frame, show="*")
        self.password_entry.pack()

        ttk.Label(frame, text="Confirm Password:").pack()
        self.confirm_password_entry = ttk.Entry(frame, show="*")
        self.confirm_password_entry.pack()

        ttk.Button(frame, text="Register", command=self.register).pack(pady=5)
        ttk.Button(frame, text="Back to Login", command=self.show_login).pack()

    def show_main_menu(self):
        self.clear_frame()
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True)

        ttk.Label(frame, text="Main Menu", font=("Arial", 16)).pack(pady=10)
        ttk.Button(frame, text="Categories", command=self.show_categories).pack(pady=5)
        ttk.Button(frame, text="Logout", command=self.show_login).pack(pady=5)

    def show_categories(self):
        self.clear_frame()
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True)

        ttk.Label(frame, text="Categories", font=("Arial", 16)).pack(pady=10)
        for category in self.activities:
            ttk.Button(frame, text=category, command=lambda c=category: self.show_activity(c)).pack(pady=2)
        ttk.Button(frame, text="Back", command=self.show_main_menu).pack(pady=5)

    def show_activity(self, category):
        self.clear_frame()
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True)

        ttk.Label(frame, text=f"Activity: {category}", font=("Arial", 16)).pack(pady=10)
        activity = self.activities[category]
        items = activity.view_items()

        listbox = tk.Listbox(frame, width=50, height=10)
        for item in items:
            listbox.insert(tk.END, ", ".join(f"{k}: {v}" for k, v in item.items()))
        listbox.pack()

        ttk.Button(frame, text="Add Item", command=lambda: self.add_activity(category)).pack(pady=5)
        ttk.Button(frame, text="Back", command=self.show_categories).pack(pady=5)

    def add_activity(self, category):
        self.clear_frame()
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True)

        ttk.Label(frame, text=f"Add {category}", font=("Arial", 16)).pack(pady=10)
        activity = self.activities[category]
        self.entries = {}
        for field in activity.file_manager.fieldnames[1:]:
            ttk.Label(frame, text=f"{field.capitalize()}:").pack()
            entry = ttk.Entry(frame)
            entry.pack()
            self.entries[field] = entry

        ttk.Button(frame, text="Save", command=lambda: self.save_activity(category)).pack(pady=5)
        ttk.Button(frame, text="Back", command=lambda: self.show_activity(category)).pack(pady=5)

    def save_activity(self, category):
        activity = self.activities[category]
        data = {field: entry.get() for field, entry in self.entries.items()}
        activity.add_item(**data)
        messagebox.showinfo("Success", f"{category} added successfully!")
        self.show_activity(category)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.user_manager.login_user(username, password):
            self.show_main_menu()
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        result = self.user_manager.register_user(username, password, confirm_password)
        messagebox.showinfo("Info", result)
        if result == "Registrasi berhasil.":
            self.show_login()

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()

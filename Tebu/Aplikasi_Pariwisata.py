import time
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

    def register_user(self):
        print("=== Registrasi ===")
        username = input("Masukkan Username: ")
        for user in self.users:
            if user['username'] == username:
                print("Username sudah terdaftar. Silakan gunakan username lain.\n")
                return False
        password = input("Masukkan Password: ")
        confirm_password = input("Konfirmasi Password: ")
        if password != confirm_password:
            print("Password tidak cocok. Registrasi gagal.\n")
            return False
        new_user = {"username": username, "password": password}
        self.users.append(new_user)
        self.file_manager.save_data(self.users)
        print("Registrasi berhasil! Silakan login.\n")
        return True

    def login_user(self):
        print("=== Login ===")
        username = input("Masukkan Username: ")
        password = input("Masukkan Password: ")
        for user in self.users:
            if user['username'] == username and user['password'] == password:
                print("Login berhasil!\n")
                return True
        print("Login gagal. Username atau password salah.\n")
        return False

class Activity:
    def __init__(self, file_name, fieldnames):
        self.file_manager = FileManager(file_name, fieldnames)
        self.data = self.file_manager.load_data()

    def add_item(self, **kwargs):
        new_item = {"id": str(len(self.data) + 1), **kwargs}
        self.data.append(new_item)
        self.file_manager.save_data(self.data)
        print(f"{kwargs.get('name', 'Item')} berhasil ditambahkan!")

    def view_items(self):
        if not self.data:
            print("Tidak ada data.\n")
        else:
            for item in self.data:
                print(", ".join(f"{key}: {value}" for key, value in item.items()))

class MainMenu:
    def __init__(self):
        self.user_manager = UserManager('users.csv')
        self.activities = {
            "1": Activity('place_activity.csv', ["id", "name", "description"]),
            "2": Activity('event_activity.csv', ["id", "name", "date"]),
            "3": Activity('gallery_activity.csv', ["id", "title", "file_name"]),
            "4": Activity('oleh_oleh_activity.csv', ["id", "store_name", "item"]),
            "5": Activity('transport_activity.csv', ["id", "name", "price"]),
            "6": Activity('hotel_activity.csv', ["id", "name", "price"]),
            "7": Activity('public_service.csv', ["id", "service_name"]),
            "8": Activity('restaurant_activity.csv', ["id", "name", "price"]),
            "9": Activity('tourism_activity.csv', ["id", "name", "type"])
        }

    def splash_activity(self):
        waktu = 4000
        print("=== Selamat Datang di Aplikasi ===")
        time.sleep(waktu / 1000)
        print("Memulai aplikasi...\n")

    def main_menu(self):
        while True:
            print("\n=== Main Menu ===")
            print("1. HOME")
            print("2. CATEGORIES")
            print("3. SETTINGS")
            print("4. LOGOUT")
            choice = input("Pilih menu: ")
            if choice == "1":
                print("Anda berada di menu HOME.\n")
            elif choice == "2":
                self.categories_menu()
            elif choice == "3":
                self.settings_menu()
            elif choice == "4":
                print("Logout berhasil. Sampai jumpa!\n")
                break
            else:
                print("Pilihan tidak valid.\n")

    def categories_menu(self):
        while True:
            print("\n=== Kategori ===")
            print("1. Tempat")
            print("2. Event")
            print("3. Galeri")
            print("4. Oleh-Oleh")
            print("5. Transportasi + Harga")
            print("6. Hotel + Harga")
            print("7. Layanan Publik")
            print("8. Restoran + Harga")
            print("9. Wisata (Alam, Belanja, Buatan, Budaya, Sejarah)")
            print("10. Kembali ke Menu Utama")
            choice = input("Pilih kategori: ")
            if choice in self.activities:
                self.activity_menu(self.activities[choice])
            elif choice == "10":
                break
            else:
                print("Pilihan tidak valid.\n")

    def activity_menu(self, activity):
        while True:
            print("\n=== Activity Menu ===")
            print("1. Tambah Data")
            print("2. Lihat Data")
            print("3. Kembali")
            choice = input("Pilih menu: ")
            if choice == "1":
                kwargs = {}
                for field in activity.file_manager.fieldnames[1:]:
                    kwargs[field] = input(f"Masukkan {field}: ")
                activity.add_item(**kwargs)
            elif choice == "2":
                activity.view_items()
            elif choice == "3":
                break
            else:
                print("Pilihan tidak valid.\n")

    def settings_menu(self):
        print("\n=== Settings ===")
        print("1. Ubah preferensi")
        print("2. Kelola akun")
        print("3. Kembali")
        choice = input("Pilih menu: ")
        if choice == "1":
            print("Fitur ubah preferensi belum tersedia.")
        elif choice == "2":
            print("Fitur kelola akun belum tersedia.")
        elif choice == "3":
            return
        else:
            print("Pilihan tidak valid.")

    def run(self):
        self.splash_activity()
        while True:
            print("1. Login")
            print("2. Registrasi")
            print("3. Keluar")
            choice = input("Pilih menu: ")
            if choice == "1":
                if self.user_manager.login_user():
                    self.main_menu()
            elif choice == "2":
                self.user_manager.register_user()
            elif choice == "3":
                print("Terima kasih telah menggunakan aplikasi ini. Sampai jumpa!\n")
                break
            else:
                print("Pilihan tidak valid.\n")

if __name__ == "__main__":
    MainMenu().run()

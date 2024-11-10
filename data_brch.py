import os
import base64
import tkinter as tk
from tkinter import messagebox
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import hashlib

# Data Breach Prevention with AES Encryption
class DataSecurity:
    def __init__(self):
        self.key = self.load_key()

    def load_key(self):
        key_path = "data_key.bin"
        if os.path.exists(key_path):
            with open(key_path, 'rb') as file:
                return file.read()
        else:
            key = get_random_bytes(16)
            with open(key_path, 'wb') as file:
                file.write(key)
            return key

    def encrypt_data(self, data):
        cipher = AES.new(self.key, AES.MODE_EAX)
        nonce = cipher.nonce
        ciphertext, tag = cipher.encrypt_and_digest(data.encode())
        return base64.b64encode(nonce + ciphertext).decode()

    def decrypt_data(self, encrypted_data):
        decoded_data = base64.b64decode(encrypted_data)
        nonce = decoded_data[:16]
        ciphertext = decoded_data[16:]
        cipher = AES.new(self.key, AES.MODE_EAX, nonce=nonce)
        return cipher.decrypt(ciphertext).decode()

# Unauthorized Access Logging and Detection
class AccessMonitor:
    def __init__(self):
        self.access_log = []

    def log_access(self, access_type, status):
        log_entry = {
            "access_type": access_type,
            "status": status,
            "alert": "Unauthorized Access Detected!" if status == "Unauthorized" else "Access Granted"
        }
        self.access_log.append(log_entry)
        return log_entry["alert"]

# GUI for Data Encryption and Access Monitoring
class DataBreachApp:
    def __init__(self, root):
        self.security = DataSecurity()
        self.monitor = AccessMonitor()
        self.root = root
        self.root.title("Data Breach Prevention Framework")

        # GUI Elements
        tk.Label(root, text="Enter Sensitive Data:").grid(row=0, column=0, padx=5, pady=5)
        self.data_entry = tk.Entry(root, width=30)
        self.data_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(root, text="Attempt Access:").grid(row=1, column=0, padx=5, pady=5)
        self.access_type_entry = tk.Entry(root, width=30)
        self.access_type_entry.grid(row=1, column=1, padx=5, pady=5)

        self.save_button = tk.Button(root, text="Encrypt & Save Data", command=self.encrypt_and_save_data)
        self.save_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.access_button = tk.Button(root, text="Attempt Access", command=self.attempt_access)
        self.access_button.grid(row=3, column=0, columnspan=2, pady=10)

    def encrypt_and_save_data(self):
        data = self.data_entry.get()
        if not data:
            messagebox.showwarning("Input Error", "Please enter data to save!")
            return

        encrypted_data = self.security.encrypt_data(data)
        with open("secure_data.txt", "w") as f:
            f.write(encrypted_data)
        messagebox.showinfo("Data Saved", "Data has been encrypted and saved securely.")

    def attempt_access(self):
        access_type = self.access_type_entry.get()
        if access_type != "Authorized":
            alert = self.monitor.log_access(access_type, "Unauthorized")
            messagebox.showwarning("Access Alert", alert)
        else:
            alert = self.monitor.log_access(access_type, "Authorized")
            messagebox.showinfo("Access Granted", alert)

# Run the application
root = tk.Tk()
app = DataBreachApp(root)
root.mainloop()

import socket
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import hashlib
import os
import tkinter as tk
from tkinter import messagebox

# Key management and secure storage
class IoTDeviceSecurity:
    def __init__(self):
        self.key = self.load_key()

    def load_key(self):
        key_path = "aes_key.bin"
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

# IoT Communication with Authentication and Secure Data Exchange
class IoTCommunication:
    def __init__(self, authorized_devices):
        self.security = IoTDeviceSecurity()
        self.authorized_devices = authorized_devices  # List of authorized devices

    def authenticate_device(self, device_id, shared_secret):
        # Authenticate device using its ID and shared secret
        combined = f"{device_id}:{shared_secret}".encode()
        return hashlib.sha256(combined).hexdigest()

    def check_authorization(self, device_id):
        # Check if device ID is in the list of authorized devices
        if device_id in self.authorized_devices:
            return True
        else:
            return False

    def send_data(self, device_id, shared_secret, data):
        # If the device is authorized, send encrypted data
        if self.check_authorization(device_id):
            auth_token = self.authenticate_device(device_id, shared_secret)
            encrypted_data = self.security.encrypt_data(data)
            return auth_token, encrypted_data, None  # No error
        else:
            # If device is unauthorized, return an error
            return None, None, "Unauthorized device access attempt!"

    def receive_data(self, encrypted_data):
        try:
            decrypted_data = self.security.decrypt_data(encrypted_data)
            return decrypted_data
        except Exception as e:
            return f"Decryption Failed: {e}"

# GUI Application using tkinter
class IoTSecurityApp:
    def __init__(self, root):
        self.comm = IoTCommunication(authorized_devices=["Device123", "456"])  # Authorized devices
        self.root = root
        self.root.title("IoT Device Security Framework")

        # GUI Elements
        self.device_id_label = tk.Label(root, text="Device ID:")
        self.device_id_label.grid(row=0, column=0, padx=5, pady=5)
        self.device_id_entry = tk.Entry(root, width=30)
        self.device_id_entry.grid(row=0, column=1, padx=5, pady=5)

        self.secret_label = tk.Label(root, text="Shared Secret:")
        self.secret_label.grid(row=1, column=0, padx=5, pady=5)
        self.secret_entry = tk.Entry(root, show="*", width=30)
        self.secret_entry.grid(row=1, column=1, padx=5, pady=5)

        self.data_label = tk.Label(root, text="Data to Send:")
        self.data_label.grid(row=2, column=0, padx=5, pady=5)
        self.data_entry = tk.Entry(root, width=30)
        self.data_entry.grid(row=2, column=1, padx=5, pady=5)

        self.send_button = tk.Button(root, text="Send Data", command=self.send_data)
        self.send_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.output_label = tk.Label(root, text="Received (Decrypted) Data:")
        self.output_label.grid(row=4, column=0, padx=5, pady=5)
        self.output_text = tk.Text(root, height=5, width=40)
        self.output_text.grid(row=4, column=1, padx=5, pady=5)

    def send_data(self):
        device_id = self.device_id_entry.get()
        shared_secret = self.secret_entry.get()
        data = self.data_entry.get()

        if not device_id or not shared_secret or not data:
            messagebox.showwarning("Input Error", "Please fill all fields!")
            return

        # Send data securely after authentication
        auth_token, encrypted_data, error = self.comm.send_data(device_id, shared_secret, data)
        
        if error:
            messagebox.showerror("Unauthorized Access", error)
            return

        messagebox.showinfo("Data Sent", f"Auth Token: {auth_token}\nEncrypted Data: {encrypted_data}")

        # Receive and decrypt data
        decrypted_data = self.comm.receive_data(encrypted_data)
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, decrypted_data)

# Run the application
root = tk.Tk()
app = IoTSecurityApp(root)
root.mainloop()

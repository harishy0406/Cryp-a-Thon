import time
import tkinter as tk
from tkinter import messagebox

# DDoS Prevention System
class DDOSPrevention:
    def __init__(self, rate_limit, time_window):
        self.rate_limit = rate_limit
        self.time_window = time_window
        self.request_timestamps = []

    def check_request(self):
        current_time = time.time()
        # Filter timestamps that are within the time window
        self.request_timestamps = [t for t in self.request_timestamps if current_time - t < self.time_window]

        if len(self.request_timestamps) < self.rate_limit:
            self.request_timestamps.append(current_time)
            return "Request Allowed"
        else:
            return "DDoS Alert: Rate Limit Exceeded"

# GUI to simulate DDoS attack detection
class DDOSApp:
    def __init__(self, root):
        self.ddos_system = DDOSPrevention(rate_limit=5, time_window=10)  # 5 requests per 10 seconds
        self.root = root
        self.root.title("DDoS Mitigation Simulation")

        # GUI Elements
        self.request_button = tk.Button(root, text="Send Request", command=self.send_request)
        self.request_button.grid(row=0, column=0, padx=10, pady=10)

        self.output_text = tk.Text(root, height=10, width=40)
        self.output_text.grid(row=1, column=0, padx=10, pady=10)

    def send_request(self):
        status = self.ddos_system.check_request()
        self.output_text.insert(tk.END, f"Request Status: {status}\n")
        if "DDoS Alert" in status:
            messagebox.showwarning("DDoS Alert", "Potential DDoS attack detected!")

# Run the application
root = tk.Tk()
app = DDOSApp(root)
root.mainloop()

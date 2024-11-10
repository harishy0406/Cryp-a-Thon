import os
import logging
import requests
from tkinter import *
from tkinter import messagebox, scrolledtext
from ratelimit import limits, sleep_and_retry
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("THIRD_PARTY_API_KEY")
API_URL = os.getenv("API_URL")

# Configure logging
logging.basicConfig(filename="api_access.log", level=logging.INFO)

# Rate limiting configuration: 5 requests per minute
@sleep_and_retry
@limits(calls=5, period=60)
def fetch_data_with_security(city):
    try:
        # Parameters for the weather API request
        params = {
            "key": API_KEY,
            "q": city,
            "aqi": "no"
        }
        
        # Make a secure HTTPS request
        response = requests.get(API_URL, params=params)
        
        # Log the API access
        logging.info(f"API request made to {API_URL} with status code {response.status_code}")
        
        # Raise an error for non-200 responses
        response.raise_for_status()
        
        # Validate and return data
        data = response.json()
        if not validate_data(data):
            raise ValueError("Data validation failed")
        
        return data

    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
        messagebox.showerror("Error", f"HTTP error: {http_err}")
    except requests.exceptions.RequestException as req_err:
        logging.error(f"Request error occurred: {req_err}")
        messagebox.showerror("Error", f"Request error: {req_err}")
    except Exception as err:
        logging.error(f"Other error occurred: {err}")
        messagebox.showerror("Error", f"An error occurred: {err}")

# Data validation function to verify expected keys in response
def validate_data(data):
    # Validate if the essential keys exist in the response
    required_keys = ["location", "current"]  # Updated based on typical weather API response
    return all(key in data for key in required_keys)

# Function to fetch data and display it in the GUI
def fetch_and_display_data():
    city = city_entry.get()
    if city:
        data = fetch_data_with_security(city)
        if data:
            result_text.delete(1.0, END)  # Clear previous data
            result_text.insert(END, str(data))  # Display new data
    else:
        messagebox.showerror("Input Error", "Please enter a city name")

# Create GUI with Tkinter
root = Tk()
root.title("Weather Data Fetcher")
root.geometry("600x400")

# Title label
Label(root, text="Weather Data Fetcher", font=("Arial", 16)).pack(pady=10)

# Input for city name
Label(root, text="Enter City Name:", font=("Arial", 12)).pack(pady=5)
city_entry = Entry(root, font=("Arial", 12))
city_entry.pack(pady=5)

# Fetch data button
fetch_button = Button(root, text="Fetch Weather Data", font=("Arial", 12), command=fetch_and_display_data)
fetch_button.pack(pady=5)

# Text area to display fetched data
result_text = scrolledtext.ScrolledText(root, width=70, height=15, font=("Arial", 10))
result_text.pack(pady=10)

# Run the main Tkinter loop
root.mainloop()
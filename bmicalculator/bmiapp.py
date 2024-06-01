import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json
import os

DATA_FILENAME = "bmi_records.json"

class BMIApp:
    def __init__(self, root):
        self.user_data = self.load_user_data()
        self.root = root
        self.root.title("BMI Tracker by Aryan Roshan")

        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(self.main_frame, text="Username:").grid(row=0, column=0, sticky=tk.W)
        self.username_entry = ttk.Entry(self.main_frame, width=25)
        self.username_entry.grid(row=0, column=1, sticky=tk.E)

        ttk.Label(self.main_frame, text="Weight (kg):").grid(row=1, column=0, sticky=tk.W)
        self.weight_entry = ttk.Entry(self.main_frame, width=25)
        self.weight_entry.grid(row=1, column=1, sticky=tk.E)

        ttk.Label(self.main_frame, text="Height (m):").grid(row=2, column=0, sticky=tk.W)
        self.height_entry = ttk.Entry(self.main_frame, width=25)
        self.height_entry.grid(row=2, column=1, sticky=tk.E)

        ttk.Button(self.main_frame, text="Add Entry", command=self.add_entry).grid(row=3, column=0, sticky=tk.W)
        ttk.Button(self.main_frame, text="View History", command=self.show_history).grid(row=3, column=1, sticky=tk.W)
        ttk.Button(self.main_frame, text="Plot Trend", command=self.plot_bmi_trend).grid(row=3, column=1, sticky=tk.E)
        ttk.Button(self.main_frame, text="Reset", command=self.reset_fields).grid(row=3, column=2, sticky=tk.E)

    def load_user_data(self):
        if os.path.exists(DATA_FILENAME):
            with open(DATA_FILENAME, "r") as file:
                return json.load(file)
        return {}

    def save_user_data(self):
        with open(DATA_FILENAME, "w") as file:
            json.dump(self.user_data, file)

    def calculate_bmi(self, weight, height):
        bmi = weight / (height ** 2)
        return bmi
    
    def get_category(self, bmi):
        if bmi < 18.5:
            category = "Underweight"
        elif 18.5 <= bmi < 24.9:
            category = "Normal weight"
        elif 25 <= bmi < 29.9:
            category = "Overweight"
        else:
            category =  "Obesity"
        return category

    def add_entry(self):
        try:
            username = self.username_entry.get().strip()
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get())

            if not username:
                raise ValueError("Username cannot be empty")

            bmi = self.compute_bmi(weight, height)
            category = self.get_bmi_category(bmi)

            if username not in self.user_data:
                self.user_data[username] = []

            self.user_data[username].append({"weight": weight, "height": height, "bmi": bmi, "category": category})
            self.save_user_data()

            messagebox.showinfo("BMI Result", f"BMI: {bmi:.2f}\nCategory: {category}")
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))

    def show_history(self):
        username = self.username_entry.get().strip()
        if username not in self.user_data:
            messagebox.showerror("Error", "No data found for this user.")
            return

        history = self.user_data[username]
        history_text = "\n".join([f"Weight: {entry['weight']} kg, Height: {entry['height']} m, BMI: {entry['bmi']:.2f}, Category: {entry['category']}" for entry in history])

        history_window = tk.Toplevel(self.root)
        history_window.title(f"{username}'s BMI History")
        history_textbox = ScrolledText(history_window, width=50, height=20)
        history_textbox.pack()
        history_textbox.insert(tk.END, history)
        history_textbox.config(state=tk.DISABLED)

    def plot_bmi_trend(self):
        username = self.username_entry.get().strip()
        if username not in self.user_data:
            messagebox.showerror("Error", "No data found for this user.")
            return

        history = self.user_data[username]
        entries = range(len(history))
        bmis = [entry['bmi'] for entry in history]

        fig, ax = plt.subplots()
        ax.plot(entries, bmis, marker='o')
        ax.set_xlabel('Entry Number')
        ax.set_ylabel('BMI')
        ax.set_title(f"{username}'s BMI Trend")

        trend_window = tk.Toplevel(self.root)
        trend_window.title(f"{username}'s BMI Trend")

        canvas = FigureCanvasTkAgg(fig, master=trend_window)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def reset_fields(self):
        username = self.username_entry.get().strip()
        if username in self.user_data:
            del self.user_data[username]
            self.save_user_data()
            messagebox.showinfo("Reset", f"Data for '{username}' has been reset.")
        else:
            messagebox.showerror("Error", "No data found for this user.")

        self.username_entry.delete(0, tk.END)
        self.weight_entry.delete(0, tk.END)
        self.height_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = BMIApp(root)
    root.mainloop()

import tkinter as tk
from tkinter import messagebox
import sqlite3
from matplotlib import pyplot as plt

# Create SQLite database and table
conn = sqlite3.connect('bmi.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY, username TEXT, password TEXT, weight REAL, height REAL)''')
conn.commit()

# Initialize Tkinter app
root = tk.Tk()
root.title("BMI Calculator")

def register():
    def submit_registration():
        username = username_entry.get()
        password = password_entry.get()
        c.execute("INSERT INTO users (username, password, weight, height) VALUES (?, ?, 0, 0)", (username, password))
        conn.commit()
        messagebox.showinfo("Registration", "Registration successful. Please login.")
        registration_window.destroy()

    registration_window = tk.Toplevel(root)
    registration_window.title("Register")
    tk.Label(registration_window, text="Username:").pack()
    username_entry = tk.Entry(registration_window)
    username_entry.pack()
    tk.Label(registration_window, text="Password:").pack()
    password_entry = tk.Entry(registration_window, show="*")
    password_entry.pack()
    tk.Button(registration_window, text="Register", command=submit_registration).pack()

def login():
    def submit_login():
        username = username_entry.get()
        password = password_entry.get()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        if user:
            current_user.set(user[1])
            login_window.destroy()
            calculate_bmi()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    login_window = tk.Toplevel(root)
    login_window.title("Login")
    tk.Label(login_window, text="Username:").pack()
    username_entry = tk.Entry(login_window)
    username_entry.pack()
    tk.Label(login_window, text="Password:").pack()
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack()
    tk.Button(login_window, text="Login", command=submit_login).pack()

def calculate_bmi():
    def calculate():
        weight = float(weight_entry.get())
        height = float(height_entry.get())
        bmi = weight / (height ** 2)
        c.execute("UPDATE users SET weight=?, height=? WHERE username=?", (weight, height, current_user.get()))
        conn.commit()
        messagebox.showinfo("BMI Result", f"Your BMI is {bmi:.2f}")

    bmi_window = tk.Toplevel(root)
    bmi_window.title("BMI Calculator")
    tk.Label(bmi_window, text="Weight (kg):").pack()
    weight_entry = tk.Entry(bmi_window)
    weight_entry.pack()
    tk.Label(bmi_window, text="Height (m):").pack()
    height_entry = tk.Entry(bmi_window)
    height_entry.pack()
    tk.Button(bmi_window, text="Calculate", command=calculate).pack()

def visualize_data():
    c.execute("SELECT weight, height FROM users WHERE username=?", (current_user.get(),))
    data = c.fetchall()
    weights = [record[0] for record in data]
    heights = [record[1] for record in data]
    plt.plot(weights, heights)
    plt.xlabel('Weight (kg)')
    plt.ylabel('Height (m)')
    plt.title('BMI Trends')
    plt.show()

current_user = tk.StringVar()

# Main application layout
tk.Button(root, text="Register", command=register).pack()
tk.Button(root, text="Login", command=login).pack()
tk.Button(root, text="Visualize Data", command=visualize_data).pack()

root.mainloop()

# Close the database connection
conn.close()

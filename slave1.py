import tkinter as tk
from tkinter import ttk
import serial

ser1 = serial.Serial('COM4', 9600)


root1 = tk.Tk()
root1.geometry("265x200")
root1.title("Slave1 GUI")
root1.iconbitmap("./task4_logo.ico")

# Set a background color for the root window
root1.configure(bg="#000036")

# Define a custom font for labels
head_font = ("Helvetica", 24, "bold")
label_font = ("Helvetica", 10, "italic")
font_style = ("Helvetica", 10, "italic")


# define style
style = ttk.Style(root1)
style.theme_use("vista")


def create_label_with_style(parent, text, font, row, column, columnspan, padx=10, pady=10):
    label = ttk.Label(parent, text=text, font=font, style="White.TLabel")
    label.grid(row=row, column=column, columnspan=columnspan,
               padx=padx, pady=pady, sticky="n")
    return label


# style with white text on a window background
style.configure("White.TLabel", background=root1.cget(
    "bg"), foreground="white")

# style for buttons with white text on a window background
style.configure("White.TButton", background=root1.cget(
    "bg"), foreground="#36454F")


def checkCode():
    entered_code = code_entry.get()
    ser1.write(entered_code.encode())


# Create GUI elements for Slave 1
head_label = ttk.Label(
    root1, text="Slave1 GUI", font=head_font)
code_label1 = create_label_with_style(
    root1, "Enter the Code:", label_font, 1, 0, 1, padx=10, pady=10)
code_entry = ttk.Entry(root1, width=40)
check_button1 = ttk.Button(root1, text="Authenticate",
                           command=checkCode, style="White.TButton")

# Grid GUI elements
head_label = create_label_with_style(
    root1, "Slave1 GUI", head_font, 0, 0, 2, padx=10, pady=15)
code_label1.grid(padx=10, pady=(10, 0))
code_entry.grid(padx=10, pady=(5, 12))
check_button1.grid(padx=10, pady=(5, 12))

root1.mainloop()

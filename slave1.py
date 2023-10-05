import tkinter as tk
from tkinter import ttk
import serial

ser1 = serial.Serial('COM4', 9600)  # Replace 'COM1' with the correct COM port


root1 = tk.Tk()
root1.geometry("250x120")
root1.title("Slave1 GUI")
root1.iconbitmap("./task4_logo.ico")

# define style
style = ttk.Style(root1)
style.theme_use("clam")


def checkCode():
    entered_code = code_entry.get()
    ser1.write(entered_code.encode())
    # You can add code here to display a message based on the response from Arduino


# Create GUI elements for Slave 1 (code entry and check button)
code_label1 = ttk.Label(root1, text="Enter Code:")
code_entry = ttk.Entry(root1, width=40)
check_button1 = ttk.Button(root1, text="Check Code", command=checkCode)

# Pack GUI elements
code_label1.pack(padx=10, pady=(10, 0))
code_entry.pack(padx=10, pady=(5, 12))
check_button1.pack(padx=10, pady=(5, 12))

root1.mainloop()

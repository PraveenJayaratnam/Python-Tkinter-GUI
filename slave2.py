import tkinter as tk
from tkinter import ttk
import serial

ser2 = serial.Serial('COM2', 9600)  # Replace 'COM1' with the correct COM port


root2 = tk.Tk()
root2.geometry("250x120")
root2.title("Slave2 GUI")
root2.iconbitmap("./task4_logo.ico")

# define style
style = ttk.Style(root2)
style.theme_use("clam")


def checkCode():
    entered_code = code_entry.get()
    ser2.write(entered_code.encode())
    # You can add code here to display a message based on the response from Arduino


# Create GUI elements for Slave 1 (code entry and check button)
code_label2 = ttk.Label(root2, text="Enter Code:")
code_entry = ttk.Entry(root2)
check_button1 = ttk.Button(root2, text="Check Code", command=checkCode)

# Pack GUI elements
code_label2.pack(padx=10, pady=(10, 0))
code_entry.pack(padx=10, pady=(5, 12))
check_button1.pack(padx=10, pady=(5, 12))

root2.mainloop()

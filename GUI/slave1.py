import time
import tkinter as tk
from tkinter import ttk
import serial


slave_ser1 = serial.Serial('COM4', 115200)


def send_to_arduino_slave(input_str, ser):
    ser.write(input_str.encode())
    time.sleep(0.1)


def read_from_arduino(ser):
    response = ser.readline().decode().strip()
    return response


def get_response():
    start_time = time.time()

    while (slave_ser1.inWaiting() == 0):
        if time.time() - start_time > 3:
            return "Try Again"

    result = read_from_arduino(slave_ser1)
    return result


def submit_token():
    code_label1.configure(text="")
    submit_button.configure(state="disabled")
    send_to_arduino_slave(code_entry.get(), slave_ser1)
    code_entry.delete(0, tk.END)
    result = get_response()
    code_label1.configure(text=result)
    submit_button.configure(state="active")


root1 = tk.Tk()
root1.geometry("265x200")
root1.title("Slave1 GUI")
root1.configure(bg="#000036")

head_font = ("Helvetica", 24, "bold")
label_font = ("Helvetica", 10, "italic")

style = ttk.Style(root1)
style.theme_use("vista")


def create_label_with_style(parent, text, font, row, column, columnspan, padx=10, pady=10):
    label = ttk.Label(parent, text=text, font=font, style="White.TLabel")
    label.grid(row=row, column=column, columnspan=columnspan,
               padx=padx, pady=pady, sticky="n")
    return label


style.configure("White.TLabel", background=root1.cget(
    "bg"), foreground="white")
style.configure("White.TButton", background=root1.cget(
    "bg"), foreground="#36454F")

head_label = ttk.Label(root1, text="Slave1 GUI", font=head_font)
code_label1 = create_label_with_style(
    root1, "Enter the Code:", label_font, 1, 0, 1, padx=10, pady=10)
code_entry = ttk.Entry(root1, width=40)

head_label = create_label_with_style(
    root1, "Slave1 GUI", head_font, 0, 0, 2, padx=10, pady=15)
code_label1.grid(padx=10, pady=(10, 0))
code_entry.grid(padx=10, pady=(5, 12))
submit_button = ttk.Button(
    root1, text='Authenticate', command=lambda: submit_token(), style="White.TButton")
submit_button.grid(padx=10, pady=(5, 12))
root1.mainloop()

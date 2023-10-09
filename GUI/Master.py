import datetime
import time
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import serial

# Define the serial port and baud rate
master_ser = serial.Serial('COM3', 115200)

root = tk.Tk()
root.geometry("370x300")
root.title("Master GUI")
root.iconbitmap("./task4_logo.ico")
root.resizable(False, False)

# Set a background color for the root window
root.configure(bg="#000036")

# Define a custom font for labels
head_font = ("Helvetica", 24, "bold")
label_font = ("Helvetica", 10, "italic")
font_style = ("Helvetica", 10, "italic")

# Define style
style = ttk.Style(root)
style.theme_use("vista")

# Create a label with white text on a window background


def create_label_with_style(parent, text, font, row, column, columnspan, padx=10, pady=10):
    label = ttk.Label(parent, text=text, font=font, style="White.TLabel")
    label.grid(row=row, column=column, columnspan=columnspan,
               padx=padx, pady=pady, sticky="n")
    return label


# Create a style with white text on a window background
style.configure("White.TLabel", background=root.cget("bg"), foreground="white")

# Create a style for buttons with white text on a window background
style.configure("White.TButton", background=root.cget(
    "bg"), foreground="#36454F")

head_label = ttk.Label(
    root, text="Master GUI", font=head_font)

nic_label = create_label_with_style(
    root, "NIC Number (First 9 digits only)", label_font, 1, 0, 1, padx=10, pady=10)
nic_input = ttk.Entry(root)

dob_label = create_label_with_style(
    root, "Date of Birth (YYYY-MM-DD)", label_font, 2, 0, 1, padx=10, pady=10)
dob_input = ttk.Entry(root)

key_label = create_label_with_style(
    root, "Select Gate", label_font, 3, 0, 1, padx=10, pady=10)
code_label = create_label_with_style(
    root, "Generated Code", label_font, 3, 0, 1, padx=10, pady=10)
gate_var = tk.StringVar()
gate_var.set("1")  # Set default value to an empty string
gate_option_menu = tk.OptionMenu(root, gate_var, "1", "2")
gate_number = gate_var


def send_to_arduino(input_str, ser):
    ser.write((input_str + "\n").encode())
    time.sleep(0.1)


def read_from_arduino(ser):
    response = ser.readline().decode().strip()
    return response


def copy_label_value():
    label_text = gate_var.get()
    root.clipboard_clear()
    root.clipboard_append(label_text)
    root.update()
    gate_var.set("Copied")
    root.after(1000, reset_func)


def reset_func():
    gate_var.set("")
    reg_btn.configure(state="active")


def generate_token():
    nic_number = nic_input.get()
    dob = dob_input.get()
    selected_gate = gate_var.get()
      # Validate NIC and DOB inputs
    if len(nic_number) != 9 or not nic_number.isdigit():
        messagebox.showerror("Error", "NIC Number should be a 9-digit number")
        return
    try:
        datetime.datetime.strptime(dob, "%Y-%m-%d")
    except ValueError:
        messagebox.showerror(
            "Error", "Date of Birth should be in the format YYYY-MM-DD")
        return

    # Check if a gate is selected
    if selected_gate == "":
        messagebox.showerror("Error", "Please select a gate")
        return
    if (gate_number.get() != ''):
        send_to_arduino(gate_number.get(), master_ser)
        while (master_ser.inWaiting() == 0):
            pass

        token = read_from_arduino(master_ser)
        print(token)
        generated_token.configure(text=token)
       

generated_token = ttk.Label(root, text="",width=20)
reg_btn = ttk.Button(root, text="Register",
                     command=lambda: generate_token(), style="White.TButton")

key_label.bind("<Button-1>", lambda event: copy_label_value())

head_label = create_label_with_style(
    root, "Master GUI", head_font, 0, 0, 2, padx=10, pady=20)
nic_label.grid(row=1, column=0, padx=10, pady=(10, 0))
nic_input.grid(row=1, column=1, padx=10, pady=(10, 0))
dob_label.grid(row=2, column=0, padx=10, pady=(10, 0))
dob_input.grid(row=2, column=1, padx=10, pady=(10, 0))
key_label.grid(row=3, column=0, padx=10, pady=(10, 0))
gate_option_menu.grid(row=3, column=1, padx=10, pady=(10, 0))
code_label.grid(row=5, column=0, padx=10, pady=(10, 0))
reg_btn.grid(row=4, column=0, columnspan=2, padx=10, pady=(10, 0), sticky="n")
generated_token.grid(row=5, column=1, columnspan=2, padx=(10,20), pady=(10, 0))


root.mainloop()

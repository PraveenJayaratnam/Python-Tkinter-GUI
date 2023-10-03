import datetime
import tkinter as tk
from tkinter import messagebox
import hashlib
from tkinter import ttk
import pyperclip
import serial

# Define the serial port and baud rate for communication with Arduino
ser = serial.Serial('COM3', 9600)  # Use your actual COM port number

root = tk.Tk()
root.geometry("450x400")
root.title("Master GUI")
root.iconbitmap("./task4_logo.ico")

# define style
style = ttk.Style(root)
style.theme_use("clam")

# Function to generate a secure hash


def generateSecureHash(data):
    sha256 = hashlib.sha256()
    sha256.update(data.encode())
    return sha256.digest()

# Generate the RFID-like code


def generateUniqueCode(last_4_nic, birth_year, birth_month, birth_date, selected_gate):
    unique_data = last_4_nic + birth_year + birth_month + birth_date
    hash_bytes = generateSecureHash(unique_data)

    # Determine the code prefix based on the selected gate
    if selected_gate == "Gate 1":
        code_prefix = "g1"
    elif selected_gate == "Gate 2":
        code_prefix = "g2"
    else:
        code_prefix = "g0"  # Default value if nothing is selected

    # Ensure the code is exactly 16 bytes long
    # Prefix (2 bytes) + First 14 bytes of hash
    code = code_prefix.encode() + hash_bytes[:14]
    return code


def generateCode():
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

    # Extract birth year, month, and date
    dob_parts = dob.split('-')
    birth_year = dob_parts[0][-2:]
    birth_month = dob_parts[1]
    birth_date = dob_parts[2]

    # Generate RFID-like code
    last_4_nic = nic_number[-4:]
    alphanumeric_code = generateUniqueCode(
        last_4_nic, birth_year, birth_month, birth_date, selected_gate)

    # Convert to hex representation
    generated_token.config(text=alphanumeric_code.hex().upper())


nic_label = ttk.Label(root, text="NIC Number (First 9 digits only)")
nic_input = ttk.Entry(root)

dob_label = ttk.Label(root, text="Date of Birth (YYYY-MM-DD)")
dob_input = ttk.Entry(root)

gate_label = ttk.Label(root, text="Select Gate")
gate_var = tk.StringVar()
gate_var.set("")  # Set default value to an empty string
gate_option_menu = ttk.OptionMenu(root, gate_var, "Gate 1", "Gate 2")

generate_button = ttk.Button(
    root, text="Generate Token", command=generateCode)
generated_token = ttk.Label(root, text="")


def copyCode():
    generated_code = generated_token.cget("text")
    if generated_code:
        pyperclip.copy(generated_code)
        messagebox.showinfo("Info", "Code copied to clipboard successfully!")
    else:
        messagebox.showerror("Error", "No code to copy.")


def sendToArduino():
    generated_code = generated_token.cget("text")
    if generated_code:
        try:
            ser.write(generated_code.encode())  # Send the code to Arduino
            messagebox.showinfo("Info", "Code sent to Arduino successfully!")
        except Exception as e:
            messagebox.showerror(
                "Error", f"Error sending code to Arduino: {e}")
    else:
        messagebox.showerror("Error", "No code to send.")


copy_button = ttk.Button(root, text="Copy Code", command=copyCode)
send_to_arduino_button = ttk.Button(
    root, text="Save to Arduino", command=sendToArduino)

nic_label.pack(padx=10, pady=(10, 0))
nic_input.pack(padx=10, pady=(5, 12))
dob_label.pack(padx=10, pady=(10, 0))
dob_input.pack(padx=10, pady=(5, 12))
gate_label.pack(padx=10, pady=(10, 0))
gate_option_menu.pack(padx=10, pady=(5, 12))
generate_button.pack(padx=10, pady=(10, 0))
generated_token.pack(padx=10, pady=(5, 12))
copy_button.pack(padx=10, pady=(5, 12))
send_to_arduino_button.pack(padx=10, pady=(5, 12))

root.mainloop()

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
root.geometry("370x300")
root.title("Master GUI")
root.iconbitmap("./task4_logo.ico")

# Set a background color for the root window
root.configure(bg="#000036")

# Define a custom font for labels
head_font = ("Helvetica", 24, "bold")
label_font = ("Helvetica", 10, "italic")
font_style = ("Helvetica", 10, "italic")

# define style
style = ttk.Style(root)
style.theme_use("vista")

# Function to create a label with white text on a window background


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


head_label = ttk.Label(
    root, text="Master GUI", font=head_font)

nic_label = create_label_with_style(
    root, "NIC Number (First 9 digits only)", label_font, 1, 0, 1, padx=10, pady=10)
nic_input = ttk.Entry(root)

dob_label = create_label_with_style(
    root, "Date of Birth (YYYY-MM-DD)", label_font, 2, 0, 1, padx=10, pady=10)
dob_input = ttk.Entry(root)

gate_label = create_label_with_style(
    root, "Select Gate", label_font, 3, 0, 1, padx=10, pady=10)
gate_var = tk.StringVar()
gate_var.set("")  # Set default value to an empty string
gate_option_menu = tk.OptionMenu(root, gate_var, "Gate 1", "Gate 2")

generate_button = ttk.Button(
    root, text="Generate Token", command=generateCode, style="White.TButton")

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


copy_button = ttk.Button(root, text="Copy Code",
                         command=copyCode, style="White.TButton")
send_to_arduino_button = ttk.Button(
    root, text="Save to Database", command=sendToArduino, style="White.TButton")

head_label = create_label_with_style(
    root, "Master GUI", head_font, 0, 0, 2, padx=10, pady=20)
nic_label.grid(row=1, column=0, padx=10, pady=(10, 0))
nic_input.grid(row=1, column=1, padx=10, pady=(10, 0))
dob_label.grid(row=2, column=0, padx=10, pady=(10, 0))
dob_input.grid(row=2, column=1, padx=10, pady=(10, 0))
gate_label.grid(row=3, column=0, padx=10, pady=(10, 0))
gate_option_menu.grid(row=3, column=1, padx=10, pady=(10, 0))
generate_button.grid(row=4, column=0, columnspan=2, padx=10, pady=(10, 0))
generated_token.grid(row=5, column=0, columnspan=2, padx=10, pady=(10, 0))
copy_button.grid(row=6, column=0, padx=10, pady=(10, 0))
send_to_arduino_button.grid(row=6, column=1, padx=10, pady=(10, 0))

root.mainloop()

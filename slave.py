import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.geometry("250x120")
root.title("Slave GUI")
root.iconbitmap("./task4_logo.ico")

# define style
style = ttk.Style(root)
style.theme_use("clam")


def buttonClicked():
    token = token_input.get()
    print(token)


token_label = ttk.Label(root, text="Enter Token")
token_input = ttk.Entry(root, width=40)

generate_button = ttk.Button(root, text="Authenticate", command=buttonClicked)

token_label.pack(padx=10, pady=(10, 0))
token_input.pack(padx=10, pady=(5, 12))
generate_button.pack(padx=10, pady=(5, 12))

root.mainloop()

import tkinter as tk
from tkinter import messagebox
import random
import string

def generate_password():
    try:
        length = int(length_entry.get())
        if length <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid positive number for length")
        return

    include_uppercase = uppercase_var.get()
    include_lowercase = lowercase_var.get()
    include_numbers = numbers_var.get()
    include_special = special_var.get()

    if not (include_uppercase or include_lowercase or include_numbers or include_special):
        messagebox.showerror("Error", "At least one character set must be selected")
        return

    characters = ""
    if include_uppercase:
        characters += string.ascii_uppercase
    if include_lowercase:
        characters += string.ascii_lowercase
    if include_numbers:
        characters += string.digits
    if include_special:
        characters += string.punctuation

    excluded_chars = exclude_entry.get()
    characters = ''.join(ch for ch in characters if ch not in excluded_chars)

    if len(characters) == 0:
        messagebox.showerror("Error", "Character set is empty after exclusion")
        return

    password = "".join(random.choice(characters) for _ in range(length))
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)

def copy_to_clipboard():
    password = password_entry.get()
    if password:
        root.clipboard_clear()
        root.clipboard_append(password)
        notification_label.config(text="Password copied to clipboard!")
        root.after(3000, lambda: notification_label.config(text=""))
    else:
        notification_label.config(text="No password to copy")
        root.after(3000, lambda: notification_label.config(text=""))

# Setting up the GUI window
root = tk.Tk()
root.title("Password Generator")

# Password length label and entry
length_label = tk.Label(root, text="Password Length:")
length_label.grid(row=0, column=0, padx=10, pady=10)
length_entry = tk.Entry(root)
length_entry.grid(row=0, column=1, padx=10, pady=10)

# Checkbox for including uppercase letters
uppercase_var = tk.BooleanVar()
uppercase_check = tk.Checkbutton(root, text="Include Uppercase Letters", variable=uppercase_var)
uppercase_check.grid(row=1, column=0, columnspan=2)

# Checkbox for including lowercase letters
lowercase_var = tk.BooleanVar()
lowercase_check = tk.Checkbutton(root, text="Include Lowercase Letters", variable=lowercase_var)
lowercase_check.grid(row=2, column=0, columnspan=2)

# Checkbox for including numbers
numbers_var = tk.BooleanVar()
numbers_check = tk.Checkbutton(root, text="Include Numbers", variable=numbers_var)
numbers_check.grid(row=3, column=0, columnspan=2)

# Checkbox for including special characters
special_var = tk.BooleanVar()
special_check = tk.Checkbutton(root, text="Include Special Characters", variable=special_var)
special_check.grid(row=4, column=0, columnspan=2)

# Exclude characters entry
exclude_label = tk.Label(root, text="Exclude Characters:")
exclude_label.grid(row=5, column=0, padx=10, pady=10)
exclude_entry = tk.Entry(root)
exclude_entry.grid(row=5, column=1, padx=10, pady=10)

# Generate password button
generate_button = tk.Button(root, text="Generate Password", command=generate_password)
generate_button.grid(row=6, column=0, columnspan=2, pady=10)

# Password output entry (readonly)
password_label = tk.Label(root, text="Generated Password:")
password_label.grid(row=7, column=0, padx=10, pady=10)
password_entry = tk.Entry(root, width=30)
password_entry.grid(row=7, column=1, padx=10, pady=10)

# Copy to clipboard button
copy_button = tk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard)
copy_button.grid(row=8, column=0, columnspan=2, pady=10)

# Notification label for copy to clipboard action
notification_label = tk.Label(root, text="", fg="green")
notification_label.grid(row=9, column=0, columnspan=2, pady=5)

# Running the GUI
root.mainloop()

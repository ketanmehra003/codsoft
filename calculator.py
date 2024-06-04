import tkinter as tk

def button_click(number):
    current = entry_input.get()
    entry_input.delete(0, tk.END)
    entry_input.insert(tk.END, str(current) + str(number))

def button_clear():
    entry_input.delete(0, tk.END)
    entry_output.delete(0, tk.END)

def button_add():
    first_number = entry_input.get()
    global f_num
    global operation
    operation = "addition"
    f_num = float(first_number)
    entry_input.delete(0, tk.END)

def button_subtract():
    first_number = entry_input.get()
    global f_num
    global operation
    operation = "subtraction"
    f_num = float(first_number)
    entry_input.delete(0, tk.END)

def button_multiply():
    first_number = entry_input.get()
    global f_num
    global operation
    operation = "multiplication"
    f_num = float(first_number)
    entry_input.delete(0, tk.END)

def button_divide():
    first_number = entry_input.get()
    global f_num
    global operation
    operation = "division"
    f_num = float(first_number)
    entry_input.delete(0, tk.END)

def button_equal():
    second_number = entry_input.get()
    entry_input.delete(0, tk.END)
    entry_output.delete(0, tk.END)
    if operation == "addition":
        result = f_num + float(second_number)
    elif operation == "subtraction":
        result = f_num - float(second_number)
    elif operation == "multiplication":
        result = f_num * float(second_number)
    elif operation == "division":
        if float(second_number) == 0:
            result = "Error: Division by zero"
        else:
            result = f_num / float(second_number)
    entry_output.insert(0, result)

# Create the main window
root = tk.Tk()
root.title("Simple Calculator")

# Create entry widgets to display input and output
entry_input = tk.Entry(root, width=35, borderwidth=5)
entry_input.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

entry_output = tk.Entry(root, width=35, borderwidth=5)
entry_output.grid(row=1, column=0, columnspan=4, padx=10, pady=10)

# Define buttons
buttons = [
    ("7", 2, 0), ("8", 2, 1), ("9", 2, 2), ("/", 2, 3),
    ("4", 3, 0), ("5", 3, 1), ("6", 3, 2), ("*", 3, 3),
    ("1", 4, 0), ("2", 4, 1), ("3", 4, 2), ("-", 4, 3),
    ("0", 5, 0), ("C", 5, 1), ("=", 5, 2), ("+", 5, 3)
]

# Add buttons to the grid
for (text, row, col) in buttons:
    if text == "=":
        button = tk.Button(root, text=text, padx=40, pady=20, command=button_equal)
    elif text == "C":
        button = tk.Button(root, text=text, padx=40, pady=20, command=button_clear)
    elif text in {"+", "-", "*", "/"}:
        if text == "+":
            command = button_add
        elif text == "-":
            command = button_subtract
        elif text == "*":
            command = button_multiply
        else:
            command = button_divide
        button = tk.Button(root, text=text, padx=40, pady=20, command=command)
    else:
        button = tk.Button(root, text=text, padx=40, pady=20, command=lambda text=text: button_click(text))
    button.grid(row=row, column=col)

# Run the application
root.mainloop()

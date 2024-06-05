import tkinter as tk
import random
import string

def generate_password():
    length = int(length_entry.get())
    use_letters = letters_var.get()
    use_numbers = numbers_var.get()
    use_symbols = symbols_var.get()

    characters = ""
    if use_letters:
        characters += string.ascii_letters
    if use_numbers:
        characters += string.digits
    if use_symbols:
        characters += string.punctuation

    if not characters:
        result_var.set("Please select at least one character set.")
        return

    password = "".join(random.choice(characters) for _ in range(length))
    result_var.set(password)

root = tk.Tk()
root.title("Random Password Generator")

tk.Label(root, text="Password Length:").pack()
length_entry = tk.Entry(root)
length_entry.pack()

letters_var = tk.BooleanVar()
letters_var.set(True)
tk.Checkbutton(root, text="Use Letters", variable=letters_var).pack()

numbers_var = tk.BooleanVar()
numbers_var.set(True)
tk.Checkbutton(root, text="Use Numbers", variable=numbers_var).pack()

symbols_var = tk.BooleanVar()
symbols_var.set(False)
tk.Checkbutton(root, text="Use Symbols", variable=symbols_var).pack()

generate_button = tk.Button(root, text="Generate Password", command=generate_password)
generate_button.pack()

result_var = tk.StringVar()
result_label = tk.Label(root, textvariable=result_var)
result_label.pack()

root.mainloop()

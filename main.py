from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json


# -------------- GENERATE PASSWORD ---------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]

    password_list = password_letters + password_numbers + password_symbols
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# -------------- SAVE PASSWORD ---------- #
def save_password():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if len(email) == 0 or len(password) == 0 or len(website) == 0:
        messagebox.showinfo(title="Empty field", message="Please fill up all the fields.")
    else:
        try:
            with open(file="data.json", mode="r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open(file="data.json", mode="w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)

            with open("data.json", mode="w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# -------------- FIND PASSWORD  ---------- #

def find_password():
    website = website_entry.get()
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No File found")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"No details for {website} are found")


# -------------- UI SET UP ---------- #

window = Tk()
window.title("Password Manager")
window.config(padx=100, pady=100, bg="black")

canvas = Canvas(height=200, width=200, bg="black")
image_logo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=image_logo)
canvas.grid(row=0, column=1)

# Labels
website_label = Label(text="Website: ", pady=10, bg="black", fg="white")
website_label.grid(row=1, column=0)
email_label = Label(text="Email: ", pady=10, bg="black", fg="white")
email_label.grid(row=2, column=0)
password_label = Label(text="Password: ", pady=10, padx=0, bg="black", fg="white")
password_label.grid(row=3, column=0)

# Entries
website_entry = Entry(width=35)
website_entry.grid(row=1, column=1)
website_entry.focus()
email_entry = Entry(width=35)
email_entry.grid(row=2, column=1)
email_entry.insert(0, "test@email.com")
password_entry = Entry(width=35)
password_entry.grid(row=3, column=1)

# Buttons
search_button = Button(text="Search", width=20, command=find_password)
search_button.grid(row=4, column=0)
generate_pw_button = Button(text="Generate password", width=20, command=generate_password)
generate_pw_button.grid(row=4, column=1)
save_button = Button(text="Save", width=20,  command=save_password)
save_button.grid(row=4, column=2)

window.mainloop()

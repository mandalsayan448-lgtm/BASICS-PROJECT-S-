import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


# ==============================
# CAFE MENU
# ==============================

menu = {
    "Coffee": 80,
    "Tea": 40,
    "Cold Coffee": 120,
    "Burger": 150,
    "Pizza": 250,
    "Sandwich": 120,
    "French Fries": 100,
    "Pasta": 180,
    "Momos": 120,
    "Coke": 60,
    "Ice Cream": 100,
    "Chocolate Cake": 140
}


# ==============================
# MAIN WINDOW
# ==============================

root = tk.Tk()

root.title("Cafe Management System")
root.geometry("1000x650")
root.resizable(False, False)


# ==============================
# VARIABLES
# ==============================

item_var = tk.StringVar()
quantity_var = tk.IntVar(value=1)

cart = []


# ==============================
# TITLE
# ==============================

title = tk.Label(
    root,
    text="☕ CAFE MANAGEMENT SYSTEM",
    font=("Arial", 25, "bold")
)

title.pack(pady=20)


# ==============================
# LEFT FRAME
# ==============================

left_frame = tk.LabelFrame(
    root,
    text="Menu",
    font=("Arial", 14, "bold"),
    padx=20,
    pady=20
)

left_frame.place(
    x=30,
    y=80,
    width=400,
    height=500
)


# ==============================
# ITEM
# ==============================

tk.Label(
    left_frame,
    text="Select Item:",
    font=("Arial", 12)
).pack(pady=10)


item_combo = ttk.Combobox(
    left_frame,
    textvariable=item_var,
    values=list(menu.keys()),
    state="readonly",
    width=25
)

item_combo.pack()

item_combo.current(0)


# ==============================
# PRICE
# ==============================

price_label = tk.Label(
    left_frame,
    text="Price: ₹80",
    font=("Arial", 12, "bold")
)

price_label.pack(pady=15)


def show_price(event=None):

    item = item_var.get()

    if item:
        price_label.config(
            text=f"Price: ₹{menu[item]}"
        )


item_combo.bind(
    "<<ComboboxSelected>>",
    show_price
)


# ==============================
# QUANTITY
# ==============================

tk.Label(
    left_frame,
    text="Quantity:",
    font=("Arial", 12)
).pack(pady=10)


quantity_box = tk.Spinbox(
    left_frame,
    from_=1,
    to=20,
    textvariable=quantity_var,
    width=25
)

quantity_box.pack()


# ==============================
# ADD TO CART
# ==============================

def add_to_cart():

    item = item_var.get()

    try:
        quantity = int(quantity_var.get())
    except:
        messagebox.showerror(
            "Error",
            "Enter valid quantity"
        )
        return

    if quantity <= 0:

        messagebox.showerror(
            "Error",
            "Quantity must be greater than 0"
        )

        return

    price = menu[item]

    total = price * quantity

    cart.append(
        [item, quantity, price, total]
    )

    order_table.insert(
        "",
        tk.END,
        values=(
            item,
            quantity,
            f"₹{price}",
            f"₹{total}"
        )
    )

    calculate_total()


add_button = tk.Button(
    left_frame,
    text="ADD TO CART",
    command=add_to_cart,
    width=25,
    height=2
)

add_button.pack(pady=25)


# ==============================
# RIGHT FRAME
# ==============================

right_frame = tk.LabelFrame(
    root,
    text="Current Order",
    font=("Arial", 14, "bold"),
    padx=10,
    pady=10
)

right_frame.place(
    x=450,
    y=80,
    width=520,
    height=500
)


# ==============================
# ORDER TABLE
# ==============================

columns = (
    "Item",
    "Quantity",
    "Price",
    "Total"
)

order_table = ttk.Treeview(
    right_frame,
    columns=columns,
    show="headings",
    height=12
)


for column in columns:

    order_table.heading(
        column,
        text=column
    )

    order_table.column(
        column,
        width=110
    )


order_table.pack(
    fill=tk.BOTH,
    expand=True
)


# ==============================
# TOTAL
# ==============================

total_label = tk.Label(
    right_frame,
    text="Total: ₹0",
    font=("Arial", 16, "bold")
)

total_label.pack(pady=10)


def calculate_total():

    total = 0

    for item in cart:
        total += item[3]

    total_label.config(
        text=f"Total: ₹{total}"
    )


# ==============================
# GENERATE BILL
# ==============================

def generate_bill():

    if len(cart) == 0:

        messagebox.showwarning(
            "Warning",
            "Please add items first."
        )

        return

    subtotal = 0

    for item in cart:
        subtotal += item[3]

    gst = subtotal * 0.05

    grand_total = subtotal + gst

    bill_window = tk.Toplevel(root)

    bill_window.title("Cafe Bill")

    bill_window.geometry("500x600")

    bill_text = tk.Text(
        bill_window,
        font=("Courier New", 11)
    )

    bill_text.pack(
        fill=tk.BOTH,
        expand=True,
        padx=10,
        pady=10
    )


    # Current date and time

    date = datetime.now().strftime(
        "%d-%m-%Y %H:%M:%S"
    )


    bill = ""

    bill += "=" * 45 + "\n"

    bill += "        CAFE MANAGEMENT SYSTEM\n"

    bill += "=" * 45 + "\n"

    bill += f"Date: {date}\n"

    bill += "-" * 45 + "\n"

    bill += "Item                 Qty   Price   Total\n"

    bill += "-" * 45 + "\n"


    for item in cart:

        bill += (
            f"{item[0]:20}"
            f"{item[1]:5}"
            f"{item[2]:8}"
            f"{item[3]:8}\n"
        )


    bill += "-" * 45 + "\n"

    bill += f"Subtotal:              ₹{subtotal:.2f}\n"

    bill += f"GST (5%):              ₹{gst:.2f}\n"

    bill += "=" * 45 + "\n"

    bill += f"Grand Total:           ₹{grand_total:.2f}\n"

    bill += "=" * 45 + "\n"

    bill += "\n        THANK YOU!\n"

    bill += "       VISIT AGAIN ☕\n"


    bill_text.insert(
        tk.END,
        bill
    )


    bill_text.config(
        state=tk.DISABLED
    )


# ==============================
# CLEAR CART
# ==============================

def clear_cart():

    cart.clear()

    for item in order_table.get_children():

        order_table.delete(item)

    calculate_total()


# ==============================
# BUTTON FRAME
# ==============================

button_frame = tk.Frame(
    right_frame
)

button_frame.pack(pady=10)


tk.Button(
    button_frame,
    text="GENERATE BILL",
    command=generate_bill,
    width=15
).grid(
    row=0,
    column=0,
    padx=5
)


tk.Button(
    button_frame,
    text="CLEAR",
    command=clear_cart,
    width=15
).grid(
    row=0,
    column=1,
    padx=5
)


tk.Button(
    button_frame,
    text="EXIT",
    command=root.destroy,
    width=15
).grid(
    row=0,
    column=2,
    padx=5
)


# ==============================
# RUN APPLICATION
# ==============================

root.mainloop()
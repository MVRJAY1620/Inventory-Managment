import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import csv
from datetime import datetime
# Createthe database to store the inventories and sales
def init_db():
    connection = sqlite3.connect("inventory.db")
    c = connection.cursor()
    c.execute(''' CREATE TABLE IF NOT EXISTS inventory(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT UNIQUE,
            price REAL,
            stock INTEGER
    )''')
    c.execute("DROP TABLE IF EXISTS sales")
    c.execute(''' CREATE TABLE IF NOT EXISTS sales(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT,
            quantity INTEGER,
            revenue REAL,
            date TEXT
    )''')

    connection.commit()
    connection.close()
# Get inventories from the database
def fetch_inventory():
    connection = sqlite3.connect("inventory.db")
    c = connection.cursor()
    c.execute("SELECT * FROM inventory ORDER BY item_name ASC")
    items = c.fetchall()
    connection.close()
    return items
# Add the new stock in inventory
def add_item():
    item_name = item_entry.get()

    try:
        price = float(price_entry.get())
        stock = int(stock_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Invalid price or stock value")
        return
    
    connection = sqlite3.connect("inventory.db")
    c = connection.cursor()
    try:
        c.execute("INSERT INTO inventory (item_name, price, stock) VALUES (?, ?, ?)",
                  (item_name, price, stock))
        connection.commit()
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", f"Item '{item_name}' already exists.")
    
    connection.close()

    clear_entry()
    refresh_inventory()
# Updates the Stocks
def update_item():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Select an item to update")
        return
    
    item_id = tree.item(selected_item[0])['values'][0]
    try:
        new_stock = int(stock_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Stock must be a number")
        return
    
    connection = sqlite3.connect("inventory.db")
    c = connection.cursor()
    c.execute("UPDATE inventory SET stock=? WHERE id=?", (new_stock, item_id))

    connection.commit()
    connection.close()

    clear_entry()
    refresh_inventory()
# Deletes the selected inventory
def delete_item():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Select an item to delete")
        return
    
    item_id = tree.item(selected_item[0])['values'][0]
    
    connection = sqlite3.connect("inventory.db")
    c = connection.cursor()
    c.execute("DELETE FROM inventory WHERE id=?", (item_id,))

    connection.commit()
    connection.close()

    refresh_inventory()
# Sells the selected stock
def sell_item():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Select an item to sell")
        return
    
    try:
        quantity = int(sell_quantity.get())
        if quantity <= 0:
            raise ValueError
    except:
        messagebox.showerror("Error", "Enter a valid positive quantity")
    
    item_id = tree.item(selected_item[0])['values'][0]
    
    with sqlite3.connect("inventory.db") as connection:
        c = connection.cursor()
        c.execute("SELECT item_name, price, stock FROM inventory WHERE id=?", (item_id,))
        item = c.fetchone()
        if not item:
            messagebox.showerror("Error", "Item not found")
            return
        name, price, stock = item
        if stock < quantity:
            messagebox.showerror("Error", "Insufficient stock")
            return
    
        c.execute("UPDATE inventory SET stock=? WHERE id=?", (stock - quantity, item_id))

        revenue = price * quantity
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute("INSERT INTO sales (item_name, quantity, revenue, date) VALUES (?, ?, ?, ?)",
                (name, quantity, revenue, date))
    
    refresh_inventory()
    sell_quantity.set(0)
# Exports the list of items to .csv file
def export_inventory():
    filepath = filedialog.asksaveasfilename(defaultextension=".csv", 
                                           filetypes=[("CSV Files", "*.csv")])
    if not filepath:
        return
    
    items = fetch_inventory()
    with open(filepath, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Item_Name", "Price", "Stock"])
        writer.writerows(items)
    messagebox.showinfo("Success", "Inventory exported successfully!")
# Refreshes the inventory after doing the databsee operations
def refresh_inventory():
    update_tree(fetch_inventory())
# Updates the CSV
def update_tree(items):
    tree.delete(*tree.get_children())
    for item in items:
        tree.insert("", tk.END, values=item)
# Clears the entries once a inventory was added
def clear_entry():
    item_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)
    stock_entry.delete(0, tk.END)
#UI
root = tk.Tk()
root.title("Inventory Management System")
root.geometry("750x600")

frame = tk.LabelFrame(root, text="Item Details", padx=10, pady=10)
frame.pack(fill="x", padx=10, pady=5)

tk.Label(frame, text="Item Name:").grid(row=0, column=0)
item_entry = tk.Entry(frame)
item_entry.grid(row=0, column=1)

tk.Label(frame, text="Price:").grid(row=0, column=2)
price_entry = tk.Entry(frame)
price_entry.grid(row=0, column=3)

tk.Label(frame, text="Stock:").grid(row=0, column=4)
stock_entry = tk.Entry(frame)
stock_entry.grid(row=0, column=5)

tk.Button(frame, text="Add Item", command=add_item).grid(row=0, column=6, padx=5)
tk.Button(frame, text="Update Stock", command=update_item).grid(row=0, column=7, padx=5)

sell_frame = tk.Frame(root)
sell_frame.pack(fill="x", padx=10, pady=5)

sell_quantity = tk.IntVar()
tk.Label(sell_frame, text="Sell Quantity:").grid(row=0, column=0)
tk.Entry(sell_frame, textvariable=sell_quantity).grid(row=0, column=1)
tk.Button(sell_frame, text="Sell item", command=sell_item).grid(row=0, column=2, padx=5)

button_frame = tk.Frame(root)
button_frame.pack(fill="x", padx=10, pady=5)
tk.Button(button_frame, text="Delete Item", command=delete_item).grid(row=0, column=0, padx=5)
tk.Button(button_frame, text="Export CSV", command=export_inventory).grid(row=0, column=1, padx=5)

tree_frame = tk.Frame(root)
tree_frame.pack(padx=10, pady=10, fill="both", expand=True)

coloummn = ("ID", "Item Name", "Price", "Stock")
tree = ttk.Treeview(tree_frame, columns=coloummn, show="headings")
for col in coloummn:
    tree.heading(col, text=col)
    tree.column(col, width=120)
tree.pack(fill="both", expand=True)

init_db()
refresh_inventory()

root.mainloop()


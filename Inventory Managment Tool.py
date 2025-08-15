#Basic Inventory Management Tool
# This is the command line interface for inventory management tool
inventory = {}
# This function adds a new item to the inventory
def add_item(item_name, price, stock):
    if item_name in inventory:
        print(f"Error: Item '{item_name}' already exists in the inventory.")
    else:
        inventory[item_name] = {
            'Price': float(price),
            'Stock': int(stock)
        }
        print(f"Item '{item_name}' added successfully.")
# This funciton updates the stock of an existing item in the inventory
def update_item(item_name, stock):
    if item_name not in inventory:
        print(f"Error: Item '{item_name}' does not exist in the inventory.")
    else:
        new_stock = stock + inventory[item_name]['stock']
        if new_stock < 0:
            print(f"Error: Insufficient stock for '{item_name}'.")
        else:
            inventory[item_name]['Stock'] = new_stock
            print(f"Item '{item_name}' updated successfully. New stock: {new_stock}")
# This functions checks the availability of an item in the inventory
def check_availability_item(item_name):
    if item_name not in inventory:
        print(f"Error: Item '{item_name}' does not exist in the inventory.")
        return "Item not found"
    else:
        return inventory[item_name]['Stock']
# This funciton generates a sales report based on the items sold
def sales_report(sales):
    total_revenue = 0.0
    for item_name, stock in sales.items():
        if item_name not in inventory:
            print(f"Error: Item '{item_name}' does not exist in the inventory.")
        elif inventory[item_name]['Stock'] < stock:
            print(f"Error: Insufficient stock for '{item_name}'.")
        else:
            inventory[item_name]['Stock'] -= stock
            total_revenue += inventory[item_name]['Price'] * stock
            print(f"Sold {stock} of '{item_name}'. Revenue: {inventory[item_name]['Price'] * stock:.2f}")
    return f"Total Revenue: {total_revenue:.2f}"
# Examples of using the functions
add_item("Apple", 0.5, 50)
add_item("Banana", 0.2, 60)
sales = {"Apple": 30, "Banana": 20, "Orange": 10}  # Orange should print an error
print(sales_report(sales))  # Should output: 19.0

print(inventory)

import os
import time
from datetime import datetime

# Constants
INVENTORY_FILE = "inventory.txt"

# Main menu
def main():
    print("\nWelcome to PizzaParty POS. Please select your desired option.\n")
    print("1. Start a new order")
    print("2. Manage store inventory")
    print("3. Clock in or clock out - WIP")
    print("4. View recent orders")
    print("5. Next page\n")
    option = int(input("Enter your option > "))
    if option == 1:
        new_order()
    elif option == 2:
        inventory()
    elif option == 3:
        clock()
    elif option == 4:
        orders()
    elif option == 5:
        main2()
    else:
        print("Your input was not recognised")
        time.sleep(3)
        main()

## Functions

# new order function
def get_pizza_price(pizza_type, size):
    pricing = {
        "thin": {"small": 4.99, "medium": 7.99, "large": 10.99},
        "italian": {"small": 5.49, "medium": 8.99, "large": 12.49},
        "pan": {"small": 5.99, "medium": 9.99, "large": 13.99}
    }
    return pricing[pizza_type][size]

def get_delivery_charge(delivery_option, speed):
    charges = {
        "delivery": {"rush": 3.99, "standard": 0.99},
        "collection": {"rush": 1.99, "standard": 0.00}
    }
    return charges[delivery_option][speed]

def save_receipt(name, address, email, delivery_type, speed, payment_method, total_price, pizza_orders, delivery_charge):
    receipt_dir = "receipts"
    os.makedirs(receipt_dir, exist_ok=True)
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{receipt_dir}/receipt_{name}_{current_time}.txt"
    
    with open(filename, 'w') as file:
        file.write("Order Summary\n")
        file.write(f"Name: {name}\n")
        file.write(f"Address: {address}\n")
        file.write(f"Email: {email}\n")
        file.write(f"Delivery Type: {delivery_type}\n")
        file.write(f"Delivery Speed: {speed}\n")
        file.write(f"Payment Method: {payment_method}\n")
        file.write("\nPizzas Ordered:\n")
        for pizza_type, pizza_size, price in pizza_orders:
            file.write(f"  - {pizza_size.capitalize()} {pizza_type.capitalize()} Pizza: £{price:.2f}\n")
        file.write(f"\nDelivery Charge: £{delivery_charge:.2f}\n")
        file.write(f"Total Price: £{total_price:.2f}\n")
        file.write(f"\nStatus: Pending\n")  # Mark order as pending by default
    
    print(f"Receipt saved as {filename}")

def new_order():
    print("\nStarting a new order...")
    number_of_pizzas = int(input("How many pizzas are you ordering? > "))
    total_price = 0
    pizza_orders = []

    # Load inventory
    inventory = load_inventory()

    for i in range(number_of_pizzas):
        print("------------------------------------")
        print("------------ Next Pizza ------------")

        # Check inventory before taking order
        print("\nCurrent Inventory:")
        for item, count in inventory.items():
            print(f"{item.capitalize()}: {count}")

        print("\nType:")
        print("1. Thin")
        print("2. Italian")
        print("3. Pan")
        pizza_option = int(input("What type of pizza > "))
        if pizza_option == 1:
            pizza_type = "thin"
        elif pizza_option == 2:
            pizza_type = "italian"
        elif pizza_option == 3:
            pizza_type = "pan"
        else:
            print("Your input was not recognised. Try again.")
            time.sleep(3)
            return new_order()

        print("\nSize:")
        print("1. Small")
        print("2. Medium")
        print("3. Large")
        size_option = int(input("What size of pizza? > "))
        if size_option == 1:
            pizza_size = "small"
            inventory_item_used = 1
        elif size_option == 2:
            pizza_size = "medium"
            inventory_item_used = 2
        elif size_option == 3:
            pizza_size = "large"
            inventory_item_used = 3
        else:
            print("Your input was not recognised. Try again.")
            time.sleep(3)
            return new_order()

        # Check if enough inventory is available
        if inventory[pizza_type] < inventory_item_used:
            print(f"Sorry, not enough {pizza_type} pizza base in stock. Please choose another type or size.")
            time.sleep(3)
            return new_order()

        # Deduct inventory after placing order
        inventory[pizza_type] -= inventory_item_used

        price = get_pizza_price(pizza_type, pizza_size)
        total_price += price
        pizza_orders.append((pizza_type, pizza_size, price))

    if number_of_pizzas > 3:
        total_price *= 0.67  # Apply 33% discount

    print("------------------------------------------")
    print("------------ Delivery Options ------------")
    print("\n")

    print("1. Delivery")
    print("2. Collection")
    delivery_option = int(input("Do you want delivery or collection? > "))
    if delivery_option == 1:
        delivery_type = "delivery"
    elif delivery_option == 2:
        delivery_type = "collection"
    else:
        print("Your input was not recognised. Try again.")
        time.sleep(3)
        return new_order()

    print("1. Rush")
    print("2. Standard")
    speed_option = int(input("Do you want rush or standard? > "))
    if speed_option == 1:
        speed = "rush"
    elif speed_option == 2:
        speed = "standard"
    else:
        print("Your input was not recognised. Try again.")
        time.sleep(3)
        return new_order()

    delivery_charge = get_delivery_charge(delivery_type, speed)
    total_price += delivery_charge

    print("-----------------------------------------")
    print("------------ Payment Options ------------")
    print("\n1. Card\n2. Cash")
    payment_method_option = int(input("Payment method > "))
    if payment_method_option == 1:
        payment_method = "card"
    elif payment_method_option == 2:
        payment_method = "cash"
    else:
        print("Your input was not recognised. Try again.")
        time.sleep(3)
        return new_order()

    name = input("Enter your name: > ")
    address = input("Enter your address: > ")
    email = input("Enter your email: > ")

    print("---------------------------------------")
    print("------------ Order Summary ------------\n")
    print(f"Order Summary for {name}")
    print(f"Delivery Type: {delivery_type}, Speed: {speed}")
    print(f"Total Price: £{total_price:.2f}, paying by {payment_method}")
    print(f"Your order will be delivered to {address} and a confirmation email sent to {email}.")

    save_receipt(name, address, email, delivery_type, speed, payment_method, total_price, pizza_orders, delivery_charge)

    # Save updated inventory
    save_inventory(inventory)

    main()

# view order history & mark as delivered function
def list_orders(status=None):
    receipt_dir = "receipts"
    if not os.path.exists(receipt_dir):
        print("No orders found.")
        return

    orders = os.listdir(receipt_dir)
    if not orders:
        print("No orders found.")
        return

    for order in orders:
        if status:
            with open(os.path.join(receipt_dir, order), 'r') as file:
                lines = file.readlines()
                order_status = [line for line in lines if line.startswith("Status:")][0].strip().split(": ")[1]
                if order_status == status:
                    print(order)
        else:
            print(order)

def search_orders(query):
    receipt_dir = "receipts"
    if not os.path.exists(receipt_dir):
        print("No orders found.")
        return

    orders = os.listdir(receipt_dir)
    found_orders = []
    for order in orders:
        with open(os.path.join(receipt_dir, order), 'r') as file:
            lines = file.readlines()
            if query.lower() in order.lower() or any(query.lower() in line.lower() for line in lines if line.startswith("Email:")):
                found_orders.append(order)

    if not found_orders:
        print("No matching orders found.")
    else:
        for order in found_orders:
            print(order)

def mark_order_completed(order_filename):
    receipt_dir = "receipts"
    order_filepath = os.path.join(receipt_dir, order_filename)
    if not os.path.exists(order_filepath):
        print("Order not found.")
        return

    with open(order_filepath, 'r') as file:
        lines = file.readlines()

    with open(order_filepath, 'w') as file:
        for line in lines:
            if line.startswith("Status:"):
                file.write("Status: Completed\n")
            else:
                file.write(line)
    
    print(f"Order {order_filename} marked as completed.")

def orders():
    while True:
        print("\n1. View All Orders")
        print("2. Search Orders")
        print("3. Mark Order as Completed")
        print("4. Exit")
        option = int(input("Choose an option: > "))

        if option == 1:
            while True:
                print("\n1. All Orders")
                print("2. Incomplete Orders")
                print("3. Completed Orders")
                print("4. Back")
                sub_option = int(input("Choose an option: > "))
                
                if sub_option == 1:
                    list_orders()
                elif sub_option == 2:
                    list_orders(status="Pending")
                elif sub_option == 3:
                    list_orders(status="Completed")
                elif sub_option == 4:
                    break
                else:
                    print("Invalid option. Please try again.")
        elif option == 2:
            query = input("Enter search query (name, date, or email): > ")
            search_orders(query)
        elif option == 3:
            order_filename = input("Enter the order filename to mark as completed: > ")
            mark_order_completed(order_filename)
        elif option == 4:
            break
        else:
            print("Invalid option. Please try again.")


# add & view inventory 
def inventory():
    while True:
        print("\n1. Display Current Inventory")
        print("2. Add to Inventory")
        print("3. Back")
        option = int(input("Choose an option: > "))

        if option == 1:
            display_inventory()
        elif option == 2:
            add_inventory()
        elif option == 3:
            break
        else:
            print("Invalid option. Please try again.")

## Inventory functions
def load_inventory():
    inventory = {"thin": 0, "italian": 0, "pan": 0}
    if os.path.exists(INVENTORY_FILE):
        with open(INVENTORY_FILE, 'r') as file:
            lines = file.readlines()
            for line in lines:
                item, count = line.strip().split(": ")
                inventory[item] = int(count)
    return inventory

def save_inventory(inventory):
    with open(INVENTORY_FILE, 'w') as file:
        for item, count in inventory.items():
            file.write(f"{item}: {count}\n")

def display_inventory():
    inventory = load_inventory()
    print("\nCurrent Inventory:")
    for item, count in inventory.items():
        print(f"{item.capitalize()}: {count}")

def add_inventory():
    print("\nAdd Inventory:")
    inventory = load_inventory()
    print("1. Thin")
    print("2. Italian")
    print("3. Pan")
    option = int(input("Select item to add inventory: > "))
    if option == 1:
        item = "thin"
    elif option == 2:
        item = "italian"
    elif option == 3:
        item = "pan"
    else:
        print("Invalid option. Please try again.")
        return

    quantity = int(input(f"Enter quantity to add for {item.capitalize()}: > "))
    if quantity > 0:
        inventory[item] += quantity
        save_inventory(inventory)
        print(f"{quantity} {item.capitalize()} added to inventory.")
        display_inventory()
    else:
        print("Quantity must be greater than zero. No changes made.")

def clock():
    pass

def main2():
    pass

main()

import os
import time
from datetime import datetime
from operator import itemgetter

# Constants
INVENTORY_FILE = "inventory.txt"
RECEIPT_DIR = "receipts"
VOUCHER_FILE = "vouchers.txt"
DISCOUNT_FILE = "discounts.txt"
VOUCHER_RECEIPT_DIR = "voucher-receipts"

# Main menu
def main():
    print("\nWelcome to PizzaParty POS. Please select your desired option.\n")
    print("1. Start a new order")
    print("2. Manage store inventory")
    print("3. Manage recent orders")
    print("4. Voucher & Discount Management")
    print("5. Delivery Driver Orders")
    print("0. Exit\n")
    option = int(input("Enter your option > "))
    if option == 1:
        new_order()
    elif option == 2:
        inventory()
    elif option == 3:
        view_recent_orders()
    elif option == 4:
        voucher()
    elif option == 5:
        delivery_driver_menu()
    elif option == 0:
        exit()
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
    os.makedirs(RECEIPT_DIR, exist_ok=True)
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{RECEIPT_DIR}/receipt_{name}_{current_time}.txt"
    
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
        print("1. Small (1)")
        print("2. Medium (2)")
        print("3. Large (3)")
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

    # Apply automatic discount for more than 3 pizzas
    if number_of_pizzas >= 3:
        total_price *= 0.67  # Apply 33% discount

    # Check if a valid voucher is entered and apply
    voucher_code = input("Enter voucher code (if any): ").strip().upper()
    if voucher_code:
        total_price = apply_voucher(total_price, voucher_code)

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
    if not os.path.exists(RECEIPT_DIR):
        print("No orders found.")
        return

    orders = os.listdir(RECEIPT_DIR)
    if not orders:
        print("No orders found.")
        return

    for order in orders:
        if status:
            with open(os.path.join(RECEIPT_DIR, order), 'r') as file:
                lines = file.readlines()
                order_status = [line for line in lines if line.startswith("Status:")][0].strip().split(": ")[1]
                if order_status == status:
                    print(order)
        else:
            print(order)

def search_orders(query):
    if not os.path.exists(RECEIPT_DIR):
        print("No orders found.")
        return

    orders = os.listdir(RECEIPT_DIR)
    found_orders = []
    for order in orders:
        with open(os.path.join(RECEIPT_DIR, order), 'r') as file:
            lines = file.readlines()
            if query.lower() in order.lower() or any(query.lower() in line.lower() for line in lines if line.startswith("Email:")):
                found_orders.append(order)

    if not found_orders:
        print("No matching orders found.")
    else:
        for order in found_orders:
            print(order)

def mark_order_completed(filename):
    order_filepath = os.path.join(RECEIPT_DIR, filename)
    with open(order_filepath, 'r') as file:
        lines = file.readlines()

    with open(order_filepath, 'w') as file:
        for line in lines:
            if line.startswith("Status:"):
                file.write("Status: Completed\n")
            else:
                file.write(line)
    
    print(f"Order {filename} marked as completed.")

def view_pending_deliveries():
    print("\nView Pending and Delivery Orders:")
    if not os.path.exists(RECEIPT_DIR):
        print("No orders found.")
        return

    orders = os.listdir(RECEIPT_DIR)
    pending_orders = []
    for order in orders:
        with open(os.path.join(RECEIPT_DIR, order), 'r') as file:
            lines = file.readlines()
            order_status = [line for line in lines if line.startswith("Status:")][0].strip().split(": ")[1]
            if order_status in ["Pending", "Delivery"]:
                pending_orders.append(order)

    if not pending_orders:
        print("No pending or delivery orders found.")
    else:
        for order in pending_orders:
            with open(os.path.join(RECEIPT_DIR, order), 'r') as file:
                lines = file.readlines()
                name = [line for line in lines if line.startswith("Name:")][0].strip().split(": ")[1]
                address = [line for line in lines if line.startswith("Address:")][0].strip().split(": ")[1]
                pizzas_ordered = sum(1 for line in lines if line.startswith("  -"))
                print(f"Order: {order}")
                print(f"Name: {name}")
                print(f"Address: {address}")
                print(f"Number of Pizzas: {pizzas_ordered}")
                print()

    return pending_orders

def update_order_status():
    pending_orders = view_pending_deliveries()
    if not pending_orders:
        return

    print("\nUpdate Order Status to Completed:")
    order_filename = input("Enter the order filename to mark as completed: > ")
    if order_filename not in pending_orders:
        print("Invalid order filename. Please try again.")
        return update_order_status()

    mark_order_completed(order_filename)

    main()

def view_recent_orders():
    print("\nRecent Orders:")
    query = input("Enter search query (name, email, or date in YYYYMMDD format) or leave empty to see recent orders: ").strip()
    receipts = get_recent_receipts(query if query else None)
    
    if not receipts:
        print("No recent orders found.")
        return
    
    print("Select a receipt to view details:")
    for index, receipt in enumerate(receipts, start=1):
        print(f"{index}. {receipt['filename']} ({receipt['date']})")
    
    try:
        choice = int(input("Enter number of receipt to view (0 to go back): "))
        if choice == 0:
            return main()
        
        selected_receipt = receipts[choice - 1]
        view_receipt(selected_receipt['filename'])
    except (IndexError, ValueError):
        print("Invalid choice. Please enter a valid number.")
        time.sleep(3)
        view_recent_orders()
    
    main()

def get_recent_receipts(query=None):
    receipts = []
    if not os.path.exists(RECEIPT_DIR):
        return receipts
    
    files = os.listdir(RECEIPT_DIR)
    for file in files:
        try:
            if not file.startswith("receipt_") or not file.endswith(".txt"):
                continue
            
            # Splitting filename into parts using "_" and "."
            parts = file.split('_')
            if len(parts) < 3 or len(parts[-1].split('.')) < 2:
                continue  # Ensure there are enough parts and format ends with .txt
            
            # Extract the timestamp part from the filename
            timestamp_str = parts[-2] + '_' + parts[-1].split('.')[0]
            
            # Parse timestamp into datetime object
            timestamp = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")
            
            # If a search query is provided, filter by name, email, or date
            if query:
                with open(os.path.join(RECEIPT_DIR, file), 'r') as receipt_file:
                    content = receipt_file.read().lower()
                    if query.lower() in content or query.lower() in file.lower():
                        receipts.append({'filename': file, 'date': timestamp})
            else:
                receipts.append({'filename': file, 'date': timestamp})
        except (IndexError, ValueError):
            continue
    
    receipts.sort(key=itemgetter('date'), reverse=True)
    return receipts[:10]

def view_receipt(filename):
    filepath = os.path.join(RECEIPT_DIR, filename)
    with open(filepath, 'r') as file:
        content = file.read()
        print("\nReceipt Details:")
        print(content)
    
    while True:
        print("\nOptions:")
        print("1. Mark as Completed")
        print("2. Void Order")
        print("3. Back")
        option = input("Choose an option: ")
        
        if option == '1':
            mark_order_completed(filename)
            break
            main()
        elif option == '2':
            void_order(filename)
            break
            main()
        elif option == '3':
            view_recent_orders()
            break
            main()
        else:
            print("Invalid option. Please choose again.")
            continue

def void_order(filename):
    order_filepath = os.path.join(RECEIPT_DIR, filename)
    os.remove(order_filepath)
    print(f"Order {filename} voided and removed.")

def delivery_driver_menu():
    while True:
        print("\nDelivery Driver Menu:")
        pending_orders = view_pending_deliveries()
        
        if not pending_orders:
            print("No pending delivery orders.")
            break
            main()

        print("\nSelect an order to mark as completed:")
        for index, order in enumerate(pending_orders, start=1):
            print(f"{index}. {order}")

        try:
            choice = int(input("Enter the number of the order to mark as completed (0 to go back): "))
            if choice == 0:
                main()
                break

            selected_order = pending_orders[choice - 1]
            mark_order_completed(selected_order)
            print(f"Order {selected_order} marked as completed.")
        except (IndexError, ValueError):
            print("Invalid choice. Please enter a valid number.")
            time.sleep(3)
            continue
def orders():
    while True:
        print("\n1. View All Orders")
        print("2. Search Orders")
        print("3. Mark Order as Completed")
        print("4. View Pending and Delivery Orders")
        print("5. Exit")
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
                    orders()
                else:
                    print("Invalid option. Please try again.")
        elif option == 2:
            query = input("Enter search query (name, date, or email): > ")
            search_orders(query)
        elif option == 3:
            update_order_status()
        elif option == 4:
            view_pending_deliveries()
        elif option == 5:
            main()
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
            main()
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

# voucher & discount management system
def voucher():
    while True:
        print("\nVoucher & Discount Management:")
        print("1. Add New Voucher")
        print("2. Remove Voucher")
        print("3. View All Vouchers")
        print("4. Back")
        option = int(input("Choose an option: > "))

        if option == 1:
            code = generate_voucher_code()
            amount = float(input("Enter amount or percentage off: "))
            description = input("Enter description: ")
            voucher_type = input("Enter voucher type (amount/percentage): ").lower()
            add_voucher(code, amount, description, voucher_type)
            print(f"New voucher added: {code} - {description}")
            print(f"Amount/Percentage: {amount}, Type: {voucher_type.capitalize()}")
            purchase_or_store = int(input("Is this a purchase(1) or a store addition(2) > "))
            if purchase_or_store == 1:
                name = input("Enter your name: > ")
                email = input("Enter your email: > ")
                payment_method = input("Enter your payment method (card/cash): > ")

                # Apply voucher and get the discounted amount
                total_spent_before_voucher = float(input("Enter the total amount before applying voucher: "))
                total_spent_after_voucher = apply_voucher(total_spent_before_voucher, code)

                # Ensure voucher-receipts directory exists
                os.makedirs(VOUCHER_RECEIPT_DIR, exist_ok=True)

                # Save voucher receipt with date and time
                current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
                with open(f"{VOUCHER_RECEIPT_DIR}/voucher_receipt_{name}_{current_time}.txt", 'w') as f:
                    f.write(f"Name: {name}\n")
                    f.write(f"Email: {email}\n")
                    f.write(f"Payment Method: {payment_method}\n")
                    f.write(f"Date and Time: {current_time}\n")
                    f.write(f"Voucher Code: {code}\n")
                    f.write(f"Voucher Type: {voucher_type.capitalize()}\n")
                    f.write(f"Description: {description}\n")
                    f.write(f"Amount Spent Before Voucher: £{total_spent_before_voucher:.2f}\n")
                    f.write(f"Amount Spent After Voucher: £{total_spent_after_voucher:.2f}\n")

                print(f"Voucher purchase receipt saved in {VOUCHER_RECEIPT_DIR}")
            else:
                print(f"The voucher code {code} was added to {VOUCHER_FILE}")
                print("Added to store addition")
        elif option == 2:
            code = input("Enter voucher code to remove: ").strip().upper()
            remove_voucher(code)
            print(f"Voucher {code} removed from {VOUCHER_FILE}")
        elif option == 3:
            vouchers = load_vouchers()
            if not vouchers:
                print("No vouchers found.")
            else:
                print("\nAll Vouchers:")
                for voucher in vouchers:
                    print(f"Code: {voucher['code']}, Amount/Percentage: {voucher['amount']}, Description: {voucher['description']}, Type: {voucher['type'].capitalize()}")
        elif option == 4:
            main()
        else:
            print("Invalid option. Please try again.")
                        
def generate_voucher_code():
    import uuid
    return str(uuid.uuid4()).upper()[:7]  # Generate a unique 7-character voucher code

def add_voucher(code, amount, description, voucher_type):
    with open(VOUCHER_FILE, 'a') as file:
        file.write(f"{code}:{amount}:{description}:{voucher_type}\n")

def remove_voucher(code):
    with open(VOUCHER_FILE, 'r+') as file:
        lines = file.readlines()
        file.seek(0)
        for line in lines:
            if not line.startswith(code):
                file.write(line)
        file.truncate()

def apply_voucher(order_total, voucher_code):
    vouchers = load_vouchers()
    for voucher in vouchers:
        if voucher['code'] == voucher_code:
            if voucher['type'] == 'amount':
                discount = min(voucher['amount'], order_total)
                voucher['amount'] -= discount
                if voucher['amount'] <= 0:
                    remove_voucher(voucher['code'])  # Remove the voucher if completely spent
                else:
                    save_vouchers(vouchers)
                return order_total - discount
            elif voucher['type'] == 'percentage':
                discount = min(order_total * voucher['amount'] / 100, voucher['amount'])
                voucher['amount'] -= discount
                if voucher['amount'] <= 0:
                    remove_voucher(voucher['code'])  # Remove the voucher if completely spent
                else:
                    save_vouchers(vouchers)
                return order_total - discount
    return order_total

def load_vouchers():
    vouchers = []
    if os.path.exists(VOUCHER_FILE):
        with open(VOUCHER_FILE, 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                if line:  # Check if line is not empty
                    try:
                        code, amount, description, voucher_type = line.split(':')
                        voucher = {
                            'code': code,
                            'amount': float(amount),
                            'description': description,
                            'type': voucher_type
                        }
                        vouchers.append(voucher)
                    except ValueError:
                        print(f"Issue reading line: {line}")  # Print the line for debugging
                        continue
    return vouchers

def save_vouchers(vouchers):
    with open(VOUCHER_FILE, 'w') as file:
        for voucher in vouchers:
            file.write(f"{voucher['code']}:{voucher['amount']}:{voucher['description']}\n")

main()

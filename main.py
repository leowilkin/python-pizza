# imports
import os
import time
from datetime import datetime

# Main menu
def main():
    print("\nWelcome to PizzaParty POS. Please select your desired option.\n")
    print("1. Start a new order")
    print("2. Manage store inventory - WIP")
    print("3. Clock in or clock out - WIP")
    print("4. View recent orders")
    print("5. Next page\n")
    option = int(input("Enter your option > "))
    if option == 1: new_order()
    elif option == 2: inventory()
    elif option == 3: clock()
    elif option == 4: orders()
    elif option == 5: main2()
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
    
    print(f"Receipt saved as {filename}")

def new_order():
    print("\nStarting a new order...")
    number_of_pizzas = int(input("How many pizzas are you ordering? > "))
    total_price = 0
    pizza_orders = []

    for i in range(number_of_pizzas):
        print("------------------------------------")
        print("------------ Next Pizza ------------")
        print("\nType:")
        print("1. Thin")
        print("2. Italian")
        print("3. Pan")
        pizza_option = int(input("What type of pizza > "))
        if pizza_option == 1: pizza_type = "thin"
        elif pizza_option == 2: pizza_type = "italian"
        elif pizza_option == 3: pizza_type = "pan"
        else:
            print("Your input was not recognised. Try again.")
            time.sleep(3)
            return new_order()
        print("\nSize:")
        print("1. Small")
        print("2. Medium")
        print("3. Large")
        size_option = int(input("What size of pizza? > "))
        if size_option == 1: pizza_size = "small"
        elif size_option == 2: pizza_size = "medium"
        elif size_option == 3: pizza_size = "large"
        else:
            print("Your input was not recognised. Try again.")
            time.sleep(3)
            return new_order()

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
    if delivery_option == 1: delivery_type = "delivery"
    elif delivery_option == 2: delivery_type = "collection"
    else:
        print("Your input was not recognised. Try again.")
        time.sleep(3)
        return new_order()

    print("1. Rush")
    print("2. Standard")
    speed_option = int(input("Do you want rush or standard? > "))
    if speed_option == 1: speed = "rush"
    elif speed_option == 2: speed = "standard"
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
    if payment_method_option == 1: payment_method = "card"
    elif payment_method_option == 2: payment_method = "cash"
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
# end new order function

# view order history & mark as delivered function
def orders():
    pass
# end view order history & mark as delivered function
def inventory():
    pass

def clock():
    pass

def main2():
    pass

main()
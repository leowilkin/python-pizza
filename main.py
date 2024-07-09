import time

def main():
    print("Welcome to Pizza Ordering system. Please select your desired option.")
    print("1. Start a new order")
    print("2. Manage store inventory")
    print("3. Clock in or clock out")
    print("4. Next page")
    option = input("Enter your option > ")
    if option == 1: new_order()
    elif option == 2: inventory()
    elif option == 3: clock()
    elif option == 4: main2()
    else: 
        print("Your input was not recognised")
        time.sleep(3)
        main()
    
def new_order():
    print("Starting a new order...")
    number = int(input("How many pizzas are you ordering? > "))
    for i in number:
        print("1. Thin")
        print("2. Italian")
        print("3. Pan")
        option = input("What type of pizza > ")
        if option == 1: type = "thin"
        elif option == 2: type = "italian"
        elif option == 3: type = "pan"
        else:
            print("Your input was not recognised. Try again.")
            time.sleep(3)
            new_order()
        print("1. Small")
        print("2. Medium")
        print("3. Large")
        option = int(input("What size of pizza? > "))
        if option == 1: size = "small"
        elif option == 2: size = "medium"
        elif option == 3: size = "large"
        else:
            print("Your input was not recognised. Try again.")
            time.sleep(3)
            new_order()
        if size == "small" and type == "thin":
            price = 



main()
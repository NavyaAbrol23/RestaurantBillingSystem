import mysql.connector
from datetime import datetime

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="navya",
        password="*************",
        database="restaurant_db"
    )

def add_menu_item():
    db = connect_db()
    cursor = db.cursor()
    item_name = input("Enter item name: ").strip()
    price = float(input("Enter item price: "))

    cursor.execute("INSERT INTO menu (item_name, price) VALUES (%s, %s)", (item_name, price))
    db.commit()
    print(f"Item '{item_name}' added successfully!")

    cursor.close()
    db.close()

def show_menu():
    db = connect_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM menu")
    items = cursor.fetchall()

    print("\nMenu:")
    for item in items:
        print(f"{item[0]}. {item[1]} - ${item[2]}")

    cursor.close()
    db.close()

def generate_receipt(order_items, total_amount):
    print("\n========== RECEIPT ==========")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("--------------------------------")

    for item_name, quantity, total in order_items:
        print(f"{item_name} x{quantity} - ${total:.2f}")

    print("--------------------------------")
    print(f"Total Amount: ${total_amount:.2f}")
    print("Thank you for dining with us!")
    print("==============================\n")

def take_order():
    show_menu()
    db = connect_db()
    cursor = db.cursor()

    order_items = []
    total_amount = 0

    while True:
        item_id = input("Enter item ID to order (or 'done' to finish): ").strip()
        if item_id.lower() == 'done':
            break

        quantity = int(input("Enter quantity: ").strip())

        cursor.execute("SELECT item_name, price FROM menu WHERE item_id = %s", (item_id,))
        item = cursor.fetchone()

        if item:
            item_name, price = item
            total_price = price * quantity
            order_items.append((item_name, quantity, total_price))
            total_amount += total_price
        else:
            print("Invalid item ID.")

    print("\nOrder Summary:")
    for item_name, quantity, total in order_items:
        print(f"{item_name} x{quantity} - ${total:.2f}")

    print(f"Total Amount: ${total_amount:.2f}")

    confirm = input("Confirm order? (yes/no): ").strip().lower()
    if confirm == 'yes':
        for item_name, quantity, total_price in order_items:
            cursor.execute("INSERT INTO orders (item_name, quantity, total_price) VALUES (%s, %s, %s)",
                           (item_name, quantity, total_price))

        db.commit()
        print("Order placed successfully!")
        generate_receipt(order_items, total_amount)

    cursor.close()
    db.close()

def view_orders():
    db = connect_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()

    print("\nOrder History:")
    for order in orders:
        print(f"ID: {order[0]}, Item: {order[1]}, Qty: {order[2]}, Total: ${order[3]}, Date: {order[4]}")

    cursor.close()
    db.close()

def main():
    while True:
        print("\nRestaurant Billing System")
        print("1. Add Menu Item")
        print("2. Show Menu")
        print("3. Take Order")
        print("4. View Orders")
        print("5. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == '1':
            add_menu_item()
        elif choice == '2':
            show_menu()
        elif choice == '3':
            take_order()
        elif choice == '4':
            view_orders()
        elif choice == '5':
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

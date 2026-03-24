# Script / file to demonstrate connecting a Python app to MongoDB
# NB: Ensure that the mongodb driver is installed (pip install pymongo)
from bson import ObjectId
# Import the required modules
from pymongo import MongoClient
from datetime import datetime

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client["ADSE-Restaurant"]

menu_col = db["menu"]
customers_col = db["customers"]
orders_col = db["orders"]


# -----------------------------------------------------------------------------------------------------
# CREATE OPERATIONS
# -----------------------------------------------------------------------------------------------------

# Function to add a new menu item
def add_menu_item():
    item = {
        "name": "Pizza",
        "category": "Food",
        "sizes": [
            {"size": "small", "price_kes": 500},
            {"size": "medium", "price_kes": 800},
            {"size": "large", "price_kes": 1200}
        ]
    }
    result = menu_col.insert_one(item)
    print(f"Menu item with id: {result.inserted_id} successfully added")

def add_customer(name, email, phone):
    customer = {
        "name": name,
        "email": email,
        "phone": phone
    }
    result = customers_col.insert_one(customer)
    print(f"Customer with id: {result.inserted_id} successfully added")
    return result.inserted_id

def create_order(customer_id):
    order = {
        "customer_id": customer_id,
        "items": [
            {
                "name": "Pizza",
                "size": "medium",
                "quantity": 1,
                "price": 800
            }
        ],
        "total_kes": 800,
        "status": "pending",
        "create_at": datetime.now(),
    }

    result = orders_col.insert_one(order)
    print(f"Order with id: {result.inserted_id} successfully added")

# -----------------------------------------------------------------------------------------------------
# READ OPERATIONS
# -----------------------------------------------------------------------------------------------------
def view_menu():
    menu_items = menu_col.find()
    print(f"Menu items:")
    for item in menu_items:
        print(item)

def view_customers():
    print(f"Customers:")
    customers = customers_col.find()
    for customer in customers:
        print(customer)

def view_orders():
    print(f"Orders:")
    orders = orders_col.find()
    for order in orders:
        print(order)

# -----------------------------------------------------------------------------------------------------
# UPDATE OPERATIONS
# -----------------------------------------------------------------------------------------------------
def update_order_status(order_id, status):
    order = orders_col.find_one({"_id": ObjectId(order_id)})
    order["status"] = status
    orders_col.update_one(order, {"$set": order}, upsert=True)
    print(f"Order with id: {order_id} successfully updated")
    return order_id

# -----------------------------------------------------------------------------------------------------
# DELETE OPERATIONS
# -----------------------------------------------------------------------------------------------------
def deleteCustomer(customer_id):
    result = customers_col.delete_one({"_id": ObjectId(customer_id)})
    if(result.deleted_count):
        print(f"Customer with id: {customer_id} successfully deleted")
    else:
        print(f"Customer with id: {customer_id} does not exist")

if __name__ == "__main__":
    # 1. Add a menu item
    # add_menu_item()

    # 2. Add customer
    # customer_id = add_customer("Alice", "0751234578", "alice@email.com")

    # 3. Create an order
    # create_order(customer_id)

    # 4. Read data
    view_menu()
    view_customers()
    view_orders()

    # NB: for update / delete copy an ID from printed out and then paste it below
    deleteCustomer("69c280450369d3c527480a6f")
    create_order("69c2758096cb2f7cd6f67006")

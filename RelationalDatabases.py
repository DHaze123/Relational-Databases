from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# -------------------------
# Part 1: Setup
# -------------------------
engine = create_engine('sqlite:///shop.db')

Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()


# -------------------------
# Part 2: Define Tables
# -------------------------

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)

    # One user can have many orders
    orders = relationship("Order", back_populates="user")

    def __repr__(self):
        return f"User(id={self.id}, name='{self.name}', email='{self.email}')"


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)

    # One product can appear in many orders
    orders = relationship("Order", back_populates="product")

    def __repr__(self):
        return f"Product(id={self.id}, name='{self.name}', price={self.price})"


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)

    # Relationships
    user = relationship("User", back_populates="orders")
    product = relationship("Product", back_populates="orders")

    def __repr__(self):
        return (f"Order(id={self.id}, user_id={self.user_id}, "
                f"product_id={self.product_id}, quantity={self.quantity})")


# -------------------------
# Part 3: Create Tables
# -------------------------
Base.metadata.create_all(engine)


# -------------------------
# Part 4: Insert Data
# -------------------------

# Users
user1 = User(name="Alice Johnson", email="alice@example.com")
user2 = User(name="Bob Smith", email="bob@example.com")

# Products
product1 = Product(name="Laptop", price=1200)
product2 = Product(name="Mouse", price=25)
product3 = Product(name="Keyboard", price=50)

session.add_all([user1, user2, product1, product2, product3])
session.commit()

# Orders
order1 = Order(user_id=user1.id, product_id=product1.id, quantity=1)
order2 = Order(user_id=user1.id, product_id=product2.id, quantity=2)
order3 = Order(user_id=user2.id, product_id=product3.id, quantity=1)
order4 = Order(user_id=user2.id, product_id=product2.id, quantity=3)

session.add_all([order1, order2, order3, order4])
session.commit()


# -------------------------
# Part 5: Queries
# -------------------------

# 1. Retrieve all users
print("\n--- All Users ---")
users = session.query(User).all()
for user in users:
    print(user)

# 2. Retrieve all products
print("\n--- All Products ---")
products = session.query(Product).all()
for product in products:
    print(f"Name: {product.name}, Price: ${product.price}")

# 3. Retrieve all orders with user name, product name, and quantity
print("\n--- All Orders ---")
orders = session.query(Order).all()
for order in orders:
    print(
        f"User: {order.user.name}, "
        f"Product: {order.product.name}, "
        f"Quantity: {order.quantity}"
    )

# 4. Update a product's price
print("\n--- Updating Product Price ---")
product_to_update = session.query(Product).filter_by(name="Mouse").first()

if product_to_update:
    product_to_update.price = 30
    session.commit()
    print(
        f"Updated {product_to_update.name} price to "
        f"${product_to_update.price}"
    )

# 5. Delete a user by ID
print("\n--- Deleting User ---")
user_to_delete = session.query(User).filter_by(id=2).first()

if user_to_delete:
    session.delete(user_to_delete)
    session.commit()
    print(f"Deleted user: {user_to_delete.name}")

print("\nAssignment completed successfully!")
"""
Models Module
------------
This module defines the database models for the application using SQLAlchemy.
It includes models for Users, Tasks, and Orders.

Classes:
    User: Represents a registered user.
    Task: Represents a task created by a user.
    Order: Represents an order placed by a user.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

# Base class for all models
Base = declarative_base()

class User(Base):
    """
    User Model
    ----------
    Represents a user in the system.

    Attributes:
        id (int): Primary Key.
        username (str): Unique username.
        email (str): Unique email address.
        password_hash (str): Hashed password for security.
        role (str): User role (e.g., 'user', 'admin').
        created_at (datetime): Timestamp of account creation.
        tasks (relationship): One-to-Many relationship with Task.
        orders (relationship): One-to-Many relationship with Order.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(150), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), default='user')
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    tasks = relationship('Task', back_populates='owner', cascade='all, delete-orphan')
    orders = relationship('Order', back_populates='owner', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<User {self.username}>"

class Task(Base):
    """
    Task Model
    ----------
    Represents a task assigned to a user.

    Attributes:
        id (int): Primary Key.
        title (str): Title of the task.
        description (str): Detailed description.
        status (str): Current status (e.g., 'pending', 'completed'). Indexed for performance.
        due_date (datetime): Optional due date.
        created_at (datetime): Timestamp of creation.
        user_id (int): Foreign Key to User table. Indexed for performance.
        owner (relationship): Many-to-One relationship with User.
    """
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    status = Column(String(50), default='pending', index=True)
    due_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    owner = relationship('User', back_populates='tasks')

    def __repr__(self):
        return f"<Task {self.title}>"

class Order(Base):
    """
    Order Model
    -----------
    Represents an order placed by a user.

    Attributes:
        id (int): Primary Key.
        product_name (str): Name of the product.
        quantity (int): Quantity ordered.
        price (float): Price per unit.
        created_at (datetime): Timestamp of creation.
        user_id (int): Foreign Key to User table. Indexed for performance.
        owner (relationship): Many-to-One relationship with User.
    """
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    product_name = Column(String(200), nullable=False)
    quantity = Column(Integer, default=1)
    price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    owner = relationship('User', back_populates='orders')

    def __repr__(self):
        return f"<Order {self.product_name}>"

"""
Database Service Module
----------------------
This module handles direct database interactions for the Standalone Application.
It replaces the APIClient and communicates directly with the SQLite database using SQLAlchemy.

Classes:
    DatabaseService: Manages user authentication and data persistence.
"""

from typing import Tuple, Optional, Any, List, Dict
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from src.models import Base, User, Task, Order
from src.config import Config

class DatabaseService:
    """
    Service for direct database operations.
    """
    def __init__(self, db_url: str = 'sqlite:///instance/database.db'):
        self.engine = create_engine(db_url, convert_unicode=True)
        self.Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=self.engine))
        
        # Ensure tables exist
        Base.metadata.create_all(bind=self.engine)
        
        self.current_user_id: Optional[int] = None

    def get_session(self):
        """Get a thread-safe session."""
        return self.Session()

    def login(self, email: str, password: str) -> Tuple[bool, str]:
        """
        Authenticate a user.
        """
        session = self.get_session()
        try:
            user = session.query(User).filter_by(email=email).first()
            if user and check_password_hash(user.password_hash, password):
                self.current_user_id = user.id
                return True, "Login successful"
            return False, "Invalid email or password"
        except Exception as e:
            return False, f"Database error: {str(e)}"
        finally:
            session.close()

    def register(self, username: str, email: str, password: str) -> Tuple[bool, str]:
        """
        Register a new user.
        """
        session = self.get_session()
        try:
            if session.query(User).filter((User.username == username) | (User.email == email)).first():
                return False, "User already exists"

            hashed_pw = generate_password_hash(password)
            new_user = User(username=username, email=email, password_hash=hashed_pw)
            session.add(new_user)
            session.commit()
            return True, "Registration successful"
        except Exception as e:
            session.rollback()
            return False, f"Registration failed: {str(e)}"
        finally:
            session.close()

    def logout(self):
        """Clear current user session."""
        self.current_user_id = None

    # ---------- Task Operations ----------

    def get_tasks(self) -> Dict[str, Any]:
        """Fetch all tasks for current user."""
        if not self.current_user_id:
            return {'tasks': []}
        
        session = self.get_session()
        try:
            tasks = session.query(Task).filter_by(user_id=self.current_user_id).all()
            return {'tasks': [self._task_to_dict(t) for t in tasks]}
        finally:
            session.close()

    def create_task(self, title: str, description: str) -> bool:
        """Create a new task."""
        if not self.current_user_id:
            return False
            
        session = self.get_session()
        try:
            task = Task(title=title, description=description, user_id=self.current_user_id)
            session.add(task)
            session.commit()
            return True
        except:
            session.rollback()
            return False
        finally:
            session.close()

    def delete_task(self, task_id: int) -> bool:
        """Delete a task."""
        session = self.get_session()
        try:
            task = session.query(Task).get(task_id)
            if task and task.user_id == self.current_user_id:
                session.delete(task)
                session.commit()
                return True
            return False
        except:
            session.rollback()
            return False
        finally:
            session.close()

    def _task_to_dict(self, task: Task) -> Dict[str, Any]:
        return {
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'status': task.status,
            'user_id': task.user_id
        }

    # ---------- Order Operations ----------

    def get_orders(self) -> Dict[str, Any]:
        """Fetch all orders for current user."""
        if not self.current_user_id:
            return {'orders': []}
        
        session = self.get_session()
        try:
            orders = session.query(Order).filter_by(user_id=self.current_user_id).all()
            return {'orders': [self._order_to_dict(o) for o in orders]}
        finally:
            session.close()

    def create_order(self, product_name: str, price: float, quantity: int = 1) -> bool:
        """Create a new order."""
        if not self.current_user_id:
            return False
            
        session = self.get_session()
        try:
            order = Order(product_name=product_name, price=price, quantity=quantity, user_id=self.current_user_id)
            session.add(order)
            session.commit()
            return True
        except:
            session.rollback()
            return False
        finally:
            session.close()

    def _order_to_dict(self, order: Order) -> Dict[str, Any]:
        return {
            'id': order.id,
            'product_name': order.product_name,
            'price': order.price,
            'quantity': order.quantity,
            'user_id': order.user_id
        }

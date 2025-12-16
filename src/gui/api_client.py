"""
API Client Module
----------------
This module handles communication with the REST API backend.
It manages authentication tokens and provides methods for all API endpoints.

Classes:
    APIClient: Wrapper for API requests.
"""

import requests
from typing import Optional, Dict, Any, Tuple

class APIClient:
    """
    Client for interacting with the Job Portal REST API.

    Attributes:
        base_url (str): The base URL of the API.
        token (str): The JWT token for authentication.
        user_id (int): The ID of the logged-in user.
    """
    def __init__(self, base_url: str = 'http://localhost:5000'):
        self.base_url = base_url
        self.token: Optional[str] = None
        self.user_id: Optional[int] = None

    def set_token(self, token: Optional[str]):
        """Set the JWT token."""
        self.token = token

    def _get_headers(self) -> Dict[str, str]:
        """Construct headers with Authorization token."""
        headers = {'Content-Type': 'application/json'}
        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'
        return headers

    def login(self, email: str, password: str) -> Tuple[bool, str]:
        """
        Login to the API.

        Args:
            email (str): User email.
            password (str): User password.

        Returns:
            (bool, str): Success status and message.
        """
        url = f'{self.base_url}/auth/login'
        try:
            print(f"Attempting login for: {email} at {url}")
            response = requests.post(url, json={'email': email, 'password': password}, timeout=5)
            print(f"Login Response: {response.status_code} - {response.text}")
            
            if response.status_code == 200:
                data = response.json()
                self.token = data.get('token')
                # Fetch user details to get ID immediately
                user_data = self.get_me()
                if user_data:
                    print(f"User ID set to: {self.user_id}")
                    return True, "Login successful"
                else:
                    return False, "Login successful but failed to fetch user details"
            
            return False, response.json().get('msg', 'Login failed')
        except requests.RequestException as e:
            print(f"Login Exception: {e}")
            return False, f"Connection error: {str(e)}"

    def register(self, username: str, email: str, password: str) -> Tuple[bool, str]:
        """
        Register a new user.

        Returns:
            (bool, str): Success status and message.
        """
        url = f'{self.base_url}/auth/register'
        try:
            response = requests.post(url, json={'username': username, 'email': email, 'password': password}, timeout=5)
            if response.status_code == 201:
                data = response.json()
                self.token = data.get('token')
                self.get_me()
                return True, "Registration successful"
            return False, response.json().get('msg', 'Registration failed')
        except requests.RequestException as e:
            return False, f"Connection error: {str(e)}"

    def get_me(self) -> Optional[Dict[str, Any]]:
        """Fetch current user details."""
        url = f'{self.base_url}/auth/me'
        try:
            response = requests.get(url, headers=self._get_headers(), timeout=5)
            if response.status_code == 200:
                data = response.json()
                self.user_id = data.get('id')
                return data
            print(f"get_me failed: {response.status_code} - {response.text}")
            return None
        except requests.RequestException as e:
            print(f"get_me Exception: {e}")
            return None

    def get_tasks(self, page: int = 1, per_page: int = 10) -> Dict[str, Any]:
        """Fetch paginated tasks."""
        url = f'{self.base_url}/api/tasks'
        params = {'page': page, 'per_page': per_page, 'user_id': self.user_id}
        try:
            response = requests.get(url, headers=self._get_headers(), params=params, timeout=5)
            if response.status_code == 200:
                return response.json()
        except requests.RequestException:
            pass
        return {'tasks': [], 'total': 0}

    def create_task(self, title: str, description: str, due_date: Optional[str] = None) -> bool:
        """Create a new task."""
        url = f'{self.base_url}/api/tasks'
        data = {
            'title': title,
            'description': description,
            'user_id': self.user_id,
            'due_date': due_date
        }
        try:
            response = requests.post(url, headers=self._get_headers(), json=data, timeout=5)
            return response.status_code == 201
        except requests.RequestException:
            return False

    def delete_task(self, task_id: int) -> bool:
        """Delete a task."""
        url = f'{self.base_url}/api/tasks/{task_id}'
        try:
            response = requests.delete(url, headers=self._get_headers(), timeout=5)
            return response.status_code == 200
        except requests.RequestException:
            return False

    def get_orders(self, page: int = 1, per_page: int = 10) -> Dict[str, Any]:
        """Fetch paginated orders."""
        url = f'{self.base_url}/api/orders'
        params = {'page': page, 'per_page': per_page, 'user_id': self.user_id}
        try:
            response = requests.get(url, headers=self._get_headers(), params=params, timeout=5)
            if response.status_code == 200:
                return response.json()
        except requests.RequestException:
            pass
        return {'orders': [], 'total': 0}

    def create_order(self, product_name: str, price: float, quantity: int = 1) -> bool:
        """Create a new order."""
        url = f'{self.base_url}/api/orders'
        data = {
            'product_name': product_name,
            'price': price,
            'quantity': quantity,
            'user_id': self.user_id
        }
        try:
            response = requests.post(url, headers=self._get_headers(), json=data, timeout=5)
            return response.status_code == 201
        except requests.RequestException:
            return False

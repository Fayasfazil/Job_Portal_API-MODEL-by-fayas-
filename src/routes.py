"""
API Routes Module
----------------
This module defines the REST API endpoints for managing Tasks and Orders.
It supports CRUD operations and pagination.

Blueprints:
    api_blueprint: The Blueprint for API routes.

Routes:
    GET /api/tasks: List tasks (paginated).
    POST /api/tasks: Create a new task.
    GET /api/tasks/<id>: Get a specific task.
    PUT /api/tasks/<id>: Update a task.
    DELETE /api/tasks/<id>: Delete a task.
    
    GET /api/orders: List orders (paginated).
    POST /api/orders: Create a new order.
    GET /api/orders/<id>: Get a specific order.
    PUT /api/orders/<id>: Update an order.
    DELETE /api/orders/<id>: Delete an order.
"""

from typing import Tuple, Dict, Any, List
from flask import Blueprint, request, jsonify, Response
from src.models import Task, Order
from src.db import db

api_blueprint = Blueprint('api', __name__)

# ---------- Helper Functions ----------

def task_to_dict(task: Task) -> Dict[str, Any]:
    """
    Convert a Task model instance to a dictionary.
    """
    return {
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'status': task.status,
        'due_date': task.due_date.isoformat() if task.due_date else None,
        'user_id': task.user_id,
        'created_at': task.created_at.isoformat()
    }

def order_to_dict(order: Order) -> Dict[str, Any]:
    """
    Convert an Order model instance to a dictionary.
    """
    return {
        'id': order.id,
        'product_name': order.product_name,
        'quantity': order.quantity,
        'price': order.price,
        'user_id': order.user_id,
        'created_at': order.created_at.isoformat()
    }

# ---------- Task CRUD ----------

@api_blueprint.route('/tasks', methods=['GET'])
def get_tasks() -> Tuple[Response, int]:
    """
    Retrieve a paginated list of tasks.
    
    Query Params:
        page (int): Page number (default 1).
        per_page (int): Items per page (default 10).
        user_id (int): Filter by user ID.
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    user_id = request.args.get('user_id')
    
    query = Task.query
    if user_id:
        query = query.filter_by(user_id=user_id)
        
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    tasks = pagination.items
    
    return jsonify({
        'tasks': [task_to_dict(t) for t in tasks],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    }), 200

@api_blueprint.route('/tasks', methods=['POST'])
def create_task() -> Tuple[Response, int]:
    """
    Create a new task.
    """
    data = request.get_json()
    if not data:
        return jsonify({'msg': 'Missing JSON body'}), 400
    
    title = data.get('title')
    if not title:
        return jsonify({'msg': 'Title is required'}), 400
        
    task = Task(
        title=title,
        description=data.get('description'),
        status=data.get('status', 'pending'),
        due_date=data.get('due_date'),
        user_id=data.get('user_id')
    )
    db.session.add(task)
    db.session.commit()
    return jsonify(task_to_dict(task)), 201

@api_blueprint.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id: int) -> Tuple[Response, int]:
    """
    Retrieve a specific task by ID.
    """
    task = Task.query.get_or_404(task_id)
    return jsonify(task_to_dict(task)), 200

@api_blueprint.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id: int) -> Tuple[Response, int]:
    """
    Update a specific task.
    """
    task = Task.query.get_or_404(task_id)
    data = request.get_json()
    if not data:
        return jsonify({'msg': 'Missing JSON body'}), 400
        
    for attr in ['title', 'description', 'status', 'due_date', 'user_id']:
        if attr in data:
            setattr(task, attr, data[attr])
            
    db.session.commit()
    return jsonify(task_to_dict(task)), 200

@api_blueprint.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id: int) -> Tuple[Response, int]:
    """
    Delete a specific task.
    """
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'msg': 'Task deleted'}), 200

# ---------- Order CRUD ----------

@api_blueprint.route('/orders', methods=['GET'])
def get_orders() -> Tuple[Response, int]:
    """
    Retrieve a paginated list of orders.
    
    Query Params:
        page (int): Page number (default 1).
        per_page (int): Items per page (default 10).
        user_id (int): Filter by user ID.
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    user_id = request.args.get('user_id')
    
    query = Order.query
    if user_id:
        query = query.filter_by(user_id=user_id)
        
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    orders = pagination.items
    
    return jsonify({
        'orders': [order_to_dict(o) for o in orders],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    }), 200

@api_blueprint.route('/orders', methods=['POST'])
def create_order() -> Tuple[Response, int]:
    """
    Create a new order.
    """
    data = request.get_json()
    if not data:
        return jsonify({'msg': 'Missing JSON body'}), 400
        
    product_name = data.get('product_name')
    price = data.get('price')
    
    if not product_name or price is None:
        return jsonify({'msg': 'product_name and price are required'}), 400
        
    order = Order(
        product_name=product_name,
        quantity=data.get('quantity', 1),
        price=price,
        user_id=data.get('user_id')
    )
    db.session.add(order)
    db.session.commit()
    return jsonify(order_to_dict(order)), 201

@api_blueprint.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id: int) -> Tuple[Response, int]:
    """
    Retrieve a specific order by ID.
    """
    order = Order.query.get_or_404(order_id)
    return jsonify(order_to_dict(order)), 200

@api_blueprint.route('/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id: int) -> Tuple[Response, int]:
    """
    Update a specific order.
    """
    order = Order.query.get_or_404(order_id)
    data = request.get_json()
    if not data:
        return jsonify({'msg': 'Missing JSON body'}), 400
        
    for attr in ['product_name', 'quantity', 'price', 'user_id']:
        if attr in data:
            setattr(order, attr, data[attr])
            
    db.session.commit()
    return jsonify(order_to_dict(order)), 200

@api_blueprint.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id: int) -> Tuple[Response, int]:
    """
    Delete a specific order.
    """
    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    return jsonify({'msg': 'Order deleted'}), 200

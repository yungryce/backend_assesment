from flask import Blueprint, request, jsonify
import requests
from datetime import datetime
from models.book import Book
from models.user import User
from models.base_model import db


backend_bp = Blueprint("backend_views", __name__, url_prefix="/api/v1/backend/admin")

@backend_bp.route('/books/add', methods=['POST'])
def add_book():
    '''
    Add a new book to the library and notify the frontend service
    '''
    # Get data from the request
    data = request.get_json()

    # Validate the received data
    if not data:
        return jsonify({"message": "Invalid data format"}), 400

    # Check if all necessary fields are provided
    title = data.get('title')
    publisher = data.get('publisher')
    category = data.get('category')

    if not title or not publisher or not category:
        return jsonify({"message": "Missing required fields: title, publisher, or category"}), 400
    
    # Check if the book with the same title already exists
    existing_book = Book.query.filter_by(title=title).first()
    if existing_book:
        return jsonify({"message": f"Book with the title '{title}' already exists"}), 409  # 409 Conflict

    # Create the book object
    book = Book(title=title, publisher=publisher, category=category)

    try:
        # Save the book to the backend database
        book.save()

        # Notify the frontend service using a webhook (localhost)
        frontend_update_url = 'http://localhost:5001/api/v1/frontend/webhooks/add-book'  # Change to your actual frontend port
        payload = {'book_id': book.id, 'book_data': book.to_dict()}
        
        # Send book data as payload
        response = requests.post(frontend_update_url, json=payload)

        # Check if the request to the frontend was successful
        if response.status_code == 200:
            return jsonify({"message": "Book added successfully and frontend updated"}), 201
        else:
            # Handle non-successful responses from the frontend webhook
            return jsonify({"message": f"Book added but failed to notify frontend: {response.text}"}), 500

    except Exception as e:
        # Handle connection errors or other request exceptions
        return jsonify({"message": f"Error adding book: {str(e)}"}), 500

@backend_bp.route('/books/remove/<string:book_id>', methods=['DELETE'])
def remove_book(book_id):
    """
    Remove a book from the backend database and notify the frontend service.

    :param book_id: ID of the book to be deleted.
    :return: JSON response indicating success or failure.
    """
    # Fetch the book by ID
    book = Book.query.get_or_404(book_id)

    try:
        # Delete the book from the backend database
        book.delete()

        # Notify the frontend service using a webhook
        frontend_update_url = 'http://localhost:5001/api/v1/frontend/webhooks/remove-book'
        payload = {'book_id': book_id}

        response = requests.post(frontend_update_url, json=payload)

        # Check if the request to the frontend was successful
        if response.status_code == 200:
            return jsonify({"message": "Book removed successfully and frontend notified"}), 200
        else:
            return jsonify({"message": f"Book removed but failed to notify frontend: {response.text}"}), 500

    except Exception as e:
        return jsonify({"message": f"Error removing book: {str(e)}"}), 500

@backend_bp.route('/users', methods=['GET'])
def list_users():
    """
    Retrieve and return a list of all users without including details about borrowed books.

    :return: JSON response with a list of users.
    """
    try:
        # Retrieve all users without filters and without the books borrowed
        users = User.get_all()
        
        # Return all users without including borrowed books
        return jsonify([user.to_dict()] for user in users), 200
    
    except Exception as e:
        # Handle unexpected errors during retrieval
        return jsonify({"message": f"Error retrieving users: {str(e)}"}), 500

@backend_bp.route('/users/books', methods=['GET'])
def list_users_with_books():
    """
    Retrieve and return a list of all users including details about books they have borrowed.

    :return: JSON response with a list of users, including borrowed books' titles.
    """
    try:
        # Retrieve all users with books borrowed
        users = User.get_all()
        
        # Return all users with borrowed books' titles included
        return jsonify([user.to_dict(include_books=True) for user in users]), 200
    
    except Exception as e:
        # Handle unexpected errors during retrieval
        return jsonify({"message": f"Error retrieving users with borrowed books: {str(e)}"}), 500

@backend_bp.route('/books/unavailable', methods=['GET'])
def list_unavailable_books():
    """
    Retrieve and return a list of books that are currently not available for borrowing.

    :return: JSON response with a list of unavailable books.
    """
    try:
        # Use get_all() with filter to fetch books that are not available
        filters = {'is_available': False}
        books = Book.get_all(filters)
        
        # Convert each book to a dictionary
        result = [book.to_dict() for book in books]
        return jsonify(result), 200
    
    except Exception as e:
        # Handle unexpected errors during retrieval
        return jsonify({"message": f"Error retrieving unavailable books: {str(e)}"}), 500



@backend_bp.route('/webhooks/add-user', methods=['POST'])
def add_user_webhook():
    """
    Webhook to handle new user enrollment notifications from the frontend service.

    Expects JSON data with 'user_id' and 'user_data'.
    Updates or creates the user in the backend database based on the received data.

    :return: JSON response indicating success or failure.
    """
    data = request.get_json()
    user_data = data.get('user_data')
    
    if not user_data:
        return jsonify({"message": "Missing user data"}), 400

    user_id = user_data.get('id')
    if not user_id:
        return jsonify({"message": "Missing user ID"}), 400
    
    # Convert date strings to datetime objects
    for date_field in ['created_at', 'updated_at']:
        if user_data.get(date_field):
            user_data[date_field] = datetime.fromisoformat(user_data[date_field])

    # Check if the user already exists
    user = User.query.get(user_id)
    if user:
        return jsonify({"message": "User already exists"}), 400
    
    # Create a new user
    user = User(**user_data)
    
    try:
        user.save()
        return jsonify({"message": "User added successfully"}), 200
    except Exception as e:
        return jsonify({"message": f"Error processing user webhook: {str(e)}"}), 500



@backend_bp.route('/webhooks/update-book', methods=['POST'])
def update_book_webhook():
    """
    Webhook to handle book updates from the frontend service.

    Expects JSON data with 'book_id' and 'is_available'.
    Updates the book's availability status based on the received data.

    :return: JSON response indicating success or failure.
    """
    data = request.get_json()
    book_id = data.get('book_id')
    is_available = data.get('is_available')

    if not book_id or is_available is None:
        return jsonify({"message": "Missing book ID or availability status"}), 400

    # Check if the book exists in the backend database
    book = Book.query.get(book_id)

    if book:
        try:
            # Update the book's availability status
            book.is_available = is_available
            book.save()
            return jsonify({"message": "Book status updated successfully"}), 200
        except Exception as e:
            return jsonify({"message": f"Error processing book update webhook: {str(e)}"}), 500
    else:
        return jsonify({"message": "Book not found in backend database"}), 404
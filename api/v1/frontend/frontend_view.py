from flask import Blueprint, request, jsonify
import requests
from models.user import User
from models.book import Book
from models.base_model import db
from datetime import datetime, timedelta


frontend_bp = Blueprint("frontend_views", __name__, url_prefix="/api/v1/frontend")

@frontend_bp.route('/enroll', methods=['POST'])
def enroll_user():
    """
    Enroll a new user and notify the backend service.

    Expects JSON data with 'email', 'firstname', and 'lastname'.
    Adds the user to the database and sends a webhook notification to the backend service.

    :return: JSON response indicating success or failure.
    """
    data = request.get_json()
    
    # Validate the received data
    if not data:
        return jsonify({"message": "Invalid data format"}), 400

    email = data.get('email')
    firstname = data.get('firstname')
    lastname = data.get('lastname')

    if not email or not firstname or not lastname:
        return jsonify({"message": "Missing required fields: email, firstname, or lastname"}), 400
    
    # Check if user already exists based on email
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"message": "User already enrolled"}), 409 

    # Create the user object
    user = User(email=email, firstname=firstname, lastname=lastname)

    try:
        # Save the user to the frontend database
        user.save()
        
        # Notify the backend service using a webhook
        backend_update_url = 'http://localhost:5000/api/v1/backend/admin/webhooks/add-user'  # URL of the backend service
        payload = {'user_id': user.id, 'user_data': user.to_dict()}
        
        # Send user data as payload
        response = requests.post(backend_update_url, json=payload)

        # Check if the request to the backend was successful
        if response.status_code == 200:
            return jsonify({"message": "User enrolled successfully and backend notified"}), 201
        else:
            return jsonify({"message": f"User enrolled but failed to notify backend: {response.text}"}), 500

    except Exception as e:
        return jsonify({"message": f"User Enrollment error: {str(e)}"}), 500


@frontend_bp.route('/books', methods=['GET'])
def list_books():
    """
    Retrieve and return a list of available books.

    This endpoint fetches all books that are currently available for borrowing.

    :return: JSON response with a list of books including their id and title.
    """
    try:
        # Fetch books that are available
        books = Book.get_all(filters={"is_available": True})
        
        # Create a list of dictionaries with id and title for each book
        book_list = [{'id': book.id, 'title': book.title} for book in books]
        
        return jsonify(book_list), 200

    except Exception as e:
        # Handle unexpected errors during retrieval
        return jsonify({"message": f"Error retrieving available books: {str(e)}"}), 500


@frontend_bp.route('/book/<string:book_id>', methods=['GET'])
def get_book(book_id):
    """
    Retrieve and return details of a specific book by its ID.

    This endpoint fetches detailed information about a book specified by its ID.

    :param book_id: ID of the book to retrieve
    :return: JSON response with details of the specified book
    """

    try:
        # Fetch the book by ID or return a 404 error if not found
        book = Book.query.get_or_404(book_id)

        # Define the fields to include in the response
        fields = ['title', 'publisher', 'category', 'is_available', 'borrowed_at', 'return_by']
        
        # Return the book details
        return jsonify(book.to_dict(fields=fields)), 200

    except Exception as e:
        # Handle unexpected errors during retrieval
        return jsonify({"message": f"Error retrieving book details: {str(e)}"}), 500

@frontend_bp.route('/books/filter', methods=['GET'])
def filter_books():
    """
    Filter and retrieve books based on publisher and/or category.

    This endpoint allows filtering books by publisher and/or category using query parameters.

    :return: JSON response with a list of book titles matching the filter criteria
    """
    try:
        # Get filter criteria from query parameters
        publisher = request.args.get('publisher')
        category = request.args.get('category')
        
        # Build the query with optional filters
        query = Book.query
        if publisher:
            query = query.filter_by(publisher=publisher)
        if category:
            query = query.filter_by(category=category)

        # Execute the query and fetch the results
        books = query.all()

        # Return a list of book titles
        return jsonify([book.title for book in books]), 200

    except Exception as e:
        # Handle unexpected errors during retrieval
        return jsonify({"message": f"Error filtering books: {str(e)}"}), 500

@frontend_bp.route('/borrow/<string:book_id>', methods=['POST'])
def borrow_book(book_id):
    """
    Borrow a book, update its availability status, and notify the backend service.

    :param book_id: ID of the book to be borrowed.
    :return: JSON response indicating success or failure.
    """
    data = request.get_json()
    book = Book.query.get_or_404(book_id)

    if not book.is_available:
        return jsonify({"message": "Book already borrowed"}), 400
    
    borrow_duration = data.get('days')

    # Validate that 'days' is an integer
    if not isinstance(borrow_duration, int) or borrow_duration <= 0:
        return jsonify({"message": "borrow duration (days) should be a positive integer"}), 400

    # Update book availability status
    book.is_available = False
    book.borrowed_at = datetime.utcnow()
    book.return_by = datetime.utcnow() + timedelta(days=borrow_duration)

    try:
        # Save the updated book status
        book.save()

        # Notify the backend service using a webhook
        backend_update_url = 'http://localhost:5000//api/v1/backend/admin/webhooks/update-book'
        payload = {'book_id': book_id, 'is_available': book.is_available}

        response = requests.post(backend_update_url, json=payload)

        # Check if the request to the backend was successful
        if response.status_code == 200:
            return jsonify({"message": "Book borrowed successfully and backend updated"}), 200
        else:
            return jsonify({"message": f"Book borrowed but failed to notify backend: {response.text}"}), 500

    except Exception as e:
        return jsonify({"message": f"Error borrowing book: {str(e)}"}), 500


@frontend_bp.route('/webhooks/add-book', methods=['POST'])
def add_book_webhook():
    '''
    Webhook for receiving new book notifications from backend and adding it to frontend database
    '''
    data = request.get_json()
    book_data = data.get('book_data')
    
    if not book_data:
        return jsonify({"message": "Missing book data"}), 400
    
    # Convert date strings to datetime objects
    for date_field in ['created_at', 'updated_at', 'borrowed_at', 'return_by']:
        if book_data.get(date_field):
            book_data[date_field] = datetime.fromisoformat(book_data[date_field])
        elif date_field in book_data and book_data[date_field] is None:
            book_data[date_field] = None

    # Check if the book already exists
    book = Book.query.get(book_data['id'])
    if book:
        return jsonify({"message": "Book already exists"}), 400

    # Create a new book
    book = Book(**book_data)
    
    # Save the new book to the frontend database
    try:
        book.save()
        return jsonify({"message": "Book added successfully to frontend"}), 200
    except Exception as e:
        return jsonify({"message": f"Error processing book webhook: {str(e)}"}), 500
    
@frontend_bp.route('/webhooks/remove-book', methods=['POST'])
def remove_book_webhook():
    """
    Webhook to handle book removal notifications from the backend service.

    Expects JSON data with 'book_id'.
    Removes the book from the frontend database based on the received data.

    :return: JSON response indicating success or failure.
    """
    data = request.get_json()
    book_id = data.get('book_id')
    
    if not book_id:
        return jsonify({"message": "Missing book ID"}), 400

    # Check if the book exists in the frontend database
    book = Book.query.get(book_id)

    if book:
        try:
            # Delete the book from the frontend database
            book.delete()
            return jsonify({"message": "Book removed successfully"}), 200
        except Exception as e:
            return jsonify({"message": f"Error processing book removal webhook: {str(e)}"}), 500
    else:
        return jsonify({"message": "Book not found in frontend database"}), 404
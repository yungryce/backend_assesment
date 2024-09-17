import pytest
import uuid
import requests_mock
from unittest.mock import patch
from flask_testing import TestCase
from app import create_app
from config.base_database import db, init_db
from models.book import Book
from models.user import User
from sqlalchemy import text

class TestBackendViews(TestCase):
    def create_app(self):
        # Create a Flask app for testing and register the blueprint
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        return app

    def setUp(self):
        # Create database tables
        with self.app.app_context():
            db.create_all()
            db.session.execute(text('DELETE FROM users'))
            db.session.commit()
        
    def tearDown(self):
        # Drop database tables
        with self.app.app_context():
            db.drop_all()

    def test_enroll_user(self):
        # Perform the test
        with requests_mock.Mocker() as m:
            m.post('http://localhost:3000/api/v1/backend/admin/webhooks/add-user', json={}, status_code=200)
            
            response = self.client.post('/api/v1/frontend/enroll', json={
                'email': 'test@example.com',
                'firstname': 'John',
                'lastname': 'Doe'
            })
            
            self.assertEqual(response.status_code, 201)
            self.assertIn(b'User enrolled successfully and backend notified', response.data)

    def test_enroll_user_existing(self):
        User(email='test@example.com', firstname='John', lastname='Doe').save()
        response = self.client.post('/api/v1/frontend/enroll', json={
            'email': 'test@example.com',
            'firstname': 'John',
            'lastname': 'Doe'
        })
        self.assertEqual(response.status_code, 409)
        self.assertIn(b'User already enrolled', response.data)

    def test_list_books(self):
        Book(title='Test Book', publisher='Macmillan', category='Horror', is_available=True).save()
        response = self.client.get('/api/v1/frontend/books')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Book', response.data)

    def test_get_book(self):
        book = Book(title='Test Book', publisher='Macmillan', category='Horror', is_available=True)
        book.save()
        response = self.client.get(f'/api/v1/frontend/book/{book.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Book', response.data)

    def test_filter_books(self):
        Book(title='Filtered Book', publisher='Test Publisher', category='Test Category').save()
        response = self.client.get('/api/v1/frontend/books/filter?publisher=Test Publisher')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Filtered Book', response.data)

    def test_borrow_book(self):
        with requests_mock.Mocker() as m:
            # Mock the backend service response
            m.post('http://localhost:3000/api/v1/backend/admin/webhooks/update-book', json={}, status_code=200)
        
            book = Book(title='Borrowable Book', publisher='Wiley', category='Drama', is_available=True)
            book.save()
            response = self.client.post(f'/api/v1/frontend/borrow/{book.id}', json={'days': 7})
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Book borrowed successfully and backend updated', response.data)

    def test_add_book_webhook(self):
        response = self.client.post('/api/v1/frontend/webhooks/add-book', json={
            'book_data': {
                'id': 'new_book_id',
                'title': 'New Book',
                'publisher': 'New Publisher',
                'category': 'New Category',
                'is_available': True
            }
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Book added successfully to frontend', response.data)

    def test_remove_book_webhook(self):
        book = Book(id='removable_book_id', title='Book to Remove', publisher='Rubbish', category='bin')
        book.save()
        response = self.client.post('/api/v1/frontend/webhooks/remove-book', json={'book_id': 'removable_book_id'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Book removed successfully', response.data)

if __name__ == '__main__':
    pytest.main()
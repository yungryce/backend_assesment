import pytest
import uuid
import requests_mock
from flask_testing import TestCase
from app import create_app
from config.base_database import db, init_db
from models.book import Book
from models.user import User

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
        
    def tearDown(self):
        # Drop database tables
        with self.app.app_context():
            db.drop_all()

    def test_add_book(self):
        with requests_mock.Mocker() as m:
            m.post('http://localhost:3001/api/v1/frontend/webhooks/add-book', json={}, status_code=200)

            response = self.client.post('/api/v1/backend/admin/books/add', json={
                'title': 'Test Book',
                'publisher': 'Test Publisher',
                'category': 'Test Category'
            })

            assert response.status_code == 201
            assert response.json['message'] == 'Book added successfully and frontend updated'
            
    def test_add_book_missing_fields(self):
        response = self.client.post('/api/v1/backend/admin/books/add', json={"title": "As e dey hot"})
        assert response.status_code == 400
        assert response.json['message'] == 'Missing required fields: publisher, category'

    def test_remove_book(self):
        book = Book(title='Test Book', publisher='Test Publisher', category='Test Category')
        book.save()
        
        with requests_mock.Mocker() as m:
            m.post('http://localhost:3001/api/v1/frontend/webhooks/remove-book', json={}, status_code=200)

            response = self.client.delete(f'/api/v1/backend/admin/books/remove/{book.id}')
            
            assert response.status_code == 200
            assert response.json['message'] == 'Book removed successfully and frontend notified'

    def test_list_users(self):
        user_id = str(uuid.uuid4())
        user = User(id=user_id, email='test_user@example.com', firstname='Test', lastname='User')
        user.save()
        
        response = self.client.get('/api/v1/backend/admin/users')
        
        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json[0]['email'] == 'test_user@example.com'

    def test_list_users_with_books(self):
        user_id = str(uuid.uuid4())
        user = User(id=user_id, email='test_user@example.com', firstname='Test', lastname='User')
        user.save()
        
        response = self.client.get('/api/v1/backend/admin/users/books')
        
        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json[0]['email'] == 'test_user@example.com'

    def test_list_unavailable_books(self):
        book = Book(title='Test Book', publisher='Test Publisher', category='Test Category', is_available=False)
        book.save()
        
        response = self.client.get('/api/v1/backend/admin/books/unavailable')
        
        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json[0]['title'] == 'Test Book'

    def test_add_user_webhook(self):
        user_id = str(uuid.uuid4())
        response = self.client.post('/api/v1/backend/admin/webhooks/add-user', json={
            'user_data': {
                'id': user_id,
                'firstname': 'New',
                'lastname': 'User',
                'email': 'new_user@example.com',
                'created_at': '2024-01-01T00:00:00',
                'updated_at': '2024-01-01T00:00:00'
            }
        })
        
        assert response.status_code == 200
        assert response.json['message'] == 'User added successfully'

    def test_update_book_webhook(self):
        book = Book(title='Test Book', publisher='Test Publisher', category='Test Category')
        book.save()
        
        response = self.client.post('/api/v1/backend/admin/webhooks/update-book', json={
            'book_id': book.id,
            'is_available': True
        })
        
        assert response.status_code == 200
        assert response.json['message'] == 'Book status updated successfully'

if __name__ == '__main__':
    pytest.main()
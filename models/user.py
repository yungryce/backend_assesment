from models.base_model import BaseModel, db
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class User(BaseModel):
    __tablename__ = 'users'

    email = db.Column(db.String(120), unique=True, nullable=False)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    books = relationship('Book', lazy=True, back_populates='users')

    def __repr__(self):
        return f'<User {self.firstname} {self.lastname}>'
    
    def to_dict(self, include_books=False):
        """
        Convert the user instance to a dictionary.

        :param include_books: If True, include borrowed book titles in the dictionary
        :return: Dictionary representation of the user instance
        """
        data = super().to_dict()  # Call the base class to_dict method to include default fields
        
        if include_books:
            # Include borrowed books' titles
            data['is_avaialable'] = [book.title for book in self.books]
        
        return data
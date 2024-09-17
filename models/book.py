from models.base_model import BaseModel
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship

class Book(BaseModel):
    __tablename__ = 'books'

    title = Column(String(255), nullable=False)
    publisher = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)
    is_available = Column(Boolean, default=True)
    borrowed_at = Column(DateTime, default=None)
    return_by = Column(DateTime, default=None)
    borrowed_by_id = Column(Integer, ForeignKey('users.id'))

    # Define a relationship with User
    users = relationship('User', lazy=True, back_populates='books')

    def __repr__(self):
        return f'<Book {self.title}>'

    def to_dict(self, fields=None):
        """
        Convert the book instance to a dictionary, including only the specified fields if provided.

        :param fields: Optional list of fields to include in the dictionary
        :return: Dictionary representation of the book instance
        """
        data = super().to_dict(fields=fields)  # Call the BaseModel's to_dict method
        if not self.is_available:
            data['available_on'] = self.return_by.isoformat() if self.return_by else None
        return data
#!/usr/bin/python3
"""models/base_model.py"""

from datetime import datetime
from sqlalchemy import Column, DateTime, String
import uuid
from config.base_database import db

class BaseModel(db.Model):
    """Base model for other models."""

    __abstract__ = True  # Declares this as a base class for other models

    # Define columns
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def save(self):
        """
        Save the current instance to the database.

        Commits the changes to the database session.
        """
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(e)

    def delete(self):
        """
        Delete the current instance from the database.

        Commits the changes to the database session.
        """
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(e)
    
    def to_dict(self, fields=None):
        """
        Convert the model instance to a dictionary, including only the specified fields if provided.

        :param fields: Optional list of fields to include in the dictionary
        :return: Dictionary representation of the model instance
        """
        data = {}
        for column in self.__table__.columns:
            if fields and column.name not in fields:
                continue
            value = getattr(self, column.name)
            if isinstance(value, datetime):
                data[column.name] = value.isoformat()  # Convert datetime to ISO format
            else:
                data[column.name] = value
        return data
    
    @classmethod
    def get_first(cls, **kwargs):
        """
        Get the first instance of the model that matches the given filter criteria.

        :param kwargs: Filter criteria
        :return: The first instance of the model matching the filter criteria, or None if not found
        """
        try:
            return db.session.query(cls).filter_by(**kwargs).first()
        except Exception as e:
            raise Exception(e)
        
    @classmethod
    def get_all(cls, filters=None):
        """
        Get all instances of the model.

        :return: List of all instances of the model
        """
        try:
            query = db.session.query(cls)
            if filters:
                query = query.filter_by(**filters)
            return query.all()
        except Exception as e:
            raise Exception(e)

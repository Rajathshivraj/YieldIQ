"""
SQLAlchemy Base declarative model.
"""
from sqlalchemy.orm import DeclarativeBase, MappedColumn
from sqlalchemy import Column, DateTime
from datetime import datetime


class Base(DeclarativeBase):
    pass

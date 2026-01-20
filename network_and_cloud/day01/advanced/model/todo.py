from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy_serializer import SerializerMixin
from network_and_cloud.day01.advanced.model.base import Base

class Todo(Base, SerializerMixin):
    __tablename__ = "todo"

    # CREATE TABLE todo (
    #     id INT AUTO_INCREMENT PRIMARY KEY,
    #     content VARCHAR(255) NOT NULL,
    #     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    # );

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String(225), nullable=False)
    created_at = Column(DateTime, default=func.now())

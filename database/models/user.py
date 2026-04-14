from datetime import datetime

from sqlalchemy import select, DateTime, Double
from sqlalchemy import Column, Integer, String, Boolean, exists
from sqlalchemy.orm import relationship

from ..base import Base, session


class User(Base):
    __tablename__ = 'users'

    vk_user_id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.first_name} {self.last_name}')>"


    def create_user(first_name, last_name, vk_user_id):
        stmt = select(exists().where(User.vk_user_id == vk_user_id))
        if session.scalar(stmt):
            return False

        user = User(first_name=first_name, last_name=last_name, vk_user_id=vk_user_id)
        with session:
            session.add(user)
            session.commit()

        return True
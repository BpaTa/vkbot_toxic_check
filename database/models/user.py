from datetime import datetime

from sqlalchemy import select, DateTime, Double, update, func
from sqlalchemy import Column, Integer, String, Boolean, exists
from sqlalchemy.orm import relationship

from database.models import Message
from ..base import Base, session


class User(Base):
    __tablename__ = 'users'

    vk_user_id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    toxic_rating = Column(Double, nullable=True)

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

def update_user_toxic_rating(user_id, toxic_rating):
    stmt = update(User).where(User.id == user_id).values(toxic_rating=toxic_rating)

    with session:
        session.execute(stmt)
        session.commit()

def calc_toxic_rating(user_id):
    total_message_count_stmt = (select(func.count(Message))
                        .select_from(Message)
                        .where(Message.from_id == user_id))
    toxic_message_count_stmt = (select(func.count(Message))
                        .select_from(Message)
                        .where(Message.from_id == user_id & Message.is_toxic == True))

    with session:
        total_message_count = session.execute(total_message_count_stmt)
        toxic_message_count = session.execute(toxic_message_count_stmt)

    toxic_rating = pow(toxic_message_count, 2) / total_message_count

    return toxic_rating

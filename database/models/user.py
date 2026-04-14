from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from ..base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)  # VK user_id
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    username = Column(String(50))  # может быть псевдонимом в боте
    avatar_url = Column(String(500))
    is_bot = Column(Boolean, default=False)

    # Связи
    user_chats = relationship('ChatUser', back_populates='user')
    user_messages = relationship('MessageUser', back_populates='user')
    sent_messages = relationship('Message', back_populates='author')

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.first_name} {self.last_name}')>"
from sqlalchemy import Column, Integer, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship

from ..base import Base


class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)  # local ID в нашей БД
    vk_message_id = Column(Integer, nullable=False)  # ID сообщения в VK (поле id из object)
    peer_id = Column(Integer, nullable=False)  # куда отправлено: peer_id из VK
    date = Column(DateTime, nullable=False)  # время отправки (поле date из object, UNIX timestamp)
    text = Column(Text)  # текст сообщения (поле body или text из object)

    # Внешние ключи
    chat_id = Column(Integer, ForeignKey('chats.id'), nullable=False)
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    # Дополнительные поля из VK API
    attachments = Column(Text)  # JSON-строка с вложениями (attachments из object)
    fwd_messages = Column(Text)  # пересланные сообщения (fwd_messages из object)
    reply_message_id = Column(Integer, ForeignKey('messages.id'), nullable=True)  # на какое сообщение ответили
    is_edited = Column(Boolean, default=False)  # редактировалось ли сообщение
    edited_at = Column(DateTime, nullable=True)  # когда редактировали

    # Статус доставки/прочтения (упрощённо)
    read_state = Column(Integer, default=0)  # 0 — не прочитано, 1 — прочитано

    # Связи
    message_users = relationship('MessageUser', back_populates='message')
    chat = relationship('Chat', back_populates='messages')
    author = relationship('User', back_populates='sent_messages')
    reply_to = relationship('Message', remote_side=[id], backref='replies')

    def __repr__(self):
        return f"<Message(id={self.vk_message_id}, chat_id={self.chat_id}, author_id={self.author_id})>"
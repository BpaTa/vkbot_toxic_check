from sqlalchemy import select
from sqlalchemy import Column, Integer, DateTime, Boolean, ForeignKey, Text, Double, func
from sqlalchemy.orm import relationship

from database.models import User
from ..base import Base, session


class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)  # local ID в нашей БД
    date = Column(DateTime, nullable=False)
    from_id = Column(Integer, ForeignKey('users.vk_user_id'), nullable=True)
    text = Column(Text)
    chat_id = Column(Integer, nullable=False)
    toxic_score = Column(Double, nullable=False, default=0.0)
    is_toxic = Column(Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"<Message(id={self.vk_message_id}, chat_id={self.chat_id}, author_id={self.author_id})>"


def save_message(date, from_id, text, chat_id, toxic_score, is_toxic=False):
    message = Message(date=date, from_id=from_id, text=text, chat_id=chat_id, toxic_level=toxic_score, is_toxic=is_toxic)

    with session:
        session.add(message)
        session.commit()


def get_top_toxic_users(chat_id):
    subquery = (
        select(
            Message.from_id,
            func.count().label('count'),
            func.sum(Message.toxic_level).label('sum'),
            func.avg(Message.toxic_level).label('avg'),
        )
        .select_from(Message)
        .where(Message.chat_id == chat_id)
        .group_by(Message.from_id)
        .limit(3)
        .cte('t')
    )

    stmt = (
        select(
            User.first_name,
            User.last_name,
            subquery.c.count.label('message_count'),
            subquery.c.sum.label('all_toxic_level'),
            subquery.c.avg.label('avg_toxic_level')
        )
        .select_from(User)
        .join(subquery, User.vk_user_id == subquery.c.from_id)
        .order_by(subquery.c.sum.desc())
    )
    with session:
        result = session.execute(stmt).all()
        return result



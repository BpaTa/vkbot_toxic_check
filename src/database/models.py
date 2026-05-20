from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base


class User(Base):
    __tablename__ = "users"

    vk_user_id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(30), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    username: Mapped[str] = mapped_column(String(30))


class UserScore(Base):
    __tablename__ = "user_score"

    user_id: Mapped[int] = mapped_column(nullable=False)
    chat_id: Mapped[int] = mapped_column(nullable=False)
    toxic_rating: Mapped[float] = mapped_column(default=0.0)
    toxic_message_count: Mapped[int] = mapped_column(default=0)
    all_message_count: Mapped[int] = mapped_column(default=0)


    
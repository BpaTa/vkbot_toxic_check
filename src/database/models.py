from ast import And
from typing import Optional

from sqlalchemy import String, select
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncSession
from torch.compiler import F

from database.base import Base, async_session


class User(Base):
    __tablename__ = "users"

    vk_user_id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(30), nullable=True)
    last_name: Mapped[str] = mapped_column(String(50), nullable=True)
    username: Mapped[str] = mapped_column(String(30), nullable=True)

    @classmethod
    async def get_user_by_id(cls, vk_user_id: int) -> Optional["User"]:
        stmt = select(cls).where(cls.vk_user_id == vk_user_id)
        async with async_session() as session:
            return await session.scalar(stmt)
        
    
    @classmethod
    async def create_user(cls, vk_user_id: int, first_name: str | None, last_name:str | None):
        new_user = cls(vk_user_id=vk_user_id, first_name=first_name, last_name=last_name)
        async with async_session() as session:
            session.add(new_user)
            await session.commit()


class UserScore(Base):
    __tablename__ = "user_score"

    user_id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    chat_id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    toxic_rating: Mapped[float] = mapped_column(default=0.0)
    toxic_message_count: Mapped[int] = mapped_column(default=0)
    all_message_count: Mapped[int] = mapped_column(default=0)

    @classmethod
    async def get_messages_count(cls, vk_user_id: int, chat_id: int):
        stmt = select(cls.toxic_message_count, cls.all_message_count).where(cls.user_id == vk_user_id, cls.chat_id == chat_id)
        async with async_session() as session:
            result = await session.execute(stmt)
            row = result.first()

            return (row.toxic_message_count, row.all_message_count) if row else (0, 0)

    @classmethod
    async def upsert_user_score(cls, vk_user_id: int, chat_id: int, toxic_rating: float, toxic_message_count: int, all_message_count: int):
        async with async_session() as session:
            user_score = await session.get(cls, (vk_user_id, chat_id))

            if user_score:
                user_score.toxic_rating = toxic_rating
                user_score.toxic_message_count = toxic_message_count
                user_score.all_message_count = all_message_count
            else:
                session.add(cls(
                    user_id=vk_user_id,
                    chat_id=chat_id,
                    toxic_rating=toxic_rating,
                    toxic_message_count=toxic_message_count,
                    all_message_count=all_message_count
                ))

            
            await session.commit()

    
from sqlalchemy.orm import DeclarativeBase, declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import logging

from config import SQLALCHEMY_DATABASE_URI

log = logging.getLogger(__name__)

engine = create_async_engine(SQLALCHEMY_DATABASE_URI, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    log.debug("Таблицы созданы")

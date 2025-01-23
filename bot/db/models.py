from sqlalchemy import BigInteger, String, URL, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
# from urllib import parse
from dotenv import load_dotenv
import os


load_dotenv()

# password = parse.quote_plus(os.getenv("BD_PASSWORD"))

url = URL.create(
    "mysql+aiomysql",
    username="root",
    password=os.getenv("BD_PASSWORD"),  # plain (unescaped) text
    host="localhost",
    database="new",
)

engine = create_async_engine(url=url)

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "peoples"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25))
    tg_id = mapped_column(BigInteger)
    post: Mapped[bool] = mapped_column(Boolean)
    position: Mapped[int] = mapped_column()
    reiting: Mapped[int] = mapped_column()


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
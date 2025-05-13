from datetime import datetime
from typing import Annotated

from sqlalchemy import func
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column

from app.config import get_db_url

DATABASE_URL = get_db_url()

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

# настройка аннотаций
int_pk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime, mapped_column(server_default=func.now())]
updated_at = Annotated[datetime, mapped_column(server_default=func.now(), onupdate=datetime.now)]
str_uniq = Annotated[str, mapped_column(unique=True, nullable=False)]
str_null_true = Annotated[str, mapped_column(nullable=True)]


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    @declared_attr.directive
    def __tablename__(cls) -> str:
        name = cls.__name__.lower()
        if name.endswith(('s', 'x', 'z', 'ch', 'sh')):
            return name + 'es'
        elif name.endswith('y'):
            return name[:-1] + 'ies'  # company -> companies
        else:
            return name if name.endswith('s') else name + 's'


def connection(method):
    async def wrapper(*args, **kwargs):
        async with async_session_maker() as this_session:
            async with this_session.begin():
                try:
                    # Явно не открываем транзакции, так как они уже есть в контексте
                    result = await method(*args, session=this_session, **kwargs)
#                    print("from wrapper:", result)
                    return result
                except Exception as e:
                    await this_session.rollback()  # Откатываем сессию при ошибке
                    raise e  # Поднимаем исключение дальше
                finally:
                    await this_session.close()  # Закрываем сессию

    return wrapper
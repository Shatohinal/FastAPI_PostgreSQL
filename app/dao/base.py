from sqlalchemy.future import select
from app.database import Base, connection
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update as sqlalchemy_update, delete as sqlalchemy_delete
import traceback

class BaseDAO[T: Base]:

    model: type[T]

    @classmethod
    @connection
    async def find_all(cls, session: AsyncSession, **filter_by) -> list[T]:
        query = select(cls.model).filter_by(**filter_by)
        print(query)
        result = await session.execute(query)
#        print(result.scalars().all())
        return result.scalars().all()
        
    @classmethod
    @connection
    async def find_one_or_none_by_id(cls, data_id: int, session: AsyncSession) -> T|None:
        query = select(cls.model).filter_by(id=data_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    @connection
    async def find_one_or_none(cls, session: AsyncSession, **filter_by) -> T|None:
        query = select(cls.model).filter_by(**filter_by)
        result = await session.execute(query)     
        return result.scalar_one_or_none()
    
    @classmethod
    @connection
    async def add(cls, session: AsyncSession, **values) -> T:
        new_instance = cls.model(**values)
        session.add(new_instance)
        await session.commit()
        return new_instance
    

    @classmethod
    @connection
    async def update(cls, filter_by, session: AsyncSession, **values) -> int:
        query = (
                sqlalchemy_update(cls.model)
                .where(*[getattr(cls.model, k) == v for k, v in filter_by.items()])
                .values(**values)
                .execution_options(synchronize_session="fetch")
            )
        result = await session.execute(query)
        await session.commit()
        return result.rowcount
    
    @classmethod
    @connection
    async def delete(cls, session: AsyncSession, delete_all: bool = False, **filter_by) -> int:
        if not delete_all and not filter_by:
            raise ValueError("Необходимо указать хотя бы один параметр для удаления.")
        
        query = sqlalchemy_delete(cls.model).filter_by(**filter_by)
        result = await session.execute(query)
        await session.commit()
        return result.rowcount
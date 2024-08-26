from abc import ABC, abstractmethod
from typing import Generic, Optional, TypeVar

from main_service.src.db.database import session
from sqlalchemy import and_, select, insert, delete, update

T = TypeVar('T')
AddT = TypeVar('AddT')


class BaseRepository(ABC, Generic[T, AddT]):
    @classmethod
    @abstractmethod
    def orm_model(cls) -> type:
        pass

    @classmethod
    @abstractmethod
    def dto_model(cls) -> type:
        pass

    @classmethod
    @abstractmethod
    def add_dto_model(cls) -> type:
        pass

    @classmethod
    @abstractmethod
    async def find_all_by_user_id(cls, user_id: int, limit: int, offset: int) -> list[T]:
        pass

    @classmethod
    async def add_one(cls, data: AddT) -> int:
        async with session() as new_session:
            data_dict = data.model_dump()
            query = insert(cls.orm_model()).values(**data_dict)
            result = await new_session.execute(query)
            await new_session.commit()
            return result.inserted_primary_key[0]


    @classmethod
    async def find_by_id(cls, user_id: int, item_id: int) -> Optional[T]:
        async with session() as new_session:
            query = select(cls.orm_model()).where(
                and_(
                    cls.orm_model().id == item_id,
                    cls.orm_model().user_id == user_id
                )
            )
            result = await new_session.execute(query)
            orm_item = result.unique().scalar_one_or_none()
            if orm_item:
                return cls.dto_model().model_validate(orm_item, from_attributes=True)
            else:
                return None

    @classmethod
    async def delete_by_id(cls, user_id: int, item_id: int) -> int:
        async with session() as new_session:
            query = delete(cls.orm_model()).where(
                and_(
                    cls.orm_model().id == item_id,
                    cls.orm_model().user_id == user_id
                )
            ).returning(cls.orm_model().id)
            result = await new_session.execute(query)
            deleted_item_id = result.scalar()
            await new_session.commit()
            return deleted_item_id

    @classmethod
    async def update_by_id(cls, user_id: int, item_id: int, data: AddT) -> None:
        async with session() as new_session:
            query = (
                update(cls.orm_model())
                .where(
                    and_(
                        cls.orm_model().id == item_id,
                        cls.orm_model().user_id == user_id
                    )
                ).values(**data.model_dump())
            )
            await new_session.execute(query)
            await new_session.commit()

from typing import Optional

from src.transactions.schemas import TransactionAddDTO, TransactionDTO
from src.db.database import session
from src.transactions.models import TransactionsOrm
from sqlalchemy import select, insert, and_


class TransactionRepository:
    @classmethod
    async def add_one(cls, data: TransactionAddDTO) -> int:
        async with session() as new_session:
            transaction_dict = data.model_dump()
            query = insert(TransactionsOrm).values(**transaction_dict)
            result = await new_session.execute(query)
            await new_session.commit()
            return result.inserted_primary_key[0]

    @classmethod
    async def find_all_by_user_id(cls, user_id: int) -> list[TransactionDTO]:
        async with session() as new_session:
            query = select(TransactionsOrm).where(TransactionsOrm.user_id == user_id)
            result = await new_session.execute(query)
            transaction_orm_list = result.unique().scalars().all()
            transaction_dto_list = [TransactionDTO.model_validate(row, from_attributes=True) for row in transaction_orm_list]
            return transaction_dto_list

    @classmethod
    async def find_by_id(cls, user_id: int, transaction_id: int) -> Optional[TransactionDTO]:
        async with session() as new_session:
            query = select(TransactionsOrm).where(
                and_(
                    TransactionsOrm.id == transaction_id,
                    TransactionsOrm.user_id == user_id
                )
            )
            result = await new_session.execute(query)
            transaction_orm = result.unique().scalar_one_or_none()
            if transaction_orm:
                return TransactionDTO.model_validate(transaction_orm, from_attributes=True)
            else:
                return None

    @classmethod
    async def delete_by_id(cls, transaction_id: int) -> None:
        async with session() as new_session:
            query = select(TransactionsOrm).where(TransactionsOrm.id == transaction_id)
            result = await new_session.execute(query)
            transaction_orm = result.scalar_one_or_none()
            if transaction_orm:
                await new_session.delete(transaction_orm)
                await new_session.commit()

    @classmethod
    async def update_by_id(cls, transaction_id: int, data: TransactionDTO) -> None:
        async with session() as new_session:
            query = select(TransactionsOrm).where(TransactionsOrm.id == transaction_id)
            result = await new_session.execute(query)
            transaction_orm = result.scalar_one_or_none()
            if transaction_orm:
                transaction_dict = data.model_dump()
                for key, value in transaction_dict.items():
                    setattr(transaction_orm, key, value)
                await new_session.commit()

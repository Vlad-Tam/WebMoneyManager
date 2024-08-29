from main_service.src.infrastructure.models.transaction import TransactionsOrm
from main_service.src.domain.entities.transaction import (
    TransactionDTO,
    TransactionAddDTO,
)
from main_service.src.infrastructure.repositories.base_crud_repo import BaseRepository
from main_service.src.infrastructure.repositories.db_repo import database_repository
from sqlalchemy import select


class TransactionRepository(BaseRepository[TransactionDTO, TransactionAddDTO]):
    repository = database_repository

    @classmethod
    def orm_model(cls) -> type:
        return TransactionsOrm

    @classmethod
    def add_dto_model(cls) -> type:
        return TransactionAddDTO

    @classmethod
    def dto_model(cls) -> type:
        return TransactionDTO

    @classmethod
    async def find_all_by_user_id(
        cls, user_id: int, limit: int, offset: int
    ) -> list[TransactionDTO]:
        async with cls.repository.a_sessionmaker() as new_session:
            query = (
                select(TransactionsOrm)
                .where(TransactionsOrm.user_id == user_id)
                .limit(limit)
                .offset(offset)
                .order_by(TransactionsOrm.id)
            )
            result = await new_session.execute(query)
            orm_list = result.unique().scalars().all()
            dto_list = [
                TransactionDTO.model_validate(row, from_attributes=True)
                for row in orm_list
            ]
            return dto_list

from main_service.src.db.database import session
from main_service.src.transactions.models import TransactionsOrm
from main_service.src.transactions.schemas import TransactionDTO, TransactionAddDTO
from main_service.src.utils.base_crud_service import BaseRepository
from sqlalchemy import select


class TransactionRepository(BaseRepository[TransactionDTO, TransactionAddDTO]):
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
    async def find_all_by_user_id(cls, user_id: int, limit: int, offset: int) -> list[TransactionDTO]:
        async with session() as new_session:
            query = select(TransactionsOrm).where(TransactionsOrm.user_id == user_id).\
                limit(limit).offset(offset).order_by(TransactionsOrm.id)
            result = await new_session.execute(query)
            orm_list = result.unique().scalars().all()
            dto_list = [TransactionDTO.model_validate(row, from_attributes=True) for row in orm_list]
            return dto_list

from datetime import date
from typing import Optional

from sqlalchemy import select, insert

from currency_service.src.domain.entities.exchange_rate import ExchangeRateDTO, AddExchangeRateDTO
from currency_service.src.infrastructure.models.exchange_rate import ExchangeRateORM
from currency_service.src.infrastructure.repositories.db_repo import database_repository


class ExchangeRateRepository:

    def __init__(self, db_repository):
        self.repository = db_repository

    async def get_exchange_rate_by_date(self, required_date: date) -> Optional[ExchangeRateDTO]:
        async with self.repository.a_sessionmaker() as new_session:
            query = (
                select(ExchangeRateORM)
                .where(ExchangeRateORM.request_date == required_date)
            )
            result = await new_session.execute(query)
            orm_exchange_rate = result.unique().scalars().one_or_none()
            if orm_exchange_rate is None:
                return None
            else:
                dto_exchange_rate = ExchangeRateDTO.model_validate(orm_exchange_rate, from_attributes=True)
                return dto_exchange_rate

    async def insert_exchange_rate(self, exchange_rate_dto: AddExchangeRateDTO) -> int:
        async with self.repository.a_sessionmaker() as new_session:
            insert_stmt = insert(ExchangeRateORM).values(
                base_currency=exchange_rate_dto.base_currency,
                request_date=exchange_rate_dto.request_date,
                rates=exchange_rate_dto.rates
            )
            result = await new_session.execute(insert_stmt)
            await new_session.commit()
            return result.inserted_primary_key[0]

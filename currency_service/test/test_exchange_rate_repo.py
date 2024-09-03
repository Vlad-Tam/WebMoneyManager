import datetime

from sqlalchemy import insert, select

from conftest import DatabaseRepositoryTest, database_repository_test
from currency_service.src.domain.entities.exchange_rate import ExchangeRateDTO
from currency_service.src.infrastructure.models.exchange_rate import ExchangeRateORM
from currency_service.src.infrastructure.repositories.exchange_rate_repo import ExchangeRateRepository


async def test_insert_exchange_rate():
    test_repo = ExchangeRateRepository(database_repository_test)
    rates = {
        "BYN": 3.6729,
        "RUB": 70.2681,
        "EUR": 89.467815
    }
    exchange_rate = ExchangeRateDTO(
        base_currency='USD',
        request_date=datetime.date(2024, 9, 1),
        rates=rates,
        id=1
    )
    await test_repo.insert_exchange_rate(exchange_rate)
    async with DatabaseRepositoryTest.a_sessionmaker() as session:
        query = select(ExchangeRateORM)
        result = await session.execute(query)
        exchange_rates = result.scalars().all()
        assert len(exchange_rates) == 1
        assert exchange_rates[0].id == 1
        assert exchange_rates[0].base_currency == "USD"
        assert exchange_rates[0].request_date == datetime.date(2024, 9, 1)
        assert exchange_rates[0].rates == rates


async def test_get_exchange_rate_by_date():
    test_repo = ExchangeRateRepository(database_repository_test)
    required_date = datetime.date(2024, 9, 1)
    not_required_date = datetime.date(2024, 2, 3)
    test_data_list = [
        {
            "id": 1,
            "base_currency": "USD",
            "request_date": required_date,
            "rates": {"BYN": 3.6729, "RUB": 70.2681, "EUR": 89.467815}
        },
        {
            "id": 2,
            "base_currency": "EUR",
            "request_date": not_required_date,
            "rates": {"BYN": 4.3261, "RUB": 80.1234, "USD": 1.12}
        }
    ]
    async with DatabaseRepositoryTest.a_sessionmaker() as session:
        stmt = insert(ExchangeRateORM).values(
            test_data_list
        )
        await session.execute(stmt)
        await session.commit()

    result_dto = await test_repo.get_exchange_rate_by_date(required_date)
    assert result_dto.request_date == required_date

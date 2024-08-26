from sqlalchemy import Column, Integer, Date, JSON, String

from currency_service.src.infrastructure.models.base import Base


class ExchangeRateORM(Base):
    __tablename__ = "exchange_rate"

    id = Column(Integer, primary_key=True, index=True)
    base_currency = Column(String(3), nullable=False)
    request_date = Column(Date, nullable=False, index=True)
    rates = Column(JSON, nullable=False)

from datetime import date, datetime
from typing import Optional

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import text

from main_service.src.infrastructure.models.base import Base
from main_service.src.domain.entities.user import Currency


class UserOrm(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    surname: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    main_currency: Mapped[Currency]
    month_limit: Mapped[Optional[float]]
    birth_date: Mapped[date]
    created_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )

    Categories: Mapped[list["CategoriesOrm"]] = relationship()

    @classmethod
    def get_db(cls, session: "AsyncSession"):
        return SQLAlchemyUserDatabase(session, UserOrm)

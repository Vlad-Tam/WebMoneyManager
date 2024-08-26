from datetime import date, datetime
from typing import Optional

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import text

from main_service.src.db.database import Base
from main_service.src.users.schemas import Currency


class UserOrm(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    surname: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    main_currency: Mapped[Currency]
    month_limit: Mapped[Optional[float]]
    birth_date: Mapped[date]
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))

    categories: Mapped[list["CategoriesOrm"]] = relationship(back_populates="user", lazy="selectin")
    transactions: Mapped[list["TransactionsOrm"]] = relationship(back_populates="user", lazy="selectin")

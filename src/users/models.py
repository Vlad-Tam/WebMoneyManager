from datetime import date, datetime

from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import text
from src.db.database import Base
from src.users.schemas import Currency


class UserOrm(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    surname: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]
    main_currency: Mapped[Currency]
    birth_date: Mapped[date]
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))


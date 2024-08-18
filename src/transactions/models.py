from datetime import datetime
from typing import Optional

from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import text, ForeignKey

from src.categories.models import CategoriesOrm
from src.db.database import Base
from src.transactions.schemas import TransactionType
from src.users.models import UserOrm


class TransactionsOrm(Base):
    __tablename__ = "transaction"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey(UserOrm.id, ondelete="CASCADE"))
    category_id: Mapped[int] = mapped_column(ForeignKey(CategoriesOrm.id, ondelete="CASCADE"))
    value: Mapped[float]
    description: Mapped[Optional[str]]
    operation_type: Mapped[TransactionType] = mapped_column(ENUM(TransactionType, name='transaction_type'))
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))

    user: Mapped["UserOrm"] = relationship(back_populates="transactions", lazy="joined")
    category: Mapped["CategoriesOrm"] = relationship(back_populates="transactions", lazy="joined")

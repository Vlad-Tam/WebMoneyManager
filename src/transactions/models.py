import enum
from datetime import datetime

from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import text, ForeignKey, func
from src.db.database import Base
from src.transactions.schemas import TransactionType


class TransactionsOrm(Base):
    __tablename__ = "transaction"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id", ondelete="CASCADE"))
    value: Mapped[float]
    description: Mapped[str]
    operation_type: Mapped[TransactionType] = mapped_column(ENUM(TransactionType, name='transaction_type'))
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))

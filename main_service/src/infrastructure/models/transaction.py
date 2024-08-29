from datetime import datetime
from typing import Optional

from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import text, ForeignKey


from main_service.src.infrastructure.models.base import Base
from main_service.src.domain.entities.transaction import TransactionType

from main_service.src.infrastructure.models.category import CategoriesOrm
from main_service.src.infrastructure.models.user import UserOrm


class TransactionsOrm(Base):
    __tablename__ = "transaction"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey(UserOrm.id, ondelete="CASCADE"))
    category_id: Mapped[int] = mapped_column(
        ForeignKey(CategoriesOrm.id, ondelete="CASCADE")
    )
    value: Mapped[float]
    description: Mapped[Optional[str]]
    operation_type: Mapped[TransactionType] = mapped_column(
        ENUM(TransactionType, name="transaction_type")
    )
    created_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())")
    )

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.database import Base
from src.users.models import UserOrm


class CategoriesOrm(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey(UserOrm.id, ondelete="CASCADE"))
    name: Mapped[str]
    is_default: Mapped[bool]

    user: Mapped["UserOrm"] = relationship(back_populates="categories", lazy="joined")
    transactions: Mapped[list["TransactionsOrm"]] = relationship(back_populates="category", lazy="joined")


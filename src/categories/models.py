from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.db.database import Base


class CategoriesOrm(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    name: Mapped[str]
    is_default: Mapped[bool]

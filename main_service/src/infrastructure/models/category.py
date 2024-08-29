from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from main_service.src.infrastructure.models.base import Base
from main_service.src.infrastructure.models.user import UserOrm


class CategoriesOrm(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey(UserOrm.id, ondelete="CASCADE"))
    name: Mapped[str]
    is_default: Mapped[bool]

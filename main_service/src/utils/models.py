from datetime import datetime

from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import text

from main_service.src.db.database import Base


class ChangeTrackerOrm(Base):
    __tablename__ = "change_tracker"

    id: Mapped[int] = mapped_column(primary_key=True)
    changed_table: Mapped[str]
    changed_id: Mapped[str]
    changed_datetime: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    operation: Mapped[str]

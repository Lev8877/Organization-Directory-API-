from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey

from database import Base

class Activity(Base):
    __tablename__ = "activities"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("activities.id"), nullable=True)

    organizations: Mapped[list["Organization"]] = relationship(secondary="organization_activities", back_populates="activities")
    parent: Mapped["Activity | None"] = relationship(back_populates="children", remote_side=[id])
    children: Mapped[list["Activity"]] = relationship(back_populates="parent")
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey

from database import Base

class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    building_id: Mapped[int] = mapped_column(ForeignKey("buildings.id"))

    building: Mapped["Building"] = relationship(back_populates="organizations")
    activities: Mapped[list["Activity"]] = relationship(secondary="organization_activities", back_populates="organizations")
    phones: Mapped[list["Phone"]] = relationship(back_populates="organization")
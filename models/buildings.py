from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String

from database import Base

class Building(Base):
    __tablename__ = "buildings"

    id: Mapped[int] = mapped_column(primary_key=True)
    address: Mapped[str] = mapped_column(String(255))
    latitude: Mapped[float] = mapped_column()
    longitude: Mapped[float] = mapped_column()

    organizations: Mapped[list["Organization"]] = relationship(back_populates="building")

    

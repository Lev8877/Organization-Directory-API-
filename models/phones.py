from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String

from database import Base 

class Phone(Base): 
    __tablename__ = "phones"

    id: Mapped[int] = mapped_column(primary_key=True)
    phone: Mapped[str] = mapped_column(String(20))

    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"))

    organization: Mapped["Organization"] = relationship(back_populates="phones")

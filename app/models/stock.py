from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Stock(Base):
    __tablename__ = "stock"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    center_id: Mapped[int] = mapped_column(Integer, ForeignKey("donation_centers.id"), nullable=False)
    donation_type: Mapped[str] = mapped_column(String(100), nullable=False)
    quantity: Mapped[str] = mapped_column(String(100), nullable=False, default="0")
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    center = relationship("DonationCenter", back_populates="stock")

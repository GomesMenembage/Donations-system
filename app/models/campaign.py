from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Campaign(Base):
    __tablename__ = "campaigns"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    center_id: Mapped[int] = mapped_column(Integer, ForeignKey("donation_centers.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    donation_type: Mapped[str] = mapped_column(String(100), nullable=False)
    goal: Mapped[str | None] = mapped_column(String(255), nullable=True)
    deadline: Mapped[date | None] = mapped_column(Date, nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="active")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    center = relationship("DonationCenter", back_populates="campaigns")
    donations = relationship("Donation", back_populates="campaign")

from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Donation(Base):
    __tablename__ = "donations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    donor_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    center_id: Mapped[int] = mapped_column(Integer, ForeignKey("donation_centers.id"), nullable=False)
    campaign_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("campaigns.id"), nullable=True)
    type: Mapped[str] = mapped_column(String(100), nullable=False)
    quantity: Mapped[str] = mapped_column(String(100), nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    donor = relationship("User", back_populates="donations", foreign_keys=[donor_id])
    center = relationship("DonationCenter", back_populates="donations")
    campaign = relationship("Campaign", back_populates="donations")

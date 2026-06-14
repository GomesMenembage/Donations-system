from sqlalchemy.orm import Session

from app.models.donation import Donation
from app.models.donation_center import DonationCenter
from app.models.notification import Notification
from app.utils.notifications import send_notification


def list_centers(db: Session, status: str = "approved") -> list[DonationCenter]:
    return db.query(DonationCenter).filter(DonationCenter.status == status).all()


def register_donation(
    db: Session,
    donor_id: int,
    center_id: int,
    donation_type: str,
    quantity: str,
    date: str,
    campaign_id: int | None = None,
) -> Donation:
    center = db.query(DonationCenter).filter(DonationCenter.id == center_id).first()
    if not center:
        raise ValueError("Donation center not found")

    donation = Donation(
        donor_id=donor_id,
        center_id=center_id,
        campaign_id=campaign_id,
        type=donation_type,
        quantity=quantity,
        date=date,
        status="pending",
    )
    db.add(donation)
    db.commit()
    db.refresh(donation)
    return donation


def list_donations(db: Session, donor_id: int) -> list[Donation]:
    return db.query(Donation).filter(Donation.donor_id == donor_id).order_by(Donation.created_at.desc()).all()


def list_notifications(db: Session, user_id: int) -> list[Notification]:
    return db.query(Notification).filter(Notification.user_id == user_id).order_by(Notification.created_at.desc()).all()


def mark_notification_read(db: Session, notification_id: int, user_id: int) -> Notification:
    notification = db.query(Notification).filter(Notification.id == notification_id, Notification.user_id == user_id).first()
    if not notification:
        raise ValueError("Notification not found")
    notification.read = True
    db.commit()
    db.refresh(notification)
    return notification

from sqlalchemy.orm import Session

from app.models.donation import Donation
from app.models.donation_center import DonationCenter
from app.models.user import User
from app.utils.notifications import send_notification


def list_pending_centers(db: Session) -> list[DonationCenter]:
    return db.query(DonationCenter).filter(DonationCenter.status == "pending").all()


def approve_center(db: Session, center_id: int) -> DonationCenter:
    center = db.query(DonationCenter).filter(DonationCenter.id == center_id).first()
    if not center:
        raise ValueError("Donation center not found")
    center.status = "approved"
    user = db.query(User).filter(User.id == center.user_id).first()
    if user:
        user.status = "active"
    db.commit()
    db.refresh(center)
    send_notification(db, center.user_id, "Center Approved", "Your donation center has been approved!")
    return center


def reject_center(db: Session, center_id: int) -> DonationCenter:
    center = db.query(DonationCenter).filter(DonationCenter.id == center_id).first()
    if not center:
        raise ValueError("Donation center not found")
    center.status = "rejected"
    db.commit()
    db.refresh(center)
    send_notification(db, center.user_id, "Center Rejected", "Your donation center registration has been rejected.")
    return center


def list_users(db: Session, role: str | None = None) -> list[User]:
    query = db.query(User)
    if role:
        query = query.filter(User.role == role)
    return query.all()


def suspend_user(db: Session, user_id: int) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError("User not found")
    user.status = "suspended"
    db.commit()
    db.refresh(user)
    return user


def reactivate_user(db: Session, user_id: int) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError("User not found")
    user.status = "active"
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int) -> None:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError("User not found")
    db.delete(user)
    db.commit()


def get_dashboard_stats(db: Session) -> dict:
    total_users = db.query(User).count()
    total_donors = db.query(User).filter(User.role == "donor").count()
    total_centers = db.query(DonationCenter).count()
    active_centers = db.query(DonationCenter).filter(DonationCenter.status == "approved").count()
    total_donations = db.query(Donation).count()
    confirmed_donations = db.query(Donation).filter(Donation.status == "confirmed").count()
    return {
        "total_users": total_users,
        "total_donors": total_donors,
        "total_centers": total_centers,
        "active_centers": active_centers,
        "total_donations": total_donations,
        "confirmed_donations": confirmed_donations,
    }


def send_global_notification(db: Session, title: str, body: str, role: str | None = None) -> int:
    query = db.query(User)
    if role:
        query = query.filter(User.role == role)
    users = query.all()
    for user in users:
        send_notification(db, user.id, title, body)
    return len(users)

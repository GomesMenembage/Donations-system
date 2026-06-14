from datetime import date

from sqlalchemy.orm import Session

from app.models.campaign import Campaign
from app.models.donation import Donation
from app.models.donation_center import DonationCenter
from app.models.stock import Stock
from app.utils.notifications import send_notification


def get_center_by_user(db: Session, user_id: int) -> DonationCenter:
    center = db.query(DonationCenter).filter(DonationCenter.user_id == user_id).first()
    if not center:
        raise ValueError("Donation center not found")
    return center


def update_center(db: Session, user_id: int, data: dict) -> DonationCenter:
    center = get_center_by_user(db, user_id)
    for key, value in data.items():
        if value is not None:
            setattr(center, key, value)
    db.commit()
    db.refresh(center)
    return center


def create_campaign(db: Session, user_id: int, title: str, donation_type: str, goal: str | None, deadline: date | None) -> Campaign:
    center = get_center_by_user(db, user_id)
    campaign = Campaign(
        center_id=center.id,
        title=title,
        donation_type=donation_type,
        goal=goal,
        deadline=deadline,
    )
    db.add(campaign)
    db.commit()
    db.refresh(campaign)
    return campaign


def list_campaigns(db: Session, user_id: int) -> list[Campaign]:
    center = get_center_by_user(db, user_id)
    return db.query(Campaign).filter(Campaign.center_id == center.id).order_by(Campaign.created_at.desc()).all()


def list_center_donations(db: Session, user_id: int, status: str | None = None) -> list[Donation]:
    center = get_center_by_user(db, user_id)
    query = db.query(Donation).filter(Donation.center_id == center.id)
    if status:
        query = query.filter(Donation.status == status)
    return query.order_by(Donation.created_at.desc()).all()


def confirm_donation(db: Session, user_id: int, donation_id: int) -> Donation:
    center = get_center_by_user(db, user_id)
    donation = db.query(Donation).filter(Donation.id == donation_id, Donation.center_id == center.id).first()
    if not donation:
        raise ValueError("Donation not found")
    if donation.status == "confirmed":
        raise ValueError("Donation already confirmed")

    donation.status = "confirmed"
    db.commit()
    db.refresh(donation)

    stock_entry = db.query(Stock).filter(
        Stock.center_id == center.id,
        Stock.donation_type == donation.type,
    ).first()

    if stock_entry:
        old_qty = int(stock_entry.quantity) if stock_entry.quantity.isdigit() else 0
        new_qty = int(donation.quantity) if donation.quantity.isdigit() else 0
        stock_entry.quantity = str(old_qty + new_qty)
    else:
        stock_entry = Stock(
            center_id=center.id,
            donation_type=donation.type,
            quantity=donation.quantity,
        )
        db.add(stock_entry)

    db.commit()

    send_notification(db, donation.donor_id, "Donation Confirmed", f"Your donation of {donation.quantity} {donation.type} has been confirmed.")

    return donation


def get_stock(db: Session, user_id: int) -> list[Stock]:
    center = get_center_by_user(db, user_id)
    return db.query(Stock).filter(Stock.center_id == center.id).all()

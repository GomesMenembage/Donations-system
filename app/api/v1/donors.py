from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_role
from app.database import get_db
from app.models.user import User
from app.schemas.donation import DonationOut, DonationRegister
from app.schemas.donation_center import DonationCenterOut
from app.schemas.notification import NotificationOut
from app.services import donor as donor_service

router = APIRouter()


@router.get("/centers", response_model=list[DonationCenterOut])
def list_centers(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return donor_service.list_centers(db)


@router.post("/donations", response_model=DonationOut)
def register_donation(
    payload: DonationRegister,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("donor")),
):
    try:
        return donor_service.register_donation(
            db,
            donor_id=user.id,
            center_id=payload.center_id,
            donation_type=payload.type,
            quantity=payload.quantity,
            date=payload.date,
            campaign_id=payload.campaign_id,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/donations", response_model=list[DonationOut])
def list_donations(db: Session = Depends(get_db), user: User = Depends(require_role("donor"))):
    return donor_service.list_donations(db, donor_id=user.id)


@router.get("/notifications", response_model=list[NotificationOut])
def list_notifications(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return donor_service.list_notifications(db, user_id=user.id)


@router.patch("/notifications/{notification_id}/read", response_model=NotificationOut)
def mark_read(notification_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    try:
        return donor_service.mark_notification_read(db, notification_id=notification_id, user_id=user.id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

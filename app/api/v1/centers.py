from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_role
from app.database import get_db
from app.models.user import User
from app.schemas.campaign import CampaignCreate, CampaignOut
from app.schemas.donation import DonationOut
from app.schemas.donation_center import DonationCenterOut, DonationCenterUpdate
from app.schemas.stock import StockOut
from app.services import center as center_service

router = APIRouter()


@router.get("/me", response_model=DonationCenterOut)
def get_profile(db: Session = Depends(get_db), user: User = Depends(require_role("center"))):
    try:
        return center_service.get_center_by_user(db, user_id=user.id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/me", response_model=DonationCenterOut)
def update_profile(payload: DonationCenterUpdate, db: Session = Depends(get_db), user: User = Depends(require_role("center"))):
    return center_service.update_center(db, user_id=user.id, data=payload.model_dump(exclude_none=True))


@router.post("/campaigns", response_model=CampaignOut)
def create_campaign(payload: CampaignCreate, db: Session = Depends(get_db), user: User = Depends(require_role("center"))):
    try:
        return center_service.create_campaign(
            db,
            user_id=user.id,
            title=payload.title,
            donation_type=payload.donation_type,
            goal=payload.goal,
            deadline=payload.deadline,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/campaigns", response_model=list[CampaignOut])
def list_campaigns(db: Session = Depends(get_db), user: User = Depends(require_role("center"))):
    return center_service.list_campaigns(db, user_id=user.id)


@router.get("/donations", response_model=list[DonationOut])
def list_donations(
    status: str | None = Query(None),
    db: Session = Depends(get_db),
    user: User = Depends(require_role("center")),
):
    return center_service.list_center_donations(db, user_id=user.id, status=status)


@router.patch("/donations/{donation_id}/confirm", response_model=DonationOut)
def confirm_donation(donation_id: int, db: Session = Depends(get_db), user: User = Depends(require_role("center"))):
    try:
        return center_service.confirm_donation(db, user_id=user.id, donation_id=donation_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/stock", response_model=list[StockOut])
def get_stock(db: Session = Depends(get_db), user: User = Depends(require_role("center"))):
    return center_service.get_stock(db, user_id=user.id)

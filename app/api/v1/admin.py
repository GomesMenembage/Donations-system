from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_role
from app.database import get_db
from app.models.user import User
from app.schemas.donation_center import DonationCenterOut
from app.schemas.user import UserOut
from app.services import admin as admin_service

router = APIRouter()


@router.get("/centers/pending", response_model=list[DonationCenterOut])
def list_pending_centers(db: Session = Depends(get_db), user: User = Depends(require_role("admin"))):
    return admin_service.list_pending_centers(db)


@router.patch("/centers/{center_id}/approve", response_model=DonationCenterOut)
def approve_center(center_id: int, db: Session = Depends(get_db), user: User = Depends(require_role("admin"))):
    try:
        return admin_service.approve_center(db, center_id=center_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/centers/{center_id}/reject", response_model=DonationCenterOut)
def reject_center(center_id: int, db: Session = Depends(get_db), user: User = Depends(require_role("admin"))):
    try:
        return admin_service.reject_center(db, center_id=center_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/users", response_model=list[UserOut])
def list_users(role: str | None = None, db: Session = Depends(get_db), user: User = Depends(require_role("admin"))):
    return admin_service.list_users(db, role=role)


@router.patch("/users/{user_id}/suspend", response_model=UserOut)
def suspend_user(user_id: int, db: Session = Depends(get_db), user: User = Depends(require_role("admin"))):
    try:
        return admin_service.suspend_user(db, user_id=user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/users/{user_id}/reactivate", response_model=UserOut)
def reactivate_user(user_id: int, db: Session = Depends(get_db), user: User = Depends(require_role("admin"))):
    try:
        return admin_service.reactivate_user(db, user_id=user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), user: User = Depends(require_role("admin"))):
    try:
        admin_service.delete_user(db, user_id=user_id)
        return {"message": "User deleted"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/dashboard")
def dashboard(db: Session = Depends(get_db), user: User = Depends(require_role("admin"))):
    return admin_service.get_dashboard_stats(db)


@router.post("/notifications/send")
def send_notification(
    title: str,
    body: str,
    role: str | None = None,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("admin")),
):
    count = admin_service.send_global_notification(db, title=title, body=body, role=role)
    return {"message": f"Notification sent to {count} users"}

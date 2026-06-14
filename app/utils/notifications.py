from sqlalchemy.orm import Session

from app.models.notification import Notification


def send_notification(db: Session, user_id: int, title: str, body: str) -> Notification:
    notification = Notification(user_id=user_id, title=title, body=body)
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification

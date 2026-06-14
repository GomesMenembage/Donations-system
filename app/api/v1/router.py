from fastapi import APIRouter

from app.api.v1 import admin, auth, centers, donors

router = APIRouter(prefix="/api")

router.include_router(auth.router, prefix="/auth", tags=["Auth"])
router.include_router(donors.router, prefix="/donors", tags=["Donors"])
router.include_router(centers.router, prefix="/centers", tags=["Centers"])
router.include_router(admin.router, prefix="/admin", tags=["Admin"])

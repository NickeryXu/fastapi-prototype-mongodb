from fastapi import APIRouter

from app.api.user import router as user_router

router = APIRouter()
'''
example:
    router.include_router(xxx, tags=["xxx"], prefix="/xxx")
'''

router.include_router(user_router)

from fastapi import APIRouter, Depends

from app.core.config import settings

from .brand import router as brand_router
from .car import router as car_router
from .roles import router as role_router
from .services import router as service_router
from .user import router as user_router
from .role_user import router as role_user_router
from .customer_cars import router as customer_car_router
from .order import router as order_router
from .order_service import router as order_service_router
from .auth import router as auth_router
from .profile import router as profile_router

router = APIRouter(
    prefix=settings.api.v1.prefix,
)

router.include_router(auth_router)
router.include_router(profile_router)
router.include_router(order_router)
router.include_router(user_router)
router.include_router(brand_router)
router.include_router(car_router)
router.include_router(role_router)
router.include_router(service_router)
router.include_router(role_user_router)
router.include_router(customer_car_router)
router.include_router(order_service_router)

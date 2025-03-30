from fastapi import APIRouter

from app.api.routes import (
    items, 
    login, 
    private, 
    users, 
    utils, 
    apartments, 
    clients, 
    payment_types, 
    payments, 
    history
)
from app.core.config import settings

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(users.router)
api_router.include_router(utils.router)
api_router.include_router(items.router)
api_router.include_router(apartments.router)
api_router.include_router(clients.router)
api_router.include_router(payment_types.router)
api_router.include_router(payments.router)
api_router.include_router(history.router)


if settings.ENVIRONMENT == "local":
    api_router.include_router(private.router)

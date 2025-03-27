from fastapi import APIRouter

from app.api.endpoints import auth, users, customers, tickets, bikes, parts

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(customers.router, prefix="/customers", tags=["customers"])
api_router.include_router(bikes.router, prefix="/bikes", tags=["bikes"])
api_router.include_router(tickets.router, prefix="/tickets", tags=["tickets"])
api_router.include_router(parts.router, prefix="/parts", tags=["parts"])
from fastapi import APIRouter
from core.lifespan import db

driver_route = APIRouter(prefix="/driver", tags=["DRIVER"])
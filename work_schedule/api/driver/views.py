from fastapi import APIRouter
from icecream import ic

from api.driver.schemes import DriverCreateSchema, DriverSchema, DriverUpdateSchema
from core.lifespan import db

driver_route = APIRouter(prefix="/driver", tags=["DRIVER"])


@driver_route.get(
    "/{id_}",
    summary="получить",
    description="Получить данные по водителю.",
    response_model=DriverSchema,
)
async def get(id_: int):
    return await db.driver.get_by_id(id_)


@driver_route.post(
    "",
    summary="добавить",
    description="Добавить водителя.",
    response_model=DriverSchema,
)
async def create(driver: DriverCreateSchema):
    return await db.driver.create(**driver.model_dump())


@driver_route.put(
    "",
    summary="обновить",
    description="Обновить водителя.",
    response_model=DriverSchema,
)
async def update(driver: DriverUpdateSchema):
    return await db.driver.update(id_=driver.id, **driver.model_dump(exclude={"id"}))


@driver_route.delete(
    "/{id_}",
    summary="удалить",
    description="Удалить водителя.",
    response_model=DriverSchema,
)
async def delete(id_: int):
    return await db.driver.delete_by_id(id_)

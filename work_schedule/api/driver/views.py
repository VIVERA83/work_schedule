from api.base.schemes import ID
from api.driver.schemes import DriverCreateSchema, DriverSchema, DriverUpdateSchema
from core.lifespan import db
from fastapi import APIRouter

driver_route = APIRouter(prefix="/driver", tags=["DRIVER"])


@driver_route.get(
    "/{id_}",
    summary="получить",
    description="Получить данные по водителю.",
    response_model=DriverSchema,
)
async def get(id_: ID):
    return await db.driver.get_by_id(id_)


@driver_route.post(
    "",
    summary="добавить",
    description="Добавить водителя.",
    response_model=DriverSchema,
)
async def create(data: DriverCreateSchema):
    return await db.driver.create(**data.model_dump())


@driver_route.put(
    "",
    summary="обновить",
    description="Обновить водителя.",
    response_model=DriverSchema,
)
async def update(data: DriverUpdateSchema):
    return await db.driver.update(id_=data.id, **data.model_dump(exclude={"id"}))


@driver_route.delete(
    "/{id_}",
    summary="удалить",
    description="Удалить водителя.",
    response_model=DriverSchema,
)
async def delete(id_: int):
    return await db.driver.delete_by_id(id_)

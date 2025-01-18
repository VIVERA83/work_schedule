from fastapi import APIRouter

from api.base.schemes import ID
from api.car.schemes import CarSchema, CarCreateSchema, CarUpdateSchema
from core.lifespan import db

car_route = APIRouter(prefix="/car", tags=["CAR"])


@car_route.get(
    "/{id_}",
    summary="получить",
    description="Получить данные по машине.",
    response_model=CarSchema,
)
async def get(id_: ID):
    return await db.car.get_by_id(id_)


@car_route.post(
    "",
    summary="добавить",
    description="Добавить машину.",
    response_model=CarSchema,
)
async def create(data: CarCreateSchema):
    return await db.car.create(**data.model_dump())


@car_route.put(
    "",
    summary="обновить",
    description="Обновить машину.",
    response_model=CarSchema,
)
async def update(data: CarUpdateSchema):
    return await db.car.update(id_=data.id, **data.model_dump(exclude={"id"}))


@car_route.delete(
    "/{id_}",
    summary="удалить",
    description="Удалить машину.",
    response_model=CarSchema,
)
async def delete(id_: int):
    return await db.car.delete_by_id(id_)

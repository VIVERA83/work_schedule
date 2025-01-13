from fastapi import APIRouter

from api.driver.schemes import DriverFullDataSchema, DriverCreateSchema, DriverSchema
from core.lifespan import db

driver_route = APIRouter(prefix="/driver", tags=["DRIVER"])


@driver_route.get(
    "/{driver_id}",
    summary="получить водителя",
    description="Получить данные по водителю. Краткий формат.",
    response_model=DriverSchema,
)
async def get(driver_id: int):
    return db.get_driver_by_id(driver_id)


@driver_route.post(
    "",
    summary="Добавить водителя.",
    description="Добавить водителя.",
    response_model=DriverFullDataSchema,
)
async def create(driver: DriverCreateSchema):
    return db.create_driver(**driver.model_dump())

#
#
# @driver_route.delete(
#     "/{brand_id}",
#     summary="удалить данные производителя",
#     description="Удалить данные производителя.",
#     response_model=BrandSchema,
# )
# async def delete_brand(brand_id: UUID):
#     return await brand_accessor.delete(brand_id)
#
#
# @driver_route.get(
#     "",
#     summary="получить всех производителей",
#     description="Получить всех производителей товаров.",
#     response_model=list[BrandSchema],
# )
# async def get_brands(page: int = query_page, page_size: int = query_page_size):
#     return await brand_accessor.get(page, page_size)
#
#
# @driver_route.get(
#     "/{brand_id}",
#     summary="получить данные по id.",
#     description="получить производителя по id",
#     response_model=BrandSchema,
# )
# async def get_brand_by_id(brand_id: UUID):
#     return await brand_accessor.get_by_id(brand_id)

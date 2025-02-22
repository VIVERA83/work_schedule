from pydantic import Field

from api.base.schemes import IdSchema


class CrewDriverCreateSchema(IdSchema):
    id_driver: int = Field(description="идентификатор водителя", examples=["1"], gt=0)


class CrewDriverSchema(IdSchema): ...


class CrewDriverUpdateSchema(IdSchema): ...

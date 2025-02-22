from pydantic import Field

from api.base.schemes import IdSchema


class CrewCarCreateSchema(IdSchema):
    id_car: int = Field(description="идентификатор машины", examples=["1"], gt=0)

class CrewCarSchema(IdSchema): ...


class CrewCarUpdateSchema(CrewCarSchema): ...

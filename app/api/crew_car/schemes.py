from pydantic import Field, BaseModel

from api.base.schemes import IdSchema


class CrewCarCreateSchema(BaseModel):
    id_crew: int = Field(description="идентификатор экипажа", examples=["1"], gt=0)
    id_car: int = Field(description="идентификатор машины", examples=["1"], gt=0)

class CrewCarSchema(IdSchema,CrewCarCreateSchema): ...


class CrewCarUpdateSchema(CrewCarSchema,CrewCarCreateSchema): ...

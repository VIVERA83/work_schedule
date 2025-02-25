from pydantic import Field, BaseModel

from api.base.schemes import IdSchema


class CrewDriverCreateSchema(BaseModel):
    id_crew: int = Field(description="идентификатор экипажа", examples=["1"], gt=0)
    id_driver: int = Field(description="идентификатор водителя", examples=["1"], gt=0)


class CrewDriverSchema(IdSchema, CrewDriverCreateSchema): ...


class CrewDriverUpdateSchema(IdSchema, CrewDriverCreateSchema): ...

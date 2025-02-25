from typing import Optional

from pydantic import Field, BaseModel

from api.base.fields import ID_CREW, ID_CAR
from api.base.schemes import IdSchema


class CrewCarCreateSchema(BaseModel):
    id_crew: int = ID_CREW
    id_car: int = ID_CAR


class CrewCarSchema(IdSchema, CrewCarCreateSchema): ...


class CrewCarUpdateSchema(IdSchema):
    id_crew: Optional[int] = Field(default=None, description="идентификатор экипажа", examples=["1"], gt=0)
    id_car: Optional[int] = Field(default=None, description="идентификатор машины", examples=["1"], gt=0)

from typing import Optional

from pydantic import BaseModel, Field

from api.base.fields import ID_CREW, ID_DRIVER
from api.base.schemes import IdSchema


class CrewDriverCreateSchema(BaseModel):
    id_crew: int = ID_CREW
    id_driver: int = ID_DRIVER


class CrewDriverSchema(IdSchema, CrewDriverCreateSchema): ...


class CrewDriverUpdateSchema(IdSchema):
    id_crew: Optional[int] = Field(default=None, description="идентификатор экипажа", examples=["1"], gt=0)
    id_driver: Optional[int] = Field(default=None, description="идентификатор водителя", examples=["1"], gt=0)

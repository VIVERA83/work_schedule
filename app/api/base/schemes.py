from typing import Annotated

from fastapi import Path, Query
from pydantic import BaseModel, Field

ID_PATH = Annotated[
    int,
    Path(
        gt=0,
        description="идентификатор объекта",
    ),
]

ID: int = Query(
    qt=0,
    description="идентификатор объекта",
    examples=[1],
)

PAGE: int = Query(
    gt=0,
    description="номер страницы",
    examples=[1],

)

PAGE_SIZE: int = Query(
    gt=0,
    lt=100,
    description="размер страницы",
    examples=[10],
)


class IdSchema(BaseModel):
    id: int = Field(
        gt=0,
        description="идентификатор объекта",
        examples=[1])

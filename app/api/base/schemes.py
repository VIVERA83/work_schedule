from typing import Annotated

from fastapi import Path
from pydantic import BaseModel, Field

ID = Annotated[
    int,
    Path(
        gt=0,
        description="идентификатор объекта",
        examples=["1"],
    ),
]


class IdSchema(BaseModel):
    id: int = Field(description="идентификатор объекта", examples=["1"])

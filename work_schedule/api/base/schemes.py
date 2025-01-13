from pydantic import BaseModel, Field


class IdSchema(BaseModel):
    id: int = Field(
        description="идентификатор объекта",
        examples=["1"]
    )

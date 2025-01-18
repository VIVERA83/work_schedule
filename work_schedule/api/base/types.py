from typing import Any, Callable, Literal, Optional, TypedDict

from pydantic import BaseModel


class ParamsType(TypedDict):
    endpoint: Callable
    methods: list[Literal["GET", "POST", "PUT", "PATCH", "DELETE"]]
    path: str
    annotations: dict[Literal["id_", "data"], Any]
    summary: str
    description: str
    request_model: BaseModel
    response_model: BaseModel


class EndpointType(TypedDict):
    get_by_id: Optional[ParamsType]
    create: Optional[ParamsType]
    update: Optional[ParamsType]
    delete_by_id: Optional[ParamsType]

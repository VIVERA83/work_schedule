from typing import Any, Callable, Literal, NotRequired, Type, TypedDict

from openpyxl.styles.builtins import total
from pydantic import BaseModel


class ParamsType(TypedDict):
    endpoint: NotRequired[Callable]
    methods: list[Literal["GET", "POST", "PUT", "PATCH", "DELETE"]]
    path: NotRequired[str]
    annotations: dict[Literal["id_", "data"], Any]
    summary: NotRequired[str]
    description: NotRequired[str]
    response_model: NotRequired[Type[BaseModel]]


class EndpointType(TypedDict):
    get_by_id: NotRequired[ParamsType]
    create: NotRequired[ParamsType]
    update: NotRequired[ParamsType]
    delete_by_id: NotRequired[ParamsType]

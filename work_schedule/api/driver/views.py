from api.base.route import BaseRoute
from api.base.schemes import ID
from api.driver.schemes import DriverCreateSchema, DriverSchema, DriverUpdateSchema
from core.lifespan import db


driver_route = BaseRoute(
    prefix="/driver",
    tags=["DRIVER"],
    db=db.driver,
    endpoints={
        "get_by_id": {
            "methods": ["GET"],
            "path": "/{id_}",
            "annotations": {"id_": ID},
            "response_model": DriverSchema,
        },
        "create": {
            "methods": ["POST"],
            "annotations": {"data": DriverCreateSchema},
            "response_model": DriverSchema,
        },
        "delete_by_id": {
            "methods": ["DELETE"],
            "path": "/{id_}",
            "annotations": {"id_": ID},
            "response_model": DriverSchema,
        },
        "update": {
            "methods": ["PUT"],
            "annotations": {"data": DriverUpdateSchema},
            "response_model": DriverSchema,
        },
    },
)

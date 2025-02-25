from api.base.route import BaseView
from api.base.schemes import ID_PATH
from api.car.schemes import CarCreateSchema, CarSchema, CarUpdateSchema
from core.lifespan import store


class CarViews(BaseView):
    class Meta:
        store = store.car
        endpoints = {
            "get_all": {
                "methods": ["GET"],
                "response_model": list[CarSchema],
            },
            "get_by_id": {
                "methods": ["GET"],
                "path": "/{id_}",  # Path parameters
                "annotations": {"id_": ID_PATH},  # Path parameters
                "response_model": CarSchema,
            },
            "create": {
                "methods": ["POST"],
                "annotations": {"data": CarCreateSchema},
                "response_model": CarSchema,
            },
            "delete_by_id": {
                "methods": ["DELETE"],
                "path": "/{id_}",  # Path parameters
                "annotations": {"id_": ID_PATH},  # Path parameters
                "response_model": CarSchema,
            },
            "update": {
                "methods": ["PUT"],
                "annotations": {"data": CarUpdateSchema},
                "response_model": CarSchema,
            },
        }

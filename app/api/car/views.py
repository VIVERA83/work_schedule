from api.base.route import BaseView
from api.base.schemes import ID
from api.car.schemes import CarCreateSchema, CarSchema, CarUpdateSchema
from core.lifespan import store


class CarViews(BaseView):
    class Meta:
        db = store.car
        endpoints = {
            "get_by_id": {
                "methods": ["GET"],
                "path": "/{id_}",
                "annotations": {"id_": ID},
                "response_model": CarSchema,
            },
            "create": {
                "methods": ["POST"],
                "annotations": {"data": CarCreateSchema},
                "response_model": CarSchema,
            },
            "delete_by_id": {
                "methods": ["DELETE"],
                "path": "/{id_}",
                "annotations": {"id_": ID},
                "response_model": CarSchema,
            },
            "update": {
                "methods": ["PUT"],
                "annotations": {"data": CarUpdateSchema},
                "response_model": CarSchema,
            },
        }

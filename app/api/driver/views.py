from api.base.route import BaseView
from api.base.schemes import ID_PATH
from api.driver.schemes import DriverCreateSchema, DriverSchema, DriverUpdateSchema
from core.lifespan import store


class DriverViews(BaseView):
    class Meta:
        store = store.driver
        endpoints = {
            "get_by_id": {
                "methods": ["GET"],
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
                "annotations": {"id_": ID_PATH},
                "response_model": DriverSchema,
            },
            "update": {
                "methods": ["PUT"],
                "annotations": {"data": DriverUpdateSchema},
                "response_model": DriverSchema,
            },
        }

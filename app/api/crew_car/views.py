from api.base.route import BaseView
from api.base.schemes import ID_PATH

from api.crew_car.schemes import CrewCarSchema, CrewCarCreateSchema, CrewCarUpdateSchema
from core.lifespan import store


class CrewCarViews(BaseView):
    class Meta:
        store = store.crew_car
        endpoints = {
            "get_by_id": {
                "methods": ["GET"],
                "response_model": CrewCarSchema,
            },
            "create": {
                "methods": ["POST"],
                "annotations": {"data": CrewCarCreateSchema},
                "response_model": CrewCarSchema,
            },
            "delete_by_id": {
                "methods": ["DELETE"],
                "path": "/{id_}",
                "annotations": {"id_": ID_PATH},
                "response_model": CrewCarSchema,
            },
            "update": {
                "methods": ["PUT"],
                "annotations": {"data": CrewCarUpdateSchema},
                "response_model": CrewCarSchema,
            },
        }

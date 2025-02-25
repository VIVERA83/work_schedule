from api.base.route import BaseView
from api.base.schemes import ID_PATH
from api.crew.schemes import CrewSchema, CrewCreateSchema
from core.lifespan import store


class CrewViews(BaseView):
    class Meta:
        store = store.crew
        endpoints = {
            "get_all": {
                "methods": ["GET"],
                "response_model": list[CrewSchema],
            },
            "get_by_id": {
                "methods": ["GET"],
                "path": "/{id_}",  # Path parameters
                "annotations": {"id_": ID_PATH},  # Path parameters
                "response_model": CrewSchema,
            },
            "create": {
                "methods": ["POST"],
                "annotations": {"data": CrewCreateSchema},
                "response_model": CrewSchema,
            },
            "delete_by_id": {
                "methods": ["DELETE"],
                "path": "/{id_}",
                "annotations": {"id_": ID_PATH},
                "response_model": CrewSchema,
            },
        }

from api.base.route import BaseView
from api.base.schemes import ID
from api.crew.schemes import CrewSchema, CrewCreateSchema, CrewUpdateSchema
from core.lifespan import store



class CrewViews(BaseView):
    class Meta:
        store = store.crew
        endpoints = {
            "get_by_id": {
                "methods": ["GET"],
                "path": "/{id_}",
                "annotations": {"id_": ID},
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
                "annotations": {"id_": ID},
                "response_model": CrewSchema,
            },
            "update": {
                "methods": ["PUT"],
                "annotations": {"data": CrewUpdateSchema},
                "response_model": CrewSchema,
            },
        }

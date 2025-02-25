from api.base.route import BaseView
from api.base.schemes import ID_PATH

from api.crew_driver.schemes import CrewDriverSchema, CrewDriverCreateSchema, CrewDriverUpdateSchema
from core.lifespan import store



class CrewDriverViews(BaseView):
    class Meta:
        store = store.crew_driver
        endpoints = {
            "get_by_id": {
                "methods": ["GET"],
                "response_model": CrewDriverSchema,
            },
            "create": {
                "methods": ["POST"],
                "annotations": {"data": CrewDriverCreateSchema},
                "response_model": CrewDriverSchema,
            },
            "delete_by_id": {
                "methods": ["DELETE"],
                "path": "/{id_}",
                "annotations": {"id_": ID_PATH},
                "response_model": CrewDriverSchema,
            },
            "update": {
                "methods": ["PUT"],
                "annotations": {"data": CrewDriverUpdateSchema},
                "response_model": CrewDriverSchema,
            },
        }

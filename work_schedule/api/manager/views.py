from api.base.route import BaseView
from api.manager.schemes import CreateSchema
from core.lifespan import db


class ManagerViews(BaseView):
    class Meta:
        db = db.manager
        endpoints = {
            "create": {
                "methods": ["POST"],
                "annotations": {"data": CreateSchema},
                "response_model": CreateSchema,
            },
        }

from logging import Logger

from manager.drivers_planner.manager import DriversPlannerManager
from store.store import Store


class Manager:
    def __init__(self, store: Store, logger: Logger):
        self.drivers_planner = DriversPlannerManager(store, logger)

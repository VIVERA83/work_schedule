from manager.drivers_planner.manager import DriversPlannerManager
from store.store import Store


class Manager:
    def __init__(self, store: Store):
        self.store = store
        self.drivers_planner = DriversPlannerManager(self.store)

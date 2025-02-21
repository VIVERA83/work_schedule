from logging import Logger

from store.store import Store


class BaseManager:
    def __init__(self, store: Store, logger: Logger):
        self.store = store
        self.logger = logger

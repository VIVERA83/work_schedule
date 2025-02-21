from store.store import Store


class BaseManager:
    def __init__(self, store: Store):
        self.store = store

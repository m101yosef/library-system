class Auditlog:
    def __init__(self):
        self._events : list[str] = []
    def record(self, message : str):
        self._events.append(message)
    def all(self) -> list[str]:
        return self._events

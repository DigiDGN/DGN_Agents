# In-memory session registry

class SessionStore:
    def __init__(self):
        self._sessions = {}
        self._default_id = None

    def add(self, session):
        self._sessions[session.id] = session
        if self._default_id is None:
            self._default_id = session.id

    def get(self, id=None):
        if id is None:
            id = self._default_id
        return self._sessions.get(id)

    @property
    def default_id(self):
        return self._default_id

    def set_default(self, id):
        if id in self._sessions:
            self._default_id = id

    def delete(self, id):
        if id in self._sessions:
            del self._sessions[id]
            if id == self._default_id:
                self._default_id = next(iter(self._sessions), None)

    def clear(self):
        self._sessions.clear()
        self._default_id = None

    def count(self):
        return len(self._sessions)

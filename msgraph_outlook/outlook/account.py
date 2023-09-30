class Account:
    def __init__(self, client, user: str = None):
        self._client = client
        self._user = user

    def create_message(self):
        from .message import Message

        return Message(client=self._client, user=self._user)

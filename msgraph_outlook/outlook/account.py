class Account:
    """Represents Microsoft Graph User Object

    https://learn.microsoft.com/en-us/graph/api/resources/user?view=graph-rest-1.0
    """

    def __init__(self, client, user: str = None):
        """Initializes Account object

        Parameters
        ----------
            client : _type_
                GraphClient
            user (str, optional): str, default None
                Username to delegate for, otherwise assumes 'me' property
        """
        self._client = client
        self._user = user

    def create_message(self):
        """Creates new Message Object

        Returns
        -------
            _type_
                Message Object
        """
        from .message import Message

        return Message(client=self._client, user=self._user)

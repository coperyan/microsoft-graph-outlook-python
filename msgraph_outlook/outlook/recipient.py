from typing import Union


class Recipient:
    """Recipient Item

    https://learn.microsoft.com/en-us/graph/api/resources/recipient?view=graph-rest-1.0
    """

    def __init__(self, address: str = None, name: str = None):
        self._address = address
        self._name = name

    @property
    def address(self) -> str:
        return self._address

    @address.setter
    def address(self, address: str):
        self._address = address

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    def get_json_format(self) -> dict:
        """Returns JSON representation of Recipient object

        https://learn.microsoft.com/en-us/graph/api/resources/recipient?view=graph-rest-1.0

        Returns
        -------
            dict
        """
        d = {"emailAddress": {"address": self.address}}
        if self.name:
            d["emailAddress"]["name"] = self.name
        return d


class Recipients:
    """Collection of Recipient items"""

    def __init__(self, recipients: Union[list, str]):
        self._recipients = []

        if recipients:
            self.add(recipients)

    def add(self, recipients: Union[list, str, tuple]):
        """Adds new recipient to collection

        Parameters
        ----------
            recipients : Union[list, str, tuple]
            recipient(s) to add to collection
                str = "emailaddress@domain.com"
                tuple = ("emailaddress@domain.com","name")
                list = [str,str] or [tuple, tuple]

        """
        if isinstance(recipients, str):
            recipients = [recipients]
        elif isinstance(recipients, tuple):
            recipients = [recipients]

        for recipient in recipients:
            if isinstance(recipient, dict):
                self._recipients.append(
                    Recipient(
                        address=recipient.get("address"), name=recipient.get("name")
                    )
                )
            elif isinstance(recipient, tuple):
                self._recipients.append(
                    Recipient(address=recipient[0], name=recipient[1])
                )

            elif isinstance(recipient, str):
                self._recipients.append(Recipient(address=recipient))

    def get_json_format(self) -> list:
        """Returns list of recipients in JSON representation

        https://learn.microsoft.com/en-us/graph/api/resources/recipient?view=graph-rest-1.0

        Returns
        -------
            list
                List of microsoft.graph.recipient items
        """
        return [r.get_json_format() for r in self._recipients]

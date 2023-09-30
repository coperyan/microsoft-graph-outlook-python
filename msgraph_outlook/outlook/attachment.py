import os
from typing import Union


class Attachment:
    def __init__(self, path: str = None, name: str = None):
        self._path = path
        self._name = name

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, path: str):
        self._path = path

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name


class Attachments:
    def __init__(self, attachments: Union[list, str]):
        self._attachments = []

        if attachments:
            self.add(attachments)

    def add(self, attachments: Union[list, str]):
        if isinstance(attachments, str):
            attachments = [attachments]

        for attachment in attachments:
            if isinstance(attachment, str):
                self._attachments.append(
                    Attachment(path=attachment.get("path"), name=attachment.get("name"))
                )
            elif isinstance(attachment, tuple):
                self._attachments.append(
                    Attachment(path=attachment[0], name=attachment[1])
                )
            elif isinstance(attachment, str):
                self._attachments.append(
                    Attachment(path=attachment, name=os.path.basename(attachment))
                )

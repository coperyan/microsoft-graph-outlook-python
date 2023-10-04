from datetime import datetime
from typing import Union

from .attachment import Attachment, Attachments
from .recipient import Recipient, Recipients
from .utils import build_url


class Message:
    """Message Object

    https://learn.microsoft.com/en-us/graph/api/resources/message?view=graph-rest-1.0

    """

    _endpoints = {
        "create_message": "/messages",
        "create_message_in_folder": "/mailFolders/{id}/messages",
        "message": "/messages/{id}",
        "send_message": "/messages/sendMail",
        "send_draft_message": "/messages/{id}/send",
    }

    def __init__(self, client, user=None, message_obj={}, **kwargs):
        """Initializes Message Object

        https://learn.microsoft.com/en-us/graph/api/resources/message?view=graph-rest-1.0

        Parameters
        ----------
            client : _type_
                GraphClient object
            user (_type_, optional): _type_, default None
                User for delegation purposes (if blank will use 'me' property)
            message_obj (dict, optional): dict, default {}
                Can initialize with message JSON if needed
        """

        self.client = client
        self.user = user
        self._id = message_obj.get("id", None)
        self._folder_id = message_obj.get("parentFolderId", None)
        self._is_draft = message_obj.get("isDraft", True)
        self._is_read = message_obj.get("isRead", None)
        self._created_datetime = message_obj.get("createdDateTime", None)
        self._last_modified_datetime = message_obj.get("lastModifiedDateTime", None)
        self._sender = Recipient(message_obj.get("from"), None)
        self._to_recipients = Recipients(
            message_obj.get("toRecipients", kwargs.get("to_recipients", []))
        )
        self._cc_recipients = Recipients(
            message_obj.get("ccRecipients", kwargs.get("cc_recipients", []))
        )
        self._bcc_recipients = Recipients(
            message_obj.get("bccRecipients", kwargs.get("bcc_recipients", []))
        )
        self._attachments = Attachments(
            message_obj.get("attachments", kwargs.get("attachments", []))
        )
        self._subject = message_obj.get("subject", "")
        self._body = message_obj.get("body", {}).get("content", "")
        self._body_type = message_obj.get("body", {}).get("contentType", "html")
        self._importance = message_obj.get("importance", "normal")

    @property
    def id(self):
        return self._id

    @property
    def sender(self):
        return self._sender

    @sender.setter
    def sender(self, sender: Union[Recipient, str]):
        if isinstance(sender, Recipient):
            self._sender = sender
        elif isinstance(sender, str):
            self._sender.address = sender
            self._sender.name = ""

    @property
    def to_recipients(self):
        return self._to_recipients

    @property
    def cc_recipients(self):
        return self._cc_recipients

    @property
    def bcc_recipients(self):
        return self._bcc_recipients

    @property
    def subject(self):
        return self._subject

    @subject.setter
    def subject(self, subject: str):
        self._subject = subject

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, body: str):
        self._body = body

    @property
    def importance(self):
        return self._importance

    @importance.setter
    def importance(self, importance):
        self._importance = importance

    @property
    def body_type(self):
        return self._body_type

    @property
    def attachments(self):
        return self._attachments

    def _build_url(self, url: str) -> str:
        return build_url(user=self.user, endpoint=url)

    def api_json(self, limit_keys: list = None) -> dict:
        """Generate MessageBody for Message

        https://learn.microsoft.com/en-us/graph/api/resources/message?view=graph-rest-1.0

        Returns
        -------
            dict
                Json/Dict representation of Message
        """
        message = {
            "subject": self.subject,
            "body": {"contentType": self.body_type, "content": self.body},
            "importance": self.importance,
        }

        if self.to_recipients:
            message["toRecipients"] = self.to_recipients.get_json_format()
        if self.cc_recipients:
            message["ccRecipients"] = self.cc_recipients.get_json_format()
        if self.bcc_recipients:
            message["bccRecipients"] = self.bcc_recipients.get_json_format()

        if limit_keys:
            for key in list(message.keys()):
                if key not in limit_keys:
                    del message[key]

        return message

    def mark_as_unread(self):
        if not self._id:
            pass  ##exception here

        data = {"isRead": False}
        url = self._build_url(self._endpoints.get("message").format(id=self._id))
        resp = self.client.patch(url, data=data)
        if not resp:
            return False

        self._is_read = False
        return True

    def mark_as_read(self):
        if not self._id:
            pass  ##exception here

        data = {"isRead": True}
        url = self._build_url(self._endpoints.get("message").format(id=self._id))
        resp = self.client.patch(url, data=data)
        if not resp:
            return False

        self._is_read = False
        return True

    def save(self):
        """Save (Existing) Message Object

        Returns
        -------
            bool
                Success of response
        """
        if self._id and not self._is_draft:
            url = self._build_url(self._endpoints.get("message").format(id=self._id))
            data = self.api_json(limit_keys=["isRead", "categories", "flag", "subject"])
            resp = self.client.patch(url, data=data)

            if not resp:
                return False

            self._last_modified_datetime = datetime.now()  ##handle timezone later

            return True
        else:
            return self.save_draft()

    def save_draft(self):
        """Save Draft of Message Object

        Will update existing message if already exists

        Returns
        -------
            bool
                Success of response

        """
        if self._id:
            url = self._build_url(self._endpoints.get("message").format(id=self.id))
            data = self.api_json()
            client_req = self.client.patch
            pass
        else:
            url = self._build_url(
                self._endpoints.get("create_message_in_folder").format(id="drafts")
            )
            data = self.api_json()
            client_req = self.client.post

        if not data:
            return True

        resp = client_req(url, data=data)
        if not resp:
            return False

        if not self._id:
            message_json = resp.json()
            self._id = message_json.get("id", None)
            self._folder_id = message_json.get("parentfolderId", None)
            self._created_datetime = message_json.get("createdDateTime", None)
            self._last_modified_datetime = message_json.get(
                "lastModifiedDateTime", None
            )
        else:
            self._last_modified_datetime = datetime.now()  ##handle timezone later

        return True

    def send(self):
        if self._id and not self._is_draft:
            pass  # error here

        if self._is_draft and self._id:
            self.save_draft()
            url = self._build_url(
                self._endpoints.get("send_draft_message").format(id=self._id)
            )
            resp = self.client.post(url, data=None)

        else:
            url = self._build_url(self._endpoints.get("send_message"))
            data = {"message": self.api_json()}
            resp = self.client.post(url, data=data)

        if not resp:
            return False

        self._id = "message_sent" if not self._id else self._id
        self._is_draft = False

        return True

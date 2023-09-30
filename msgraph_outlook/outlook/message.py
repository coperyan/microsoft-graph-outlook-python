from typing import Union
from .recipient import Recipients, Recipient
from .attachment import Attachments, Attachment
from .utils import build_url


class Message:
    _endpoints = {
        "create_message": "/messages",
        "create_message_in_folder": "/mailFolders/{id}/messages",
        "message": "/messages/{id}",
    }

    def __init__(self, client, user=None, message_obj={}, **kwargs):
        """Initializes Message Object

        Parameters
        ----------
            credentials (_type_, optional): _type_, default None
                Credentials object to be used for further commands within the instance
            message_id (_type_, optional): _type_, default None
                Message ID (passed for existing items)
        """

        self.client = client
        self.user = user
        self._id = message_obj.get("id", None)
        self._folder_id = message_obj.get("parentFolderId", None)
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

    def api_json(self) -> dict:
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

        return message

    def save_draft(self):
        if self._id:
            ##Handle updating of existing message?
            url = self._build_url(self._endpoints.get("message").format(id=self.id))
            data = self.api_json()
            client_req = self.client.patch
            pass
        else:
            # Prevent unintended "creation of drafts?"
            url = self._build_url(
                self._endpoints.get("create_message_in_folder").format(id="drafts")
            )
            data = self.api_json()
            client_req = self.client.post

        resp = client_req(url, data=data)

        if not self._id:
            message_json = resp.json()
            self._id = message_json.get("id", None)
            self._folder_id = message_json.get("parentfolderId", None)
            self._created_datetime = message_json.get("createdDateTime", None)
            self._last_modified_datetime = message_json.get(
                "lastModifiedDateTime", None
            )

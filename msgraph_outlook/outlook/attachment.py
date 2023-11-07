import os
import base64
from typing import Union

from .utils import build_url

UPLOAD_SESSION_BYTES_THRESHOLD = 1000000 * 5


class Attachment:
    _endpoints = {
        "attach": "/messages/{id}/attachments",
        "attach_session": "/messages/{id}/attachents/createUploadSession",
    }

    def __init__(self, attachment: None, parent=None, **kwargs):
        self._attachment = attachment
        self.parent = parent
        self.kwargs = kwargs
        self._attachment_type = "file"
        self._media_content_type = None
        self._size = None
        self._name = None
        self._is_inline = None
        self._content_id = None
        self._content = None
        self._on_disk = False
        self._on_cloud = False
        self._id = None
        self._file_path = None

        if attachment:
            if isinstance(attachment, dict):
                # Attachment exists in cloud, set attributes to values from dict
                if "id" in attachment:
                    self._id = attachment.get("id")
                    self._attachment_type = (
                        "item"
                        if "item" in attachment.get("@odata.type", "").lower()
                        else "file"
                    )
                    self._media_content_type = attachment.get(
                        "@odata.mediaContentType", None
                    )
                    self._size = attachment.get("size", None)
                    self._name = attachment.get("name", None)
                    self._is_inline = attachment.get("isInline", False)
                    self._content_id = attachment.get("contentId", None)
                    self._content = attachment.get("contentBytes", None)
                    self._on_disk = False
                    self._on_cloud = True
                else:
                    file_path = attachment.get("path", attachment.get("name"))

                    if file_path is None:
                        raise ValueError("Must provide path or name for attachment.")
                    self._content = attachment.get("content", None)
                    self._on_disk = attachment.get("on_disk", True)
                    self._id = attachment.get("id", None)
                    self._file_path = file_path if self._on_disk else None
                    self._name = attachment.get("name") if self._on_disk else None

            elif isinstance(attachment, str):
                self._file_path = attachment
                self._name = os.path.basename(attachment)

            elif isinstance(attachment, tuple):
                ## Tuples must be path, then name
                self._file_path = attachment[0]
                self._name = attachment[1]

            if self._content is None and self._file_path is not None:
                with open(self._file_path, "rb") as f:
                    self._content = f.read()
                    # self._content = base64.b64encode(f.read()).decode("utf-8")
                    self._size = len(self._content)
                    self._on_disk = True

    def save_local(self, path: str):
        if not self._content:
            return False

        if not self._id:
            return False

        with open(path, "wb") as f:
            f.write(base64.b64decode(self._content))

    def upload(self):
        if self._size < UPLOAD_SESSION_BYTES_THRESHOLD:
            url = build_url(
                user=self.parent.user,
                endpoint=self._endpoints.get("attach").format(id=self.parent._id),
            )


##If existing message, use parent ID to get list of attachments
##Initialize each individual Attachment based on response?
##If not existing message
##Initialize each individual Attachment based on parameters?


class Attachments:
    _endpoints = {
        "attachments": "/messages/{id}/attachments",
        "attachment": "/messages/{id}/attachments/{ida}",
    }

    def __init__(self, parent, attachments: Union[list, str] = None):
        self.parent = parent
        self.__attachments = attachments

        if attachments:
            self.add(attachments)

    def add(self, attachments: Union[list, str]):
        if isinstance(attachments, str):
            attachments = [attachments]

        ##If parent exists, attach to message

        ##If parent does not exist, create normal attachment?

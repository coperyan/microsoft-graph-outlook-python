import json
import requests
from azure.identity import ClientSecretCredential


class GraphClient:
    DefaultScope = "https://graph.microsoft.com/.default"
    BaseUrl = "https://graph.microsoft.com/v1.0"

    def __init__(self, tenant_id: str, client_id: str, client_secret: str):
        self._tenant_id = tenant_id
        self._client_id = client_id
        self._client_secret = client_secret
        self._credentials = None
        self._session = None
        self._create_credentials()

    def _create_credentials(self):
        self._credentials = ClientSecretCredential(
            tenant_id=self._tenant_id,
            client_id=self._client_id,
            client_secret=self._client_secret,
        )

    def _create_session(self, scope=DefaultScope):
        self._create_credentials()
        self._session = requests.Session()
        self._session.headers.update(
            {"Authorization": f"Bearer {self._credentials.get_token(scope).token}"}
        )

    def request(self, method: str, url: str, data: dict = None, **kwargs):
        return self._session.request(
            method,
            url=url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(data),
        )

    def post(self, url: str, data: dict = None, **kwargs):
        if not self._session:
            self._create_session()
        print(url)
        print(data)
        resp = self.request(method="post", url=url, data=data, **kwargs)
        print(resp.json())
        return resp

    def patch(self, url: str, data: dict = None, **kwargs):
        if not self._session:
            self._create_session()
        print(url)
        print(data)
        resp = self.request(method="patch", url=url, data=data, **kwargs)
        print(resp.json())
        return resp

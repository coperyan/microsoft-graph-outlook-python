import os

_BASE_URL = "https://graph.microsoft.com/v1.0"


def build_url(user: str, endpoint: str) -> str:
    return (
        (_BASE_URL + "/users/" + user + endpoint)
        if user
        else (_BASE_URL + "/me" + endpoint)
    )

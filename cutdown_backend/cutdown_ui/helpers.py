import json
from cgitb import reset
from email import message

import requests
from rest_framework import status


def get_shorten_url(url: str) -> str:
    response = requests.post(
        url=f"http://127.0.0.1:8000/shorten_url",
        headers={"Content-Type": "application/json; charset=utf-8"},
        data=json.dumps({"origin_url": url}),
    )

    if response.status_code == status.HTTP_201_CREATED:
        data = response.json()

    elif response.status_code == status.HTTP_403_FORBIDDEN:

        data = {
            "message": "Please come back in few minutes. Many shorten URLs has been created"
        }

    else:
        data = {
            "message": "We regert that we are facing some techincal issue on our server &#128532;. Sorry for the inconvenience caused"
        }

    return data

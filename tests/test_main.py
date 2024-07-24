from typing import Literal

from fastapi.testclient import TestClient

from app.main import app
from app.schemas import SCOPES, UserBase


client = TestClient(app)


def test_create_user():
    response = client.post(
        "/users/",
        headers={"Content-Type": "application/json", "accept": "application/json"},
        json={
            "email": "vbastianpalavecino@gmail.com",
            "username": "vbastianpc",
            "password": "r1qpa9E#",
        },
    )
    assert response.status_code in [201, 400]


def get_token(username: str, password: str, scopes: list[str]):
    response = client.post(
        "/token",
        data={"username": username, "password": password, "scope": " ".join(scopes)},
        headers={
            "accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        print(response.json())
        raise Exception(f"response returns status code {response.status_code}")


token = get_token("vbastianpc", "r1qpa9E#", scopes=[SCOPES.ME, SCOPES.ADMIN])
header_token = {"Authorization": f"Bearer {token}"}
header_json = {"Content-Type": "application/json", "accept": "application/json"}


def test_read_users_me():
    response = client.get("/users/me/", headers=header_token)
    assert response.status_code == 200


def test_update_user():
    response = client.put(
        "/users/me",
        headers=header_token | header_json,
        json=UserBase(email="baztyan@gmail.com", username="vbastianpc").model_dump(),
    )
    assert response.status_code == 200

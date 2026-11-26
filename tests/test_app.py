import pytest

from fastapi.testclient import TestClient

from app import app


client = TestClient(app)


def test_root():

    response = client.get("/")

    assert response.status_code == 200

    assert response.json() == {
        "service": "jenkins-fastapi-demo",
        "version": "1.0.1",
    }


def test_health():

    response = client.get("/health")

    assert response.status_code == 200

    assert response.json() == {
        "status": "ok",
    }


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (3, 5, 8),
        (-2, 7, 5),
        (0, 0, 0),
    ],
)
def test_add(a, b, expected):

    response = client.get(
        "/api/v1/add",
        params={
            "a": a,
            "b": b,
        },
    )

    assert response.status_code == 200

    assert response.json() == {
        "a": a,
        "b": b,
        "result": expected,
    }


def test_add_invalid_input():

    response = client.get(
        "/api/v1/add",
        params={
            "a": "abc",
            "b": 5,
        },
    )

    assert response.status_code == 422

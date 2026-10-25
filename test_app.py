import os
import pytest
from app import app, PRICES


@pytest.fixture
def client():
    return app.test_client()


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_json()["status"] == "ok"


def test_price_known_item(client):
    r = client.get("/price/laptop")
    assert r.get_json()["price"] == PRICES["laptop"]


def test_price_unknown_item(client):
    assert client.get("/price/unicorn").status_code == 404


@pytest.mark.skipif(not os.getenv("REDIS_HOST"), reason="needs a Redis service")
def test_visit_counter_with_redis(client):
    first = client.get("/visit").get_json()["visits"]
    second = client.get("/visit").get_json()["visits"]
    assert second == first + 1

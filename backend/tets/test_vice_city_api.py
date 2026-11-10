"""Regression tests for the Vice City dossier content API."""
import os

import pytest
import requests


BASE_URL = os.environ.get("REACT_APP_BACKEND_URL")
if not BASE_URL:
    pytest.skip("REACT_APP_BACKEND_URL is not configured", allow_module_level=True)
BASE_URL = BASE_URL.rstrip("/")


@pytest.fixture(scope="module")
def api_client():
    return requests.Session()


def test_api_root(api_client):
    response = api_client.get(f"{BASE_URL}/api/", timeout=15)
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "online"


def test_story_has_editorial_chapters(api_client):
    response = api_client.get(f"{BASE_URL}/api/story", timeout=15)
    assert response.status_code == 200
    body = response.json()
    assert body["title"]
    assert len(body["chapters"]) >= 3
    assert any(chapter["tag"] == "TEORIA" for chapter in body["chapters"])


def test_characters_include_lucia_and_jason(api_client):
    response = api_client.get(f"{BASE_URL}/api/characters", timeout=15)
    assert response.status_code == 200
    names = {item["name"] for item in response.json()["items"]}
    assert {"Lucia", "Jason"}.issubset(names)


@pytest.mark.parametrize("category, expected", [("CIDADE", "CIDADE"), ("PISTA", "PISTA"), ("TEORIA", "TEORIA")])
def test_easter_egg_category_filter(api_client, category, expected):
    response = api_client.get(f"{BASE_URL}/api/easter-eggs", params={"category": category}, timeout=15)
    assert response.status_code == 200
    items = response.json()["items"]
    assert items and all(item["category"] == expected for item in items)


def test_trailers_have_sequential_content(api_client):
    response = api_client.get(f"{BASE_URL}/api/trailers", timeout=15)
    assert response.status_code == 200
    items = response.json()["items"]
    assert len(items) >= 2
    assert all(item["image"] and item["title"] for item in items)
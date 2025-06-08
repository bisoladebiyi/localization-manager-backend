import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from src.localization_management_api.main import app

client = TestClient(app)

@pytest.fixture
def mock_supabase_table():
    with patch("src.localization_management_api.main.supabase") as mock_client:
        yield mock_client.table.return_value


# TESTS FOR EACH ENDPOINT 
def test_get_localizations(mock_supabase_table):
    mock_supabase_table.select.return_value.execute.return_value.data = [{"id": "4f5953ca-3b1a-4ca9-bbdb-e71d8ffeedcc", "key": "_welcome_"}]
    
    response = client.get("/api/localizations")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json()[0]["key"] == "_welcome_"

def test_get_localization(mock_supabase_table):
    mock_supabase_table.select.return_value.eq.return_value.single.return_value.execute.return_value.data = {"id": "4f5953ca-3b1a-4ca9-bbdb-e71d8ffeedcc", "key": "_thanks_"}

    response = client.get("/api/localizations/4f5953ca-3b1a-4ca9-bbdb-e71d8ffeedcc")

    assert response.status_code == 200
    assert response.json()["key"] == "_thanks_"

def test_create_localization(mock_supabase_table):
    mock_supabase_table.insert.return_value.execute.return_value.data = {"key": "greeting"}

    payload = {
        "key": "_greeting_",
        "category": None,
        "description": None,
        "translations": {
            "en": {
                "value": "Hello",
                "updatedAt": "2025-06-08T15:42:10",
                "updatedBy": "abby@mail.com"
            }
        }
    }

    response = client.post("/api/localizations", json=payload)

    assert response.status_code == 200
    assert response.json()["message"] == "Localization created successfully"

def test_update_localization(mock_supabase_table):
    mock_supabase_table.update.return_value.eq.return_value.execute.return_value.data = {"key": "greeting"}

    payload = {
        "id": "8288269e-da25-4c3c-939e-8b8ee0c9efbe",
        "key": "greeting",
        "category": "",
        "description": "",
        "translations": {
            "en": {
                "value": "Hey",
                "updatedAt": "2025-06-08T15:42:10",
                "updatedBy": "abby@mail.com"
            }
        }
    }

    response = client.put("/api/localizations/8288269e-da25-4c3c-939e-8b8ee0c9efbe", json=payload)

    assert response.status_code == 200
    assert response.json()["message"] == "Localization updated successfully"

def test_delete_localization(mock_supabase_table):
    mock_supabase_table.delete.return_value.eq.return_value.execute.return_value.data = {"id": "abcd"}

    response = client.delete("/api/localizations/abcd")

    assert response.status_code == 200
    assert response.json()["message"] == "Localization deleted successfully"

def test_bulk_update_localizations():
    payload = [
        {
            "id": "8288269e-da25-4c3c-939e-8b8ee0c9efbe",
            "key": "_greeting_",
            "category": "",
            "description": "",
            "translations": {
                "en": {"value": "Hello"},
                "fr": {"value": "Bonjour"}
            }
        },
        {
            "id": "4f5953ca-3b1a-4ca9-bbdb-e71d8ffeedcc",
            "key": "_bye_",
            "category": "",
            "description": "",
            "translations": {
                "en": {"value": "Goodbye"},
                "fr": {"value": "Au revoir"}
            }
        }
    ]

    response = client.post("/api/localizations/bulk-update", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "updateCount" in data
    assert "failedUpdatesId" in data
    assert isinstance(data["updateCount"], int)
    assert isinstance(data["failedUpdatesId"], list)
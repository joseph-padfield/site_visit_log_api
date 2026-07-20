from fastapi.testclient import TestClient

def test_create_site(client: TestClient):
    response = client.post(
        "/sites/",
        json={
            "name": "St Anne's Church",
            "address": "1 High Street, London",
            "site_type": "listed building",
            "notes": "Victorian parish church."
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 1
    assert data["name"] == "St Anne's Church"
    assert data["address"] == "1 High Street, London"
    assert data["site_type"] == "listed building"
    assert data["notes"] == "Victorian parish church."
    assert "created_at" in data

def test_unknown_site_returns_404(
        client: TestClient
        ):
    response = client.get("/sites/9999")

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Site not found."
    }
    
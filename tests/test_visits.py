from fastapi.testclient import TestClient

def create_test_site(client: TestClient) -> int:
    response = client.post(
        "/sites/",
        json={
            "name": "Riverside Mill",
            "address": "Mill Lane, York",
            "site_type": "industrial building",
            "notes": None,
        }
    )

    assert response.status_code == 201

    return response.json()["id"]

def test_create_visit_for_site(
        client: TestClient
):
    site_id = create_test_site(client)

    response = client.post(
        f"/sites/{site_id}/visits/",
        json={
            "visit_date": "2026-07-10",
            "purpose": "Condition inspection",
            "weather": "Dry",
            "notes": "Masonry generally sound.",
            "follow_up_required": False,
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 1
    assert data["site_id"] == site_id
    assert data["purpose"] == "Condition inspection"
    assert data["follow_up_required"] is False

def test_create_visit_for_unknown_site_returns_404(
        client: TestClient
):
    response = client.post(
        "/sites/9999/visits/",
        json={
            "visit_date": "2026-07-10",
            "purpose": "Condition inspection",
            "weather": None,
            "notes": None,
            "follow_up_required": False,
        }
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Site not found."
    }

def test_filter_visits_since_date(
    client: TestClient,
):
    site_id = create_test_site(client)

    visits = [
        {
            "visit_date": "2025-12-15",
            "purpose": "Winter inspection",
            "weather": "Cold",
            "notes": None,
            "follow_up_required": False,
        },
        {
            "visit_date": "2026-02-10",
            "purpose": "Roof inspection",
            "weather": "Dry",
            "notes": None,
            "follow_up_required": True,
        },
        {
            "visit_date": "2026-07-01",
            "purpose": "Summer inspection",
            "weather": "Sunny",
            "notes": None,
            "follow_up_required": False,
        },
    ]

    for visit in visits:
        response = client.post(
            f"/sites/{site_id}/visits/",
            json=visit,
        )

        assert response.status_code == 201

    response = client.get(
        "/visits/",
        params={
            "since": "2026-01-01",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2

    assert data[0]["visit_date"] == "2026-07-01"
    assert data[1]["visit_date"] == "2026-02-10"
    
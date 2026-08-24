from urllib.parse import quote


def test_root_redirects_to_static_index(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_activity_details(client):
    response = client.get("/activities")

    assert response.status_code == 200
    activities = response.json()
    assert "Chess Club" in activities
    assert activities["Chess Club"]["description"]
    assert activities["Chess Club"]["schedule"]
    assert activities["Chess Club"]["max_participants"] == 12
    assert activities["Chess Club"]["participants"] == [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]


def test_activity_name_with_spaces_is_url_encoded(client):
    response = client.post(
        f"/activities/{quote('Chess Club', safe='')}/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 200

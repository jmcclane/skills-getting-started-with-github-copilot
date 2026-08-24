def test_signup_adds_student_to_activity(client):
    response = client.post(
        "/activities/Soccer Team/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Signed up student@mergington.edu for Soccer Team"
    }
    activities = client.get("/activities").json()
    assert "student@mergington.edu" in activities["Soccer Team"]["participants"]


def test_duplicate_signup_returns_bad_request_without_duplicate(client):
    email = "michael@mergington.edu"

    response = client.post("/activities/Chess Club/signup", params={"email": email})

    assert response.status_code == 400
    participants = client.get("/activities").json()["Chess Club"]["participants"]
    assert participants.count(email) == 1


def test_signup_for_unknown_activity_returns_not_found(client):
    response = client.post(
        "/activities/Unknown Club/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_without_email_returns_unprocessable_entity(client):
    response = client.post("/activities/Soccer Team/signup")

    assert response.status_code == 422

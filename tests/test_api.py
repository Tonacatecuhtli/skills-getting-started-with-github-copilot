from src.app import activities


def test_root_redirects_to_index(client):
    # Arrange: client fixture
    # Act
    resp = client.get("/", follow_redirects=False)

    # Assert
    assert resp.status_code in (302, 307)
    assert resp.headers.get("location", "").endswith("/static/index.html")


def test_get_activities_returns_all(client):
    # Arrange
    # Act
    resp = client.get("/activities")

    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_happy_path_returns_200_and_message(client):
    # Arrange
    activity = "Swimming Club"
    email = "tester1@mergington.edu"
    assert email not in activities[activity]["participants"]

    # Act
    resp = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert resp.status_code == 200
    assert email in activities[activity]["participants"]
    assert email in resp.json().get("message", "")


def test_signup_nonexistent_activity_returns_404(client):
    # Arrange
    activity = "NoSuchActivity"
    email = "noone@nowhere.test"

    # Act
    resp = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert resp.status_code == 404


def test_signup_already_signed_up_returns_400(client):
    # Arrange
    activity = "Chess Club"
    existing = activities[activity]["participants"][0]

    # Act
    resp = client.post(f"/activities/{activity}/signup?email={existing}")

    # Assert
    assert resp.status_code == 400


def test_remove_participant_happy_path(client):
    # Arrange
    activity = "Chess Club"
    existing = activities[activity]["participants"][0]
    assert existing in activities[activity]["participants"]

    # Act
    resp = client.delete(f"/activities/{activity}/participants?email={existing}")

    # Assert
    assert resp.status_code == 200
    assert existing not in activities[activity]["participants"]


def test_remove_nonexistent_participant_returns_404(client):
    # Arrange
    activity = "Swimming Club"
    email = "not-registered@mergington.edu"

    # Act
    resp = client.delete(f"/activities/{activity}/participants?email={email}")

    # Assert
    assert resp.status_code == 404


def test_activity_max_participants_edge_case(client):
    # Arrange: set an activity to full capacity
    activity = "Swimming Club"
    max_p = activities[activity]["max_participants"]
    # fill participants to max
    activities[activity]["participants"] = [f"p{i}@m.test" for i in range(max_p)]
    new_email = "extra@mergington.edu"

    # Act: current implementation does not enforce max; we assert current behavior
    resp = client.post(f"/activities/{activity}/signup?email={new_email}")

    # Assert: signup succeeds (matches current app behavior)
    assert resp.status_code == 200
    assert new_email in activities[activity]["participants"]

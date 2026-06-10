from urllib.parse import quote

import src.app as app_module


# ---------------------------------------------------------------------------
# Signup tests
# ---------------------------------------------------------------------------


def test_signup_success(client):
    # Arrange
    activity = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{quote(activity)}/signup?email={quote(email)}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity}"


def test_signup_adds_participant_to_activity(client):
    # Arrange
    activity = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    client.post(f"/activities/{quote(activity)}/signup?email={quote(email)}")

    # Assert
    assert email in app_module.activities[activity]["participants"]


def test_signup_unknown_activity_returns_404(client):
    # Arrange
    activity = "Underwater Basket Weaving"
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{quote(activity)}/signup?email={quote(email)}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_duplicate_email_returns_400(client):
    # Arrange: michael is already in Chess Club in the baseline state
    activity = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{quote(activity)}/signup?email={quote(email)}")

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already signed up for this activity"


def test_signup_full_activity_returns_400(client):
    # Arrange: fill Chess Club up to max_participants
    activity = "Chess Club"
    max_p = app_module.activities[activity]["max_participants"]
    existing = len(app_module.activities[activity]["participants"])
    for i in range(max_p - existing):
        app_module.activities[activity]["participants"].append(f"filler{i}@mergington.edu")

    # Act
    response = client.post(
        f"/activities/{quote(activity)}/signup?email={quote('overflow@mergington.edu')}"
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Activity is full"


# ---------------------------------------------------------------------------
# Unregister tests
# ---------------------------------------------------------------------------


def test_unregister_success(client):
    # Arrange: michael is in Chess Club in the baseline state
    activity = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(f"/activities/{quote(activity)}/unregister?email={quote(email)}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity}"


def test_unregister_removes_participant_from_activity(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    client.delete(f"/activities/{quote(activity)}/unregister?email={quote(email)}")

    # Assert
    assert email not in app_module.activities[activity]["participants"]


def test_unregister_unknown_activity_returns_404(client):
    # Arrange
    activity = "Underwater Basket Weaving"
    email = "student@mergington.edu"

    # Act
    response = client.delete(f"/activities/{quote(activity)}/unregister?email={quote(email)}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_email_not_registered_returns_404(client):
    # Arrange
    activity = "Chess Club"
    email = "notregistered@mergington.edu"

    # Act
    response = client.delete(f"/activities/{quote(activity)}/unregister?email={quote(email)}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Email not signed up for this activity"

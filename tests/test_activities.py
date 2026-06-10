def test_get_activities_returns_200(client):
    # Arrange: baseline activities are pre-loaded by the reset_activities fixture

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200


def test_get_activities_returns_all_expected_activities(client):
    # Arrange
    expected_activities = [
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Basketball Team",
        "Soccer Club",
        "Art Studio",
        "Drama Club",
        "Music Ensemble",
        "Debate Team",
    ]

    # Act
    response = client.get("/activities")

    # Assert
    data = response.json()
    for name in expected_activities:
        assert name in data


def test_get_activities_each_entry_has_required_fields(client):
    # Arrange: pick a known activity to verify shape
    target = "Chess Club"

    # Act
    response = client.get("/activities")

    # Assert
    activity = response.json()[target]
    assert "description" in activity
    assert "schedule" in activity
    assert "max_participants" in activity
    assert "participants" in activity
    assert isinstance(activity["participants"], list)


def test_get_activities_no_store_cache_header(client):
    # Arrange: no additional setup

    # Act
    response = client.get("/activities")

    # Assert
    cache_control = response.headers.get("cache-control", "")
    assert "no-store" in cache_control


def test_get_activities_pragma_no_cache_header(client):
    # Arrange: no additional setup

    # Act
    response = client.get("/activities")

    # Assert
    assert response.headers.get("pragma") == "no-cache"

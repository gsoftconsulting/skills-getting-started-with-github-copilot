from urllib.parse import quote


def test_root_redirects_to_static_index(client):
    # Arrange: no additional setup — the redirect target is fixed by the app

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code in (301, 302, 307, 308)
    assert response.headers["location"] == "/static/index.html"

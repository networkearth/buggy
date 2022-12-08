"""
Tests for the / endpoint
"""

def test_view(client):
    """
    Tests that the / endpoint exists
    """
    response = client.get('/')
    assert response.status_code == 200

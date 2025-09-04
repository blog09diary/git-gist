# Import required modules for testing
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
import httpx
import sys
import os

# Add the parent directory to the system path to import 'main'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import app

# Create a test client using the FastAPI app
client = TestClient(app)

# Test fetching public gists for the user 'octocat'
def test_get_gists_octocat():
    mock_gists = [
        {"id": "1", "description": "Test Gist", "html_url": "https://gist.github.com/octocat/1"}
    ]
    with patch("httpx.AsyncClient.get") as mock_get:
        mock_response = httpx.Response(
            status_code=200,
            json=mock_gists
        )
        mock_get.return_value = mock_response
        response = client.get("/octocat")
        # Ensure the response is successful
        assert response.status_code == 200
        # The response should be a list
        assert isinstance(response.json(), list)
        # If there are gists, check for required fields
        if response.json():
            gist = response.json()[0]
            assert "id" in gist
            assert "url" in gist

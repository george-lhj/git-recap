import os
import fetch
import pytest
from unittest.mock import patch, MagicMock, ANY

from unittest.mock import patch, MagicMock

# ======================
# 1. Test fetch_commits()
# ======================
@patch("fetch.authenticate")  # Mock the authenticate function
@patch("fetch.requests.get")
def test_fetch_commits_success(mock_get, mock_authenticate):
    """Test fetch_commits with a successful API response."""
    mock_authenticate.return_value = {"Authorization": "token mock_token_for_testing"}  # Mocked headers
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {
            "sha": "abc123",
            "commit": {
                "message": "Test commit message",
                "author": {"date": "2025-03-01T12:00:00Z"}
            }
        }
    ]
    mock_get.return_value = mock_response

    commits = fetch.fetch_commits("test_owner", "test_repo", "2025-03-01", "2025-03-10")
    assert len(commits) == 1
    assert commits[0]["sha"] == "abc123"


@patch("fetch.authenticate")  # Mock the authenticate function
@patch("fetch.requests.get")
def test_fetch_commits_failure(mock_get, mock_authenticate):
    """Test fetch_commits handling of API failure."""
    mock_authenticate.return_value = {"Authorization": "token mock_token_for_testing"}  # Mocked headers
    mock_response = MagicMock()
    mock_response.status_code = 403
    mock_response.text = "Forbidden"
    mock_get.return_value = mock_response

    commits = fetch.fetch_commits("test_owner", "test_repo", "2025-03-01", "2025-03-10")
    assert commits == []  # Should return an empty list on failure


# ======================
# 2. Test fetch_pull_requests()
# ======================
@patch("fetch.authenticate")  # Mock the authenticate function
@patch("fetch.requests.get")
def test_fetch_pull_requests_success(mock_get, mock_authenticate):
    """Test fetch_pull_requests with a successful API response."""
    mock_authenticate.return_value = {"Authorization": "token mock_token_for_testing"}  # Mocked headers
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {
            "number": 1,
            "created_at": "2025-03-02T12:00:00Z",
            "user": {"login": "test_user"},
            "title": "Test PR",
            "state": "open",
            "body": "PR description",
            "labels": [],
            "assignees": []
        }
    ]
    mock_get.return_value = mock_response

    prs = fetch.fetch_pull_requests("test_owner", "test_repo", "test_user", "2025-03-01", "2025-03-10")
    assert len(prs) == 1
    assert prs[0]["number"] == 1


@patch("fetch.authenticate")  # Mock the authenticate function
@patch("fetch.requests.get")
def test_fetch_pull_requests_failure(mock_get, mock_authenticate):
    """Test fetch_pull_requests handling of API failure."""
    mock_authenticate.return_value = {"Authorization": "token mock_token_for_testing"}  # Mocked headers
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.text = "Internal Server Error"
    mock_get.return_value = mock_response

    prs = fetch.fetch_pull_requests("test_owner", "test_repo", "test_user", "2025-03-01", "2025-03-10")
    assert prs == []  # Should return an empty list on failure


@patch("fetch.authenticate")  # Mock the authenticate function
@patch("fetch.requests.get")
def test_fetch_reviews_by_user_failure(mock_get, mock_authenticate):
    """Test fetch_reviews_by_user handling of API failure."""
    mock_authenticate.return_value = {"Authorization": "token mock_token_for_testing"}  # Mocked headers
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.text = "Not Found"
    mock_get.return_value = mock_response

    reviews = fetch.fetch_reviews_by_user("test_owner", "test_repo", 1, "test_user")
    assert reviews == []  # Should return an empty list on failure


# ======================
# 4. Test fetch_issues()
# ======================
@patch("fetch.authenticate")  # Mock the authenticate function
@patch("fetch.requests.get")
def test_fetch_issues_success(mock_get, mock_authenticate):
    """Test fetch_issues with a successful API response."""
    mock_authenticate.return_value = {"Authorization": "token mock_token_for_testing"}  # Mocked headers
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {
            "title": "Test Issue",
            "created_at": "2025-03-02T12:00:00Z",
            "user": {"login": "test_user"},
            "body": "Issue description",
            "labels": [],
            "assignees": []
        }
    ]
    mock_get.return_value = mock_response

    issues = fetch.fetch_issues("test_owner", "test_repo", "test_user", "2025-03-01", "2025-03-10")
    assert len(issues) == 1
    assert issues[0]["title"] == "Test Issue"


@patch("fetch.authenticate")  # Mock the authenticate function
@patch("fetch.requests.get")
def test_fetch_issues_failure(mock_get, mock_authenticate):
    """Test fetch_issues handling of API failure."""
    mock_authenticate.return_value = {"Authorization": "token mock_token_for_testing"}  # Mocked headers
    mock_response = MagicMock()
    mock_response.status_code = 403
    mock_response.text = "Forbidden"
    mock_get.return_value = mock_response

    issues = fetch.fetch_issues("test_owner", "test_repo", "test_user", "2025-03-01", "2025-03-10")
    assert issues == []  # Should return an empty list on failure
import os
import fetch
import pytest
from unittest.mock import patch, MagicMock, ANY

# ======================
# 1. Test get_time_range()
# ======================
def test_get_time_range_default():
    """Test default time range calculation (last Sunday to next Sunday)."""
    start_date, end_date = fetch.get_time_range()
    assert start_date < end_date  # Ensure start is before end
    assert len(start_date) == 10 and len(end_date) == 10  # Ensure YYYY-MM-DD format


def test_get_time_range_custom():
    """Test get_time_range with custom start and end dates."""
    start_date, end_date = fetch.get_time_range("2025-03-01", "2025-03-10")
    assert start_date == "2025-03-01"
    assert end_date == "2025-03-10"


# ======================
# 2. Test authenticate()
# ======================
@patch.dict(os.environ, {"GITHUB_TOKEN": "test_token"})
def test_authenticate():
    """Test if authenticate() correctly loads the GitHub token."""
    headers = fetch.authenticate()
    assert headers["Authorization"] == "token test_token"


@patch.dict(os.environ, {}, clear=True)  # Clear environment variables
def test_authenticate_missing_token():
    """Test if authenticate() raises an error when GITHUB_TOKEN is missing."""
    with pytest.raises(ValueError, match="GitHub token not found"):
        fetch.authenticate()


# ======================
# 3. Test fetch_commits()
# ======================
@patch("fetch.requests.get")
def test_fetch_commits_success(mock_get):
    """Test fetch_commits with a successful API response."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"sha": "abc123", "commit": {"message": "Test commit"}}]
    mock_get.return_value = mock_response

    commits = fetch.fetch_commits("test_owner", "test_repo", "2025-03-01", "2025-03-10")
    assert len(commits) == 1
    assert commits[0]["sha"] == "abc123"


@patch("fetch.requests.get")
def test_fetch_commits_failure(mock_get):
    """Test fetch_commits handling of API failure."""
    mock_response = MagicMock()
    mock_response.status_code = 403
    mock_response.text = "Forbidden"
    mock_get.return_value = mock_response

    commits = fetch.fetch_commits("test_owner", "test_repo", "2025-03-01", "2025-03-10")
    assert commits == []  # Should return an empty list on failure


# ======================
# 4. Test fetch_pull_requests()
# ======================
@patch("fetch.requests.get")
def test_fetch_pull_requests_success(mock_get):
    """Test fetch_pull_requests with a successful API response."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {"number": 1, "created_at": "2025-03-02T12:00:00Z", "user": {"login": "test_user"}}
    ]
    mock_get.return_value = mock_response

    prs = fetch.fetch_pull_requests("test_owner", "test_repo", "test_user", "2025-03-01", "2025-03-10")
    assert len(prs) == 1
    assert prs[0]["number"] == 1


@patch("fetch.requests.get")
def test_fetch_pull_requests_failure(mock_get):
    """Test fetch_pull_requests handling of API failure."""
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.text = "Internal Server Error"
    mock_get.return_value = mock_response

    prs = fetch.fetch_pull_requests("test_owner", "test_repo", "test_user", "2025-03-01", "2025-03-10")
    assert prs == []  # Should return an empty list on failure


# ======================
# 5. Test fetch_reviews_by_user()
# ======================
@patch("fetch.requests.get")
def test_fetch_reviews_by_user_success(mock_get):
    """Test fetch_reviews_by_user with a successful API response."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {"id": 123, "state": "APPROVED", "user": {"login": "test_user"}}
    ]
    mock_get.return_value = mock_response

    reviews = fetch.fetch_reviews_by_user("test_owner", "test_repo", 1, "test_user")
    assert len(reviews) == 1
    assert reviews[0]["state"] == "APPROVED"


@patch("fetch.requests.get")
def test_fetch_reviews_by_user_failure(mock_get):
    """Test fetch_reviews_by_user handling of API failure."""
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.text = "Not Found"
    mock_get.return_value = mock_response

    reviews = fetch.fetch_reviews_by_user("test_owner", "test_repo", 1, "test_user")
    assert reviews == []  # Should return an empty list on failure


# ======================
# 6. Test fetch_issues()
# ======================
@patch("fetch.requests.get")
def test_fetch_issues_success(mock_get):
    """Test fetch_issues with a successful API response."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {"title": "Test Issue", "created_at": "2025-03-02T12:00:00Z", "user": {"login": "test_user"}}
    ]
    mock_get.return_value = mock_response

    issues = fetch.fetch_issues("test_owner", "test_repo", "test_user", "2025-03-01", "2025-03-10")
    assert len(issues) == 1
    assert issues[0]["title"] == "Test Issue"


@patch("fetch.requests.get")
def test_fetch_issues_failure(mock_get):
    """Test fetch_issues handling of API failure."""
    mock_response = MagicMock()
    mock_response.status_code = 403
    mock_response.text = "Forbidden"
    mock_get.return_value = mock_response

    issues = fetch.fetch_issues("test_owner", "test_repo", "test_user", "2025-03-01", "2025-03-10")
    assert issues == []  # Should return an empty list on failure


# ======================
# 7. Test fetch_github_activity()
# ======================
@patch("fetch.fetch_commits")
@patch("fetch.fetch_pull_requests")
@patch("fetch.fetch_reviews_by_user")
@patch("fetch.fetch_issues")
def test_fetch_github_activity(
    mock_issues, mock_reviews, mock_prs, mock_commits
):
    """
    Test fetch_github_activity with minimal mocked data.
    Verify that the function integrates correctly with its dependencies.
    """
    # Mocked commits (minimal structure)
    mock_commits.return_value = [
        {"sha": "abc123", "commit": {"message": "Test commit", "author": {"date": "2025-03-01T12:00:00Z"}}}
    ]

    # Mocked pull requests (minimal structure)
    mock_prs.return_value = [
        {
            "title": "Test PR",
            "state": "open",
            "created_at": "2025-03-02T10:00:00Z",
            "body": "PR description",
            "labels": [],
            "assignees": [],
            "number": 1  # Ensure 'number' is present
        }
    ]

    # Mocked reviews (minimal structure)
    mock_reviews.return_value = [
        {"id": 123, "state": "APPROVED", "body": "Great work!"}
    ]

    # Mocked issues (minimal structure)
    mock_issues.return_value = [
        {
            "title": "Test Issue",
            "state": "open",
            "created_at": "2025-03-03T10:00:00Z",
            "body": "Issue description",
            "labels": [],
            "assignees": []
        }
    ]

    # Call the function under test
    data = fetch.fetch_github_activity("test_owner", "test_repo", "test_user")

    # Assertions
    assert "commits" in data
    assert "pull_requests" in data
    assert "reviews" in data
    assert "issues" in data

    # Verify the number of items returned
    assert len(data["commits"]) == 1
    assert len(data["pull_requests"]) == 1
    assert len(data["reviews"][1]) == 1
    assert len(data["issues"]) == 1

    # Verify basic fields in commits
    assert data["commits"][0]["message"] == "Test commit"
    assert data["commits"][0]["date"] == "2025-03-01T12:00:00Z"

    # Verify basic fields in pull requests
    assert data["pull_requests"][0]["title"] == "Test PR"
    assert data["pull_requests"][0]["state"] == "open"

    # Verify basic fields in reviews
    assert data["reviews"][1][0]["state"] == "APPROVED"
    assert data["reviews"][1][0]["body"] == "Great work!"

    # Verify basic fields in issues
    assert data["issues"][0]["title"] == "Test Issue"
    assert data["issues"][0]["state"] == "open"

    # Verify calls to mocked functions
    mock_commits.assert_called_once_with("test_owner", "test_repo", ANY, ANY)
    mock_prs.assert_called_once_with("test_owner", "test_repo", "test_user", ANY, ANY)
    mock_reviews.assert_called_once_with("test_owner", "test_repo", 1, "test_user")
    mock_issues.assert_called_once_with("test_owner", "test_repo", "test_user", ANY, ANY)
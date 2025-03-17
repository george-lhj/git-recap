import os
import fetch
import pytest
from unittest.mock import patch

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
def test_fetch_commits(mock_get):
    """Test fetch_commits with a mocked GitHub API response."""
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [{"sha": "abc123", "commit": {"message": "Test commit"}}]

    commits = fetch.fetch_commits("test_owner", "test_repo", "2025-03-01", "2025-03-10")
    assert len(commits) == 1
    assert commits[0]["sha"] == "abc123"

@patch("fetch.requests.get")
def test_fetch_commits_failure(mock_get):
    """Test fetch_commits handling of API failure."""
    mock_get.return_value.status_code = 403  # Simulating API rate limit error
    mock_get.return_value.text = "Forbidden"

    commits = fetch.fetch_commits("test_owner", "test_repo", "2025-03-01", "2025-03-10")
    assert commits == []  # Should return an empty list on failure

# ======================
# 4. Test fetch_pull_requests()
# ======================
@patch("fetch.requests.get")
def test_fetch_pull_requests(mock_get):
    """Test fetch_pull_requests with a mocked GitHub API response."""
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [{"number": 1, "created_at": "2025-03-02T12:00:00Z"}]

    prs = fetch.fetch_pull_requests("test_owner", "test_repo", "2025-03-01", "2025-03-10")
    assert len(prs) == 1
    assert prs[0]["number"] == 1

@patch("fetch.requests.get")
def test_fetch_pull_requests_failure(mock_get):
    """Test fetch_pull_requests handling of API failure."""
    mock_get.return_value.status_code = 500  # Simulating server error
    mock_get.return_value.text = "Internal Server Error"

    prs = fetch.fetch_pull_requests("test_owner", "test_repo", "2025-03-01", "2025-03-10")
    assert prs == []  # Should return an empty list on failure

# ======================
# 5. Test fetch_reviews()
# ======================
@patch("fetch.requests.get")
def test_fetch_reviews(mock_get):
    """Test fetch_reviews with a mocked GitHub API response."""
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [{"id": 123, "state": "APPROVED"}]

    reviews = fetch.fetch_reviews("test_owner", "test_repo", 1)
    assert len(reviews) == 1
    assert reviews[0]["state"] == "APPROVED"

@patch("fetch.requests.get")
def test_fetch_reviews_failure(mock_get):
    """Test fetch_reviews handling of API failure."""
    mock_get.return_value.status_code = 404  # Simulating PR not found
    mock_get.return_value.text = "Not Found"

    reviews = fetch.fetch_reviews("test_owner", "test_repo", 1)
    assert reviews == []  # Should return an empty list on failure

# ======================
# 6. Test fetch_github_activity()
# ======================
@patch("fetch.fetch_commits", return_value=[{"sha": "abc123"}])
@patch("fetch.fetch_pull_requests", return_value=[{"number": 1}])
@patch("fetch.fetch_reviews", return_value={1: [{"id": 123, "state": "APPROVED"}]})
def test_fetch_github_activity(mock_commits, mock_prs, mock_reviews):
    """Test fetch_github_activity with mocked functions."""
    data = fetch.fetch_github_activity("test_owner", "test_repo")

    assert "commits" in data
    assert "pull_requests" in data
    assert "reviews" in data

    assert len(data["commits"]) == 1
    assert len(data["pull_requests"]) == 1
    assert len(data["reviews"][1]) == 1

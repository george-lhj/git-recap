import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

GITHUB_API_URL = "https://api.github.com"
load_dotenv()

def authenticate():
    """
    Get GitHub credentials from environment variables.
    Returns:
        headers (dict): Authentication headers for GitHub API requests.
    """
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise ValueError("GitHub token not found. Set GITHUB_TOKEN in your .env file.")
    
    return {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}


def get_time_range(start_date=None, end_date=None):
    """
    Get the time range for retrieving GitHub data.
    Defaults:
        - Start Date: Last Sunday
        - End Date: Next Sunday
    Users can override:
        - Start Date (e.g., a specific past date)
        - End Date (e.g., today's date instead of next Sunday)
    
    Args:
        start_date (str, optional): User-specified start date (YYYY-MM-DD).
        end_date (str, optional): User-specified end date (YYYY-MM-DD).

    Returns:
        tuple: (start_date, end_date) in YYYY-MM-DD format.
    """
    today = datetime.today()

    if not start_date:
        start_date = today - timedelta(days=today.weekday() + 1)
    if not end_date:
        end_date = start_date + timedelta(days=6)

    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
    if isinstance(end_date, str):
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

    return start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")

def fetch_commits(owner, repo, start_date, end_date):
    """
    Fetch commits from a GitHub repository within a specific date range.
    Args:
        owner (str): Repository owner.
        repo (str): Repository name.
        start_date (str): Start date in YYYY-MM-DD format.
        end_date (str): End date in YYYY-MM-DD format.
    Returns:
        list: List of commits.
    """
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/commits"
    params = {"since": f"{start_date}T00:00:00Z", "until": f"{end_date}T23:59:59Z"}
    response = requests.get(url, headers=authenticate(), params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching commits: {response.status_code}, {response.text}")
        return []
    
def fetch_pull_requests(owner, repo, start_date, end_date):
    """
    Fetch pull requests from a GitHub repository within a specific date range.
    Args:
        owner (str): Repository owner.
        repo (str): Repository name.
        start_date (str): Start date in YYYY-MM-DD format.
        end_date (str): End date in YYYY-MM-DD format.
    Returns:
        list: List of pull requests.
    """
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/pulls"
    params = {"state": "all", "sort": "updated", "direction": "desc"}
    response = requests.get(url, headers=authenticate(), params=params)
    if response.status_code == 200:
        prs = response.json()
        return [pr for pr in prs if start_date <= pr["created_at"][:10] <= end_date]
    else:
        print(f"Error fetching PRs: {response.status_code}, {response.text}")
        return []

def fetch_reviews(owner, repo, pr_number):
    """
    Fetch reviews for a given pull request.
    Args:
        owner (str): Repository owner.
        repo (str): Repository name.
        pr_number (int): Pull request number.
    Returns:
        list: List of reviews for the PR.
    """
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/pulls/{pr_number}/reviews"
    response = requests.get(url, headers=authenticate())
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching reviews for PR {pr_number}: {response.status_code}, {response.text}")
        return []
    
def fetch_github_activity(owner, repo, start_date=None, end_date=None):
    """
    Fetch commits, pull requests, and reviews from a GitHub repository in a given time range.
    Args:
        owner (str): Repository owner.
        repo (str): Repository name.
        start_date (str, optional): Custom start date (YYYY-MM-DD).
        end_date (str, optional): Custom end date (YYYY-MM-DD).
    Returns:
        dict: Dictionary containing commits, PRs, and reviews.
    """
    start_date, end_date = get_time_range(start_date, end_date)

    print(f"Fetching GitHub activity from {start_date} to {end_date}...")

    commits = fetch_commits(owner, repo, start_date, end_date)
    prs = fetch_pull_requests(owner, repo, start_date, end_date)

    reviews = {}
    for pr in prs:
        pr_number = pr["number"]
        reviews[pr_number] = fetch_reviews(owner, repo, pr_number)

    return {
        "commits": commits,
        "pull_requests": prs,
        "reviews": reviews
    }

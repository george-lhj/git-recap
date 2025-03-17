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

def fetch_active_repositories(username, months=6):
    """
    Fetch repositories where the user has been active in the past X months.
    Args:
        username (str): GitHub username.
        months (int): Number of months to look back for activity.
    Returns:
        list: List of unique repository names where the user has been active.
    """
    cutoff_date = (datetime.now() - timedelta(days=30 * months)).isoformat()
    events_url = f"{GITHUB_API_URL}/users/{username}/events"
    headers = authenticate()
    response = requests.get(events_url, headers=headers)
    if response.status_code != 200:
        print(f"Error fetching events: {response.status_code}, {response.text}")
        return []
    events = response.json()

    active_repos = set()
    for event in events:
        created_at = event.get("created_at")
        if created_at and created_at >= cutoff_date:
            repo_name = event.get("repo", {}).get("name")
            if repo_name:
                active_repos.add(repo_name)

    return list(active_repos)

def fetch_commits(owner, repo, start_date, end_date):
    """
    Fetch commits from a GitHub repository within a specific date range.
    Args:
        owner (str): Repository owner.
        repo (str): Repository name.
        start_date (str): Start date in YYYY-MM-DD format.
        end_date (str): End date in YYYY-MM-DD format.
    Returns:
        list: List of commit objects.
    """
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/commits"
    params = {"since": f"{start_date}T00:00:00Z", "until": f"{end_date}T23:59:59Z"}
    response = requests.get(url, headers=authenticate(), params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching commits: {response.status_code}, {response.text}")
        return []

def fetch_pull_requests(owner, repo, username, start_date, end_date):
    """
    Fetch pull requests created by the user from a GitHub repository within a specific date range.
    Args:
        owner (str): Repository owner.
        repo (str): Repository name.
        username (str): GitHub username of the user.
        start_date (str): Start date in YYYY-MM-DD format.
        end_date (str): End date in YYYY-MM-DD format.
    Returns:
        list: List of pull request objects created by the user.
    """
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/pulls"
    params = {"state": "all", "sort": "updated", "direction": "desc"}
    response = requests.get(url, headers=authenticate(), params=params)
    if response.status_code == 200:
        prs = response.json()
        return [
            pr for pr in prs
            if start_date <= pr["created_at"][:10] <= end_date
            and pr["user"]["login"] == username
        ]
    else:
        print(f"Error fetching PRs: {response.status_code}, {response.text}")
        return []

def fetch_reviews_by_user(owner, repo, pr_number, username):
    """
    Fetch detailed information about reviews performed by the user for a given pull request.
    Args:
        owner (str): Repository owner.
        repo (str): Repository name.
        pr_number (int): Pull request number.
        username (str): GitHub username of the user performing the review.
    Returns:
        list: List of reviews performed by the user for the PR.
    """
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/pulls/{pr_number}/reviews"
    response = requests.get(url, headers=authenticate())
    if response.status_code == 200:
        reviews = response.json()
        return [review for review in reviews if review["user"]["login"] == username]
    else:
        print(f"Error fetching reviews for PR {pr_number}: {response.status_code}, {response.text}")
        return []

def fetch_issues(owner, repo, username, start_date, end_date):
    """
    Fetch issues created by the user from a GitHub repository within a specific date range.
    Args:
        owner (str): Repository owner.
        repo (str): Repository name.
        username (str): GitHub username of the user.
        start_date (str): Start date in YYYY-MM-DD format.
        end_date (str): End date in YYYY-MM-DD format.
    Returns:
        list: List of issue objects created by the user.
    """
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/issues"
    params = {"state": "all", "sort": "created", "direction": "desc"}
    response = requests.get(url, headers=authenticate(), params=params)
    if response.status_code == 200:
        issues = response.json()
        return [
            issue for issue in issues
            if start_date <= issue["created_at"][:10] <= end_date
            and issue["user"]["login"] == username
        ]
    else:
        print(f"Error fetching issues: {response.status_code}, {response.text}")
        return []

def process_commit(commit):
    """
    Process a commit object to extract relevant details.
    Args:
        commit (dict): Commit object from GitHub API.
    Returns:
        dict: Simplified commit details.
    """
    return {
        "message": commit["commit"]["message"],
        "date": commit["commit"]["author"]["date"]
    }

def process_pull_request(pr):
    """
    Process a pull request object to extract relevant details.
    Args:
        pr (dict): Pull request object from GitHub API.
    Returns:
        dict: Simplified pull request details.
    """
    return {
        "title": pr["title"],
        "state": pr["state"],
        "created_at": pr["created_at"],
        "description": pr["body"],
        "labels": [label["name"] for label in pr["labels"]],
        "assignees": [assignee["login"] for assignee in pr["assignees"]]
    }

def process_issue(issue):
    """
    Process an issue object to extract relevant details.
    Args:
        issue (dict): Issue object from GitHub API.
    Returns:
        dict: Simplified issue details.
    """
    return {
        "title": issue["title"],
        "state": issue["state"],
        "created_at": issue["created_at"],
        "description": issue["body"],
        "labels": [label["name"] for label in issue["labels"]],
        "assignees": [assignee["login"] for assignee in issue["assignees"]]
    }

def fetch_github_activity(owner, repo, username, start_date=None, end_date=None):
    """
    Fetch detailed commits, pull requests, reviews, and issues from a GitHub repository in a given time range.
    Args:
        owner (str): Repository owner.
        repo (str): Repository name.
        username (str): GitHub username of the user.
        start_date (str, optional): Custom start date (YYYY-MM-DD).
        end_date (str, optional): Custom end date (YYYY-MM-DD).
    Returns:
        dict: Dictionary containing simplified commits, PRs, reviews, and issues.
    """
    start_date, end_date = get_time_range(start_date, end_date)

    print(f"Fetching GitHub activity from {start_date} to {end_date}...")

    # Fetch detailed commits
    raw_commits = fetch_commits(owner, repo, start_date, end_date)
    commits = [process_commit(commit) for commit in raw_commits]

    # Fetch detailed pull requests created by the user
    raw_prs = fetch_pull_requests(owner, repo, username, start_date, end_date)
    prs = [process_pull_request(pr) for pr in raw_prs]

    # Fetch detailed reviews performed by the user
    reviews = {}
    for pr in raw_prs:
        pr_number = pr["number"]
        user_reviews = fetch_reviews_by_user(owner, repo, pr_number, username)
        if user_reviews:
            reviews[pr_number] = [{"state": review["state"], "body": review["body"]} for review in user_reviews]

    # Fetch detailed issues created by the user
    raw_issues = fetch_issues(owner, repo, username, start_date, end_date)
    issues = [process_issue(issue) for issue in raw_issues]

    return {
        "commits": commits,
        "pull_requests": prs,
        "reviews": reviews,
        "issues": issues
    }
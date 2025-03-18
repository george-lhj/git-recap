from fetch import *
from format import *
from ollama import *

def main(optional_save=False):
    headers = authenticate()
    response = requests.get(f"{GITHUB_API_URL}/user", headers=headers)
    if response.status_code != 200:
        print(f"Error fetching user info: {response.status_code}, {response.text}")
        return
    user_info = response.json()
    username = user_info["login"]
    active_repos = fetch_active_repositories(username, months=6)
    if not active_repos:
        print("No active repositories found in the past 6 months.")
        return
    
    print("Repositories where you've been active in the past 6 months:")
    for idx, repo_name in enumerate(active_repos, start=1):
        print(f"{idx}. {repo_name}")
    selected_indices = input("Enter the numbers of the repositories you want to fetch (comma-separated): ")
    
    try:
        selected_indices = [int(idx.strip()) - 1 for idx in selected_indices.split(",")]
    except ValueError:
        print("Invalid input. Please enter comma-separated numbers.")
        return
    
    valid_indices = [idx for idx in selected_indices if 0 <= idx < len(active_repos)]
    if not valid_indices:
        print("No valid repositories selected.")
        return

    all_activity = {}
    for idx in valid_indices:
        repo_name = active_repos[idx]
        owner, repo = repo_name.split("/")
        print(f"\nFetching activity for repository: {repo_name}...")
        try:
            activity = fetch_github_activity(owner, repo, username)
            if activity:
                all_activity[repo_name] = activity
        except Exception as e:
            print(f"Failed to fetch activity for {repo_name}: {e}")

    markdown_content = format_activity_as_markdown(all_activity)

    if optional_save:
        save_activity_as_markdown(all_activity)
        try:
            markdown_content = read_markdown_file("github_activity_summary.md")
        except FileNotFoundError as e:
            print(e)
            return
    
    print("Generating weekly summary with Ollama...")
    try:
        summary = summarize_with_ollama(markdown_content)
        print(summary)
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
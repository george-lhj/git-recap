def save_activity_as_markdown(all_activity, filename="github_activity_summary.md"):
    """
    Save aggregated GitHub activity as a Markdown file.
    Args:
        all_activity (dict): Aggregated GitHub activity data.
        filename (str): Name of the Markdown file to save.
    """
    with open(filename, "w") as f:
        f.write("# GitHub Activity Summary\n\n")
        for repo_name, activity in all_activity.items():
            f.write(f"## Repository: {repo_name}\n\n")
            f.write("### Commits\n")
            if activity["commits"]:
                for commit in activity["commits"]:
                    f.write(f"- **Message**: {commit['message']}\n")
                    f.write(f"  - **Date**: {commit['date']}\n")
            else:
                f.write("- No commits found.\n")
            f.write("\n")
            f.write("### Pull Requests\n")
            if activity["pull_requests"]:
                for pr in activity["pull_requests"]:
                    f.write(f"- **Title**: {pr['title']}\n")
                    f.write(f"  - **State**: {pr['state']}\n")
                    f.write(f"  - **Created At**: {pr['created_at']}\n")
                    f.write(f"  - **Description**: {pr['description'] or 'No description provided.'}\n")
                    if pr["labels"]:
                        f.write(f"  - **Labels**: {', '.join(pr['labels'])}\n")
                    if pr["assignees"]:
                        f.write(f"  - **Assignees**: {', '.join(pr['assignees'])}\n")
            else:
                f.write("- No pull requests found.\n")
            f.write("\n")
            f.write("### Reviews I Performed\n")
            if activity["reviews"]:
                for pr_number, review_list in activity["reviews"].items():
                    for review in review_list:
                        f.write(f"- **PR #{pr_number}**\n")
                        f.write(f"  - **State**: {review['state']}\n")
                        f.write(f"  - **Body**: {review['body'] or 'No review comments provided.'}\n")
            else:
                f.write("- No reviews performed.\n")
            f.write("\n")
            f.write("### Issues\n")
            if activity["issues"]:
                for issue in activity["issues"]:
                    f.write(f"- **Title**: {issue['title']}\n")
                    f.write(f"  - **State**: {issue['state']}\n")
                    f.write(f"  - **Created At**: {issue['created_at']}\n")
                    f.write(f"  - **Description**: {issue['description'] or 'No description provided.'}\n")
                    if issue["labels"]:
                        f.write(f"  - **Labels**: {', '.join(issue['labels'])}\n")
                    if issue["assignees"]:
                        f.write(f"  - **Assignees**: {', '.join(issue['assignees'])}\n")
            else:
                f.write("- No issues found.\n")
            f.write("\n")
    print(f"\nGitHub activity summary saved to {filename}")
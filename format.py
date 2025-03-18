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

def format_activity_as_markdown(all_activity):
    """
    Converts activity data to markdown format without saving to a file.
    Returns the markdown content as a string.
    """
    markdown_lines = ["# GitHub Activity Summary\n"]
    
    for repo_name, activity in all_activity.items():
        markdown_lines.append(f"## Repository: {repo_name}\n")
    
        markdown_lines.append("### Commits\n")
        if activity.get("commits"):
            for commit in activity["commits"]:
                markdown_lines.append(f"- **Message**: {commit.get('message', 'No message')}")
                markdown_lines.append(f"  - **Date**: {commit.get('date', 'Unknown Date')}")
        else:
            markdown_lines.append("- No commits found.")
        
        markdown_lines.append("\n### Pull Requests\n")
        if activity.get("pull_requests"):
            for pr in activity["pull_requests"]:
                markdown_lines.append(f"- **Title**: {pr.get('title', 'No title')}")
                markdown_lines.append(f"  - **State**: {pr.get('state', 'Unknown State')}")
                markdown_lines.append(f"  - **Created At**: {pr.get('created_at', 'Unknown Date')}")
                markdown_lines.append(f"  - **Description**: {pr.get('description', 'No description provided.')}")
                if pr.get("labels"):
                    markdown_lines.append(f"  - **Labels**: {', '.join(pr['labels'])}")
                if pr.get("assignees"):
                    markdown_lines.append(f"  - **Assignees**: {', '.join(pr['assignees'])}")
        else:
            markdown_lines.append("- No pull requests found.")

        markdown_lines.append("\n### Reviews I Performed\n")
        if activity.get("reviews"):
            for pr_number, review_list in activity["reviews"].items():
                for review in review_list:
                    markdown_lines.append(f"- **PR #{pr_number}**")
                    markdown_lines.append(f"  - **State**: {review.get('state', 'Unknown State')}")
                    markdown_lines.append(f"  - **Body**: {review.get('body', 'No review comments provided.')}")
        else:
            markdown_lines.append("- No reviews performed.")

        markdown_lines.append("\n### Issues\n")
        if activity.get("issues"):
            for issue in activity["issues"]:
                markdown_lines.append(f"- **Title**: {issue.get('title', 'No title')}")
                markdown_lines.append(f"  - **State**: {issue.get('state', 'Unknown State')}")
                markdown_lines.append(f"  - **Created At**: {issue.get('created_at', 'Unknown Date')}")
                markdown_lines.append(f"  - **Description**: {issue.get('description', 'No description provided.')}")
                if issue.get("labels"):
                    markdown_lines.append(f"  - **Labels**: {', '.join(issue['labels'])}")
                if issue.get("assignees"):
                    markdown_lines.append(f"  - **Assignees**: {', '.join(issue['assignees'])}")
        else:
            markdown_lines.append("- No issues found.")

        markdown_lines.append("\n")  # Separate repositories with a newline
    
    return "\n".join(markdown_lines)
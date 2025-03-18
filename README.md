# git-recap

This repository provides tools to fetch your GitHub activity (commits, pull requests, issues, and reviews) for a specified time range and generate a concise weekly summary. The summary is formatted to align with the team's weekly standup reports, making it easy to share updates during meetings.

Using Ollama, the tool processes the fetched GitHub data and generates human-readable summaries in a structured format.

## Features

- extract detailed contributions from github events, including commits, PRs (created and reviewed), and issues.
- filter out activity by repo and date range
- generate weekly summary in given output format

### Dependencies

- Requires Ollama to be run locally
- Set an `.env` file with `GITHUB_TOKEN`=PERSONAL_ACCESS_TOKEN from github.

#### Running

- Simply use `python3 main.py`. Can set `main(optional_save=True)` to save the pulled events to a file, otherwise it runs in terminal by default.

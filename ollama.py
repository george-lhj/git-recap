import os
import requests

OLLAMA_API_URL = "http://localhost:11434/api/generate" 
MODEL_NAME = "llama3.1:latest"

def read_markdown_file(file_path):
    """
    Read the contents of a Markdown file.
    Args:
        file_path (str): Path to the Markdown file.
    Returns:
        str: Contents of the file.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()
    
def summarize_with_ollama(content, model_name=MODEL_NAME):
    """
    Send the content to Ollama for summarization.
    Args:
        content (str): Content to summarize.
        model_name (str): Name of the Ollama model to use.
    Returns:
        str: Generated summary.
    """

    prompt = (f"""
        Format the following GitHub activity report. 
        Organize the contributions into sections for PRs, commits, issues, and reviews. 
        For each section, include links to relevant PRs or issues along with brief descriptions. 
        You do not need to include the dates, but try to take the descriptions provided and expand on it in the report.
              
        Follow this structure:

        PRs (count): Repository Name
        - [Link to PR] <= Description
        - [Link to PR] <= Description

        Commits (count): Repository Name
        - [Link to Commit] <= Description
        - [Link to Commit] <= Description

        Issues (count):
        - [Link to Issue] <= Description
        - [Link to Issue] <= Description

        Reviews (count): Repository Name
        - Reviewed PR #X: Description
        - Reviewed PR #Y: Description

        Here is the GitHub activity data:
        {content}
        """
    )

    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_API_URL, json=payload)
        if response.status_code != 200:
            raise Exception(f"Ollama API error: {response.status_code}, {response.text}")

        result = response.json()
        return result.get("response", "No summary generated.")

    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to connect to Ollama: {e}")



input_file = "github_activity_summary.md"

try:
    markdown_content = read_markdown_file(input_file)
    print("Generating weekly summary with Ollama...")
    summary = summarize_with_ollama(markdown_content)
    print(summary)
except FileNotFoundError as e:
    print(e)
except Exception as e:
    print(f"An error occurred: {e}")
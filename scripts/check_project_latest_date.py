#!/usr/bin/python3

import json, os, re
from urllib.error import HTTPError
from urllib.request import Request, urlopen


def get_latest_commit_date(github_url):
    # Extract 'owner/repo' from URLs like https://github.com/owner/repo or https://github.com/owner/repo.git
    match = re.search(r"github\.com/([^/]+)/([^/\.]+)", github_url)
    if not match:
        return None

    owner, repo = match.groups()

    api_url = f"https://api.github.com/repos/{owner}/{repo}/commits/"
    branches = ["main", "master"]
    for branch in branches:
        try:
            # GitHub API requires a User-Agent header
            req = Request(f"{api_url}{branch}", headers={"User-Agent": "Python-Script"})
            with urlopen(req) as response:
                data = json.loads(response.read().decode())
                # Commit date in ISO 8601 format (e.g., 2026-03-15T10:00:00Z)
                date = data["commit"]["committer"]["date"]
                return date.split("T")[0] # Keep Y-M-D format
        except HTTPError as e:
            if e.code != 422:
                print(f"Error fetching commit for {github_url}: {e}")
                return None


def main():
    path = "_projects/"

    if not os.path.exists(path):
        print(f"Directory '{path}' not found.")
        return

    for project in os.listdir(path):
        file_path = os.path.join(path, project)
        if not os.path.isfile(file_path):
            continue

        # Open in 'r' mode to read lines safely
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        online_commit_date = None
        local_commit_date = None
        commit_date_idx = -1

        for idx, line in enumerate(lines):
            stripped_line = line.strip()

            if stripped_line.startswith("source"):
                source = stripped_line.split(" ")[-1].replace('"', '')
                online_commit_date = get_latest_commit_date(source)

            if stripped_line.startswith("last_updated"):
                local_commit_date = stripped_line.split(" ")[-1]
                commit_date_idx = idx

            if online_commit_date and local_commit_date:
                break

        print(f"Project: {project}")
        print(f"  Online Date: {online_commit_date}")
        print(f"  Local Date:  {local_commit_date}")

        # String comparison works for YYYY-MM-DD ISO format
        if online_commit_date and local_commit_date:
            if online_commit_date > local_commit_date:
                print(f"  -> Updating {project} to {online_commit_date}...")

                # Preserve indentation/formatting by replacing line content
                prefix = lines[commit_date_idx].split(":")[0]
                lines[commit_date_idx] = f"{prefix}: {online_commit_date}\n"

                # Overwrite file with modified content
                with open(file_path, "w", encoding="utf-8") as file:
                    file.writelines(lines)
            else:
                print("  -> Up to date.")


if __name__ == "__main__":
    main()

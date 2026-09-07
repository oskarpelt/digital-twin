import base64
import json
import subprocess
from pathlib import Path

OUTPUT = Path(__file__).parent.parent / "github.txt"

MAX_README_CHARS = 2000


def gh(*args):
    result = subprocess.run(["gh", *args], capture_output=True, text=True, check=True)
    return result.stdout


def fetch_repos():
    output = gh("repo", "list", "--json", "nameWithOwner,description,url", "--limit", "50", "--no-archived", "--visibility", "public")
    return json.loads(output)


def fetch_readme(name_with_owner):
    try:
        output = gh("api", f"repos/{name_with_owner}/readme", "--jq", ".content")
        text = base64.b64decode(output.strip()).decode("utf-8")
        return text[:MAX_README_CHARS] + ("..." if len(text) > MAX_README_CHARS else "")
    except subprocess.CalledProcessError:
        return ""


def main():
    repos = fetch_repos()
    sections = []

    for repo in repos:
        name_with_owner = repo["nameWithOwner"]
        name = name_with_owner.split("/")[-1]
        description = repo.get("description") or ""
        url = repo["url"]
        readme = fetch_readme(name_with_owner)

        section = f"## {name}\n{url}"
        if description:
            section += f"\n{description}"
        if readme:
            section += f"\n\n{readme}"
        sections.append(section)

    output = "# GitHub Projects\n\n" + "\n\n---\n\n".join(sections)

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write(output)

    print(f"Written {len(repos)} repos to github.txt")


if __name__ == "__main__":
    main()

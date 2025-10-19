import os
import requests
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
    "User-Agent": "my-app"
}

# repo_owner = "Divy13ansh"
# repo_name = "sih_2025"

# url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/"

def dir_structure(owner, repo, path=""):
    """
    Recursively fetch the directory structure of a GitHub repository.
    Returns a nested list/dict representing files and folders.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    data = r.json()
    
    structure = []
    for item in data:
        if item["type"] == "dir":
            sub_structure = dir_structure(owner, repo, path=item["path"])
            structure.append({item["name"]: sub_structure})
        else:
            structure.append(item["name"])
    return structure


def parse_url(repo_url):
    """Extract owner and repo name from GitHub URL."""
    try:
        parts = repo_url.rstrip('/').split('/')
        owner = parts[-2]
        repo = parts[-1].replace('.git', '')
        return owner, repo
    except IndexError:
        raise ValueError("Invalid GitHub repository URL.")
    

def tree_structure_str(structure, prefix=""):
    """
    Recursively build a tree-like string from a nested structure.
    """
    lines = []
    for i, item in enumerate(structure):
        connector = "└── " if i == len(structure) - 1 else "├── "
        
        if isinstance(item, dict):
            for folder, contents in item.items():
                lines.append(f"{prefix}{connector}{folder}/")
                extension = "    " if i == len(structure) - 1 else "│   "
                lines.append(tree_structure_str(contents, prefix + extension))
        else:
            lines.append(f"{prefix}{connector}{item}")
    
    return "\n".join(lines)


def get_repo_structure(repo_url):
    """Get the directory structure from a GitHub repository URL."""
    owner, repo = parse_url(repo_url)
    structure = dir_structure(owner, repo)
    structure = tree_structure_str(structure)
    return structure

def repo_dict(repo_url):
    """Get the directory structure as a nested dictionary from a GitHub repository URL."""
    owner, repo = parse_url(repo_url)
    structure = dir_structure(owner, repo)
    return structure
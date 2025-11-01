#!/usr/bin/env python3

"""
Handy dandy script for starting a new JIRA ticket, does some novel things

* given a ticket ref (e.g. MYPROJ-1234), queries JIRA for ticket description
* slugifies that description
* cuts a branch with the slugified description (after pulling latest from origin
  for specified target branch)
* creates a task in VS Code
"""


import json
import subprocess
import sys
from datetime import datetime
from getpass import getpass
from shutil import copyfile

from requests import request
from requests.auth import HTTPBasicAuth
from cryptocode import decrypt, encrypt
from slugify import slugify  # from python-slugify


def get_auth(decrypt_key):
    # keyfile contains the encrypted contents of my JIRA password,
    # read and decrypt to get the actual password & generate the
    # http basic auth.
    with open(".vscode/keyfile", "r", encoding="utf-8") as fobj:
        keyfile = fobj.readline().strip()

    passcode = decrypt(keyfile, decrypt_key)
    return HTTPBasicAuth(username="adam.parkin@zapier.com", password=passcode)


def do_jira_stuff(task_name, decrypt_key):
    """Build a slugified task name from JIRA ticket info."""

    issue_type_icon_map = {
        "Initiative": "☑️",
        "Epic": "⚡",
        "Spike": "💡",
        "Story": "✅",
        "Bug": "🐛",
        "Design Task": "🎨",
        "Security Bug": "🔒",
        "Task": "📝",
    }
    priority_level_map = {
        "Highest": "0️⃣",
        "High": "1️⃣",
        "Medium": "2️⃣",
        "Low": "3️⃣",
        "Lowest": "4️⃣",
    }

    headers = {
        "Content-Type": "application/json",
    }
    response = request(
        "GET",
        f"https://zapierorg.atlassian.net/rest/api/2/issue/{task_name}?fields=summary,issuetype,priority",
        headers=headers,
        auth=get_auth(decrypt_key),
        timeout=30,
    ).json()

    fields = response["fields"]
    summary = fields.get("summary")
    issue_type = fields.get("issuetype", {}).get("name", "Task")
    icon = issue_type_icon_map.get(issue_type, "📝")
    key = response["key"]
    priority = fields.get("priority", {}).get("name")
    priority = (
        ""
        if not priority or priority.lower() == "none"
        else priority_level_map.get(priority, "❓")
    )

    return f"{key}-{priority}-{icon}-{slugify(summary)}"


def do_git_stuff(task_name, branch):
    """Create & checkout a new git branch for the task."""
    subprocess.run(f"git checkout {branch}".split(), check=True)
    subprocess.run(f"git pull origin {branch}".split(), check=True)
    subprocess.run(f"git checkout -b {task_name[:100]}".split(), check=True)


def add_to_tasks_context(task_name):
    """
    Add the new task to the VS Code tasks context file.

    Will create the file if it doesn't already exist.
    """
    fname = ".vscode/tasks-context.json"

    try:
        with open(fname, "r", encoding="utf-8") as fobj:
            data = json.load(fobj)
        copyfile(fname, f"{fname}.bak")
    except FileNotFoundError:
        data = {"tasks": []}

    new_item = {
        "name": task_name,
        "complete": False,
        "creationDate": datetime.now().isoformat(),
        "files": [],
    }
    data["tasks"].append(new_item)

    data_to_write = json.dumps(data, indent=2)

    with open(fname, "w", encoding="utf-8") as fobj:
        fobj.write(data_to_write)


def regenerate_key_file():
    """Regenerate the keyfile used to store encrypted JIRA password."""

    password = getpass("Enter JIRA password: ")
    encrypted = encrypt(password, getpass("enter decryption key: "))
    with open(".vscode/keyfile", "w", encoding="utf-8") as fobj:
        fobj.write(encrypted)
    print("Successfully regenerated keyfile")


def main():
    """
    Main entry point for the script.
    """
    # if 1st arg is "regen" then regenerate the keyfile
    if len(sys.argv) == 2 and sys.argv[1] == "regen":
        regenerate_key_file()
        return 1

    if len(sys.argv) < 4:
        print("Need to specify name, decryption key, and branch")
        return 1

    task_name = sys.argv[1]
    key = sys.argv[2]
    branch = sys.argv[3]
    task_name = do_jira_stuff(task_name, key)
    print(f"Creating new ticket: {task_name}")
    do_git_stuff(task_name, branch)
    add_to_tasks_context(task_name)


if __name__ == "__main__":
    exit(main())

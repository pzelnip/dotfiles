#!/usr/bin/env python3

"""
Handy dandy script for starting a new JIRA ticket, does some novel things

* given a ticket ref (e.g. MYPROJ-1234), queries JIRA for ticket description
* slugifies that description
* cuts a branch with the slugified description (after pulling latest from origin
  for specified target branch)
* creates a task in VS Code
"""


import argparse
import contextlib
import json
import subprocess
from datetime import datetime
from getpass import getpass
from shutil import copyfile

import keyring
from cryptocode import decrypt, encrypt
from requests import request
from requests.auth import HTTPBasicAuth
from slugify import slugify  # from python-slugify


def get_auth(account, key_string):
    """Get JIRA auth."""

    # Currently this is implemented to use keyring to get the password/API
    # token.
    #
    # See https://id.atlassian.com/manage-profile/security/api-tokens for
    # details on how to generate a token.
    #
    # We store the token encrypted in the keyring using a user-provided
    # decryption string.

    passcode = keyring.get_password("jira", account)
    if not passcode:
        print("No JIRA password stored in keyring")
        passcode = encrypt(getpass("Enter JIRA API token: "), key_string)
        keyring.set_password("jira", account, passcode)

    if (decrypted_passcode := decrypt(passcode, key_string)) is False:
        print("Failed to decrypt JIRA API token, perhaps the key is wrong?")
        exit(1)

    return HTTPBasicAuth(username=account, password=decrypted_passcode)


def do_jira_stuff(task_name, account, key_string):
    """Build a slugified task name from JIRA ticket info."""

    issue_type_icon_map = {
        "Initiative": "☑️",
        "Epic": "⚡",
        "Spike": "💡",
        "Story": "✍️",
        "Bug": "🐛",
        "Design Task": "🎨",
        "Security Bug": "🔒",
        "Task": "📝",
    }
    priority_level_map = {
        "Highest": "0",
        "High": "1",
        "Medium": "2",
        "Low": "3",
        "Lowest": "4",
    }

    headers = {
        "Content-Type": "application/json",
    }
    response = request(
        "GET",
        # FIXME: move to newest API
        f"https://zapierorg.atlassian.net/rest/api/2/issue/{task_name}?fields=summary,issuetype,priority",
        headers=headers,
        auth=get_auth(account, key_string),
        timeout=30,
    ).json()

    fields = response["fields"]
    summary = fields.get("summary")
    issue_type = fields.get("issuetype", {}).get("name", "Task")
    icon = issue_type_icon_map.get(issue_type, "📝")
    key = response["key"]
    priority = fields.get("priority", {}).get("name")
    priority = (
        "🤷‍♂️"
        if not priority or priority.lower() == "none"
        else f"P{priority_level_map.get(priority, "???")}"
    )

    return f"{key}-{priority}-{icon}-{slugify(summary)}"


def get_default_branch():
    """Get the default branch name from git."""

    # try origin/HEAD first
    with contextlib.suppress(subprocess.CalledProcessError):
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "origin/HEAD"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip().replace("origin/", "")

    # fall back to git ls-remote if that fails
    with contextlib.suppress(subprocess.CalledProcessError):
        result = subprocess.run(
            ["git", "ls-remote", "--symref", "origin", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        )
        for line in result.stdout.strip().split("\n"):
            if line.startswith("ref:"):
                return line.split()[1].replace("refs/heads/", "")

    # if all else fails, raise an error
    raise RuntimeError("Failed to determine default branch")


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


def parse_args():
    parser = argparse.ArgumentParser(
        description="Create a new JIRA ticket branch and VS Code task"
    )
    parser.add_argument(
        "-t",
        "--task",
        required=True,
        help="JIRA ticket reference (e.g. MYPROJ-1234)",
    )
    parser.add_argument("-a", "--account", required=True, help="JIRA account/username")
    parser.add_argument(
        "-k",
        "--key",
        required=True,
        help="Decryption key for decoding stored API token",
    )
    return parser.parse_args()


def main():
    """
    Main entry point for the script.
    """
    args = parse_args()

    task_name = do_jira_stuff(args.task, args.account, args.key)
    branch = get_default_branch()
    print(f"Creating task branch: {task_name} based on {branch}")
    do_git_stuff(task_name, branch)
    add_to_tasks_context(task_name)


if __name__ == "__main__":
    exit(main())

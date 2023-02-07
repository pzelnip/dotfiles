#!/usr/bin/env python3

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
    with open(".vscode/keyfile", "r") as fobj:
        keyfile = fobj.readline().strip()

    passcode = decrypt(keyfile, decrypt_key)
    return HTTPBasicAuth(username="adam.parkin@zapier.com", password=passcode)


def do_jira_stuff(task_name, decrypt_key):
    headers = {
        "Content-Type": "application/json",
    }
    response = request(
        "GET",
        f"https://zapierorg.atlassian.net/rest/api/2/issue/{task_name}?fields=summary",
        headers=headers,
        auth=get_auth(decrypt_key),
    ).json()
    summary = response["fields"]["summary"]
    key = response["key"]
    return f"{key}-{slugify(summary)}"


def do_git_stuff(task_name, branch):
    subprocess.run(f"git checkout {branch}".split(), check=True)
    subprocess.run(f"git pull origin {branch}".split(), check=True)
    subprocess.run(f"git checkout -b {task_name}".split(), check=True)


def add_to_tasks_context(task_name):
    fname = ".vscode/tasks-context.json"
    with open(fname, "r") as fobj:
        data = json.load(fobj)

    new_item = {
        "name": task_name,
        "complete": False,
        "creationDate": datetime.now().isoformat(),
        "files": [],
    }
    data["tasks"].append(new_item)

    copyfile(fname, f"{fname}.bak")
    data_to_write = json.dumps(data, indent=2)

    with open(fname, "w") as fobj:
        fobj.write(data_to_write)


def regenerate_key_file():
    password = getpass("Enter JIRA password: ")
    encrypted = encrypt(password, getpass("enter decryption key: "))
    with open(".vscode/keyfile", "w") as fobj:
        fobj.write(encrypted)
    print("Successfully regenerated keyfile")


def main():
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

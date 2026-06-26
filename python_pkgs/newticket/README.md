# newticket

Handy script for starting work on a new ticket. Given a ticket reference it:

- queries the issue tracker (JIRA or Linear) for the ticket's details
- slugifies the summary/title into a branch-name-friendly string
- pulls the latest default branch and cuts a new branch from it
- registers the task in `.vscode/tasks-context.json`

The branch name follows the format `KEY-PRIORITY-ICON-slugified-title`, e.g.
`EDC-10195-P2-📝-backfill-cleanup-of-orphaned-zapstorage-records`.

## Install / reinstall

Installed via [pipx](https://pipx.pypa.io/) (see the repo's
`install_py_pkgs.sh`). There is no separate build step — `pipx` runs `setup.py`.

From the dotfiles root:

```sh
# first install
pipx install python_pkgs/newticket

# reinstall after changing the source (plain install is a no-op if present)
pipx install --force python_pkgs/newticket
```

> `pipx install` copies the source into its own venv — it does **not** symlink,
> so working-tree edits won't take effect until you re-run with `--force`.
> For active development, use an editable install instead:
> `pipx install -e python_pkgs/newticket`.

Verify:

```sh
pipx list | grep newticket
```

## Usage

```sh
newticket -t <ticket-id> [--tracker {jira,linear}] [-a <account> -k <key>]
```

### JIRA (default)

`--tracker` defaults to `jira`. `--account`/`--key` are required in this mode.

```sh
newticket -t MYPROJ-1234 -a you@example.com -k <decryption-key>
```

Auth uses `keyring` to store an encrypted JIRA API token; `--key` decrypts it.
See <https://id.atlassian.com/manage-profile/security/api-tokens> for generating
a token.

### Linear

```sh
newticket -t EDC-10195 --tracker linear
```

Linear support shells out to the [`linear`
CLI](https://github.com/schpet/linear-cli), so:

- the CLI must be installed and authenticated (`linear auth`)
- `--account`/`--key` are **not** needed (the CLI handles auth)

Notes on the Linear mapping:

- **Priority**: Linear's integer priority (`0`=None, `1`=Urgent, `2`=High,
  `3`=Medium, `4`=Low) is mapped to the same `P0`-`P3`/`X` indicators as JIRA.
- **Icon**: Linear has no issue-type concept, so the icon is derived from the
  issue's labels (matched against the built-in icon map), defaulting to 📝.
- Queries the CLI's raw GraphQL endpoint (`linear api`) rather than
  `linear issue view`, because the latter does not return labels.

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

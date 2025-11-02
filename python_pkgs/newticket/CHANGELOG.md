# Revision History

## [Unreleased]
### Added
### Changed
### Deprecated
### Removed
### Fixed
### Security

## [1.0.0] - 2025-11-01

### Changed

- *BREAKING* Updated command-line arguments: now requires account parameter
  in addition to decryption key
- *BREAKING* Updated command-line arguments: branch no longer supplied, read
  from repo instead
- Switched from encrypted keyfile to `keyring` library for secure
  credential storage
- use argparse instead of `sys.argv` for command line arguments
- Command usage now: `newticket -t <ticket-id> -a <account> -k <key>`
- priority indicator changed from emoji numeral to ASCI digit (when known)

### Removed

- Removed `regenerate_key_file()` function and "regen" command
- Removed dependency on `.vscode/keyfile` for password storage

### Security

- Improved security by using OS-level keyring instead of encrypted file for credential storage

## [0.0.3] - 2025-11-01

### Added

- emoji's to JIRA-derived task name, now includes issue type & priority if present

### Fixed

- added encoding arguments to all the `open()` calls
- script no longer errors if `.vscode/tasks-context.json` doesn't exist, instead
  creates a new file

## [0.0.2] - 2023-07-23

### Changed

- branch name limited to 100 characters
- added 30 sec timeout to JIRA REST API call

## [0.0.1] - 2023-02-07

### Added

- Initial release

---

**Note:** This project follows [Semantic Versioning](https://semver.org/) and
the format is based on [Keep a Changelog](https://keepachangelog.com/).

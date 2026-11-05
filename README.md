# Stack Attack updates

Public update downloads for Stack Attack, a local multiplayer falling-block game.

**Existing players:** use **Settings > System > Game updates** in a complete
version 0.17 or newer installation. Check, confirm the update, then restart.
No GitHub login or access token is required on your device. Your original music
folders, controller mappings and settings are preserved.

[Latest update downloads](https://github.com/w-Twich/stack-attack-updates/releases/latest)

These downloads are runtime-only updates, not complete first-time installers.
First install the full game using the package supplied by the developer. Launch
`StackAttack.pygame` on Batocera, `PLAY_MAC.command` on Mac, `PLAY_WINDOWS.bat` on
Windows, or `python main.py` on other supported source installations.

## Publishing

Development source/history and the full soundtrack are kept in a separate
private repository. Each public release contains game runtime Python code and
background artwork, with no music, user settings, secrets or development tools.
The Python code in a download is readable even though development is private.

The `release/` directory is an encoded transport copy of the current verified
update plus its checksum metadata. A trusted maintainer stages it after the
private game tests pass. The GitHub Actions workflow reassembles and validates
the archive and its file allowlist, then publishes it using this repository's
short-lived `GITHUB_TOKEN`. No cross-repository personal token is used.

Publication creates a draft first and makes it public only after all files are
uploaded. Each version is published once. To retry after a failed upload, inspect
and remove the incomplete draft before rerunning the workflow. Normal game
launches only check for updates; installation always requires confirmation.

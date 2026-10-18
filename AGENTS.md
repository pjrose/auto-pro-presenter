# ProPresenter service preparation

## Check network access first

Before reading service attachments or operating the ProPresenter interface,
run `python check_setup.py` from this repository. This checks the configured
local API before any lengthy work; `--show-root` is optional for this first
check. An explicit `--api-url http://HOST:PORT` or `PROPRESENTER_API_URL` can
override Windows preference discovery. Never guess or scan ports.

If Network is off or the API is unavailable, stop the service-preparation
workflow within the first ten seconds and tell the user to enable Network in
ProPresenter Settings and verify its port. Do not retry repeatedly, wait for
the app, or substitute a computer-use workflow. If the error is a sandbox or
OS permission denial, identify that accurately instead of claiming Network
is off. Resume only after the user resolves the issue or explicitly requests
an alternative. "Stop" means stop the workflow, not close ProPresenter.

The check has an eight-second total probe deadline and no retries. Staging
also requires a successful preflight. The later `--apply` step and standalone
theme installation are intentionally offline because ProPresenter must be
closed; do not demand a live API during that already-authorized step.

## Routine restarts

When preparing or updating a service in this project, gracefully closing and
reopening ProPresenter is authorized whenever necessary to install or verify
the requested changes. Accept the standard "Are you sure you want to quit
ProPresenter?" confirmation without asking the user again. This project
preference explicitly overrides a skill's default requirement to ask about
that routine quit confirmation.

Save pending work before quitting. Do not discard unsaved work or force-kill
ProPresenter under this authorization. If a dialog would discard unsaved work
and it cannot be saved safely, ask the user. A user's current instruction to
leave ProPresenter open takes precedence.

Stage and validate files before closing the app, wait until its process has
fully exited before applying files, back up overwritten files, and reopen it
afterward.

## Visual review

Maximize ProPresenter before inspecting or operating its interface, including
after each restart. Verify slide dimensions separately from the window size.

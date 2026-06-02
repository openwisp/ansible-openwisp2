# AGENTS.md

## Project Overview

`ansible-openwisp2` is the Ansible role used to deploy OpenWISP on virtual machines.

Core code lives in this repository root:

- `tasks/`, `handlers/`, `defaults/`, `vars/`, and `meta/` define role behavior and variables.
- `templates/` and `files/` provide generated service, Django, nginx, uWSGI, supervisor, and FreeRADIUS configuration.
- `molecule/` contains integration scenarios.
- Documentation lives in `docs/`.

## Source of Truth

- Use `README.md` and `docs/` for setup, role variables, and deployment behavior.
- Use `.github/workflows/ci.yml`, `.ansible-lint`, and `.yamllint.yml` for CI-tested QA and test commands.
- Use GitHub issue/PR templates when asked to open issues or PRs.

If instructions conflict, repository config and CI workflows win first, docs next, and this file is supplemental.

## Development Notes

- Keep changes focused. Avoid unrelated refactors and formatting churn.
- Preserve role variables, defaults, handlers, task ordering, idempotency, supported OS behavior, and upgrade paths unless explicitly required.
- Be careful with templates, secrets, file ownership, permissions, service restarts, migrations, and FreeRADIUS/nginx/supervisor integration.
- Avoid unnecessary blank lines inside Jinja, YAML, and shell blocks.
- Update docs when variables, defaults, setup steps, supported OS versions, or deployment behavior change.

## Testing and QA

- Add or update Molecule or role tests for behavior changes when applicable.
- For bug fixes, write or update the failing test or scenario first when feasible, confirm it fails for the expected reason, then implement the fix.
- Use targeted checks while iterating, then run the documented full QA/test command before considering the change complete.
- Run `./run-qa-checks` when present. Treat failures as blocking unless confirmed unrelated and reported.

## Security Notes

- Watch for leaked secrets, unsafe defaults, weak permissions, unsafe shell expansion, and templates that expose credentials.
- Preserve safe handling of Django secret keys, database credentials, TLS material, FreeRADIUS secrets, private keys, and admin credentials.
- Write comments only when they explain why code is shaped a certain way. Put comments before the relevant block instead of scattering them inside it.

## Troubleshooting

- If setup, QA, Molecule, or role execution fails, check docs first, then compare with CI. If commands diverge, follow CI.

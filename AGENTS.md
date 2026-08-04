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

- Preserve role variables, defaults, handlers, task ordering, idempotency, supported OS behavior, and upgrade paths unless explicitly required.
- Be careful with templates, secrets, file ownership, permissions, service restarts, migrations, and FreeRADIUS/nginx/supervisor integration.
- Be careful when changing nginx listen directives, FreeRADIUS listen addresses, or service ports. Do not broaden a service's network exposure beyond the role's documented deployment configuration without an explicit requirement.
- Avoid unnecessary blank lines inside Jinja, YAML, and shell blocks.
- Prefer short, precise names that rely on their nearest meaningful scope. Do not repeat a feature, domain object, or namespace already named by the containing module, class, or function. For example, prefer `EstimatedLocation.refresh()` over `EstimatedLocation.refresh_estimated_location()`. Repeat that context only when the name is used outside that scope or is needed to distinguish genuinely different concepts. When a concise name cannot express a necessary distinction, use a concise docstring to describe it rather than encoding it in an excessively long name.
- Before adding a comment or docstring, ask whether it conveys information a reader cannot reasonably infer from clear code, names, and surrounding scope. Add a concise comment when it explains a non-obvious reason, constraint, compatibility or security requirement, side effect, or unavoidable complexity. In opaque syntax or domain-specific code, especially shell scripts, a comment may also explain what the code does. Do not add comments that merely restate adjacent code one-to-one.
- Update docs when variables, defaults, setup steps, supported OS versions, or deployment behavior change.
- Review documentation examples and references when behavior changes.
- Preserve public documentation anchors, URLs, include directives, and versioned links unless explicitly required.

## Testing and QA

- Add or update Molecule or role tests for every role behavior change.
- For bug fixes, write or update the failing test or scenario first, run it against the unfixed code, confirm it fails for the expected reason, then implement the fix.
- Use targeted checks while iterating, then run the documented full QA/test command before considering the change complete.
- Treat QA failures as blocking unless confirmed unrelated and reported.

## Security Notes

- Watch for leaked secrets, unsafe defaults, weak permissions, unsafe shell expansion, and templates that expose credentials.
- Preserve safe handling of Django secret keys, database credentials, TLS material, FreeRADIUS secrets, private keys, and admin credentials.
- Prevent secret disclosure, unsafe deployment instructions, stale security guidance, and insecure links.

## Troubleshooting

- If documentation and CI commands differ, use CI for verification and report the exact documentation path, CI workflow path, and differing commands. Do not change the documentation until the user explicitly chooses one of these actions: update the named documentation file in the current change because the divergence was caused by that change, or leave it unchanged for a separate follow-up. Never decide that scope distinction independently.

## Contributing Guidelines

- Before editing, inspect the relevant implementation, tests, documentation, and configuration. Follow existing repository patterns and do not invent behavior or requirements.
- Keep each contribution focused and change only the lines necessary for its goal. Do not include unrelated refactors, formatting churn, or generated and dependency-file changes unless explicitly required.
- Add or update focused tests for every behavior change. For bug fixes, follow the regression-test rule above.
- Run the relevant targeted tests, builds, and documented QA checks, including `./run-qa-checks` when provided. Do not claim a change is complete when verification fails; report the failure or blocker.
- When requirements, intended behavior, or an unexpected failure are unclear, stop and seek clarification instead of making speculative changes.
- When starting work on a new issue, create a new branch from `master`. Use `issues/<issue-number>-<short-title>` for issue work; otherwise, use a short, descriptive branch name.
- Commit messages must be descriptive and use past tense. Past tense is a writing guideline that agents and contributors must follow; it is not checked automatically. For issue work, use an allowed prefix and a capitalized, past-tense subject ending with `#<issue-number>`, for example `[fix] Fixed perennial "modified" state #213`. Repeat the issue reference in the body with `Fixes`, `Closes`, `Resolves`, or `Related to` as appropriate. Use `openwisp-commit --check` to validate the structural commit convention and `cz -n cz_openwisp info` to view the allowed prefixes and message structure. If the repository's declared QA dependency predates these commands, install the development version with `pip install --upgrade "openwisp-utils[qa] @ https://github.com/openwisp/openwisp-utils/archive/refs/heads/master.tar.gz"` in the development environment.
- Add an explanatory commit body only for substantial changes, new features, or non-obvious bug fixes. The releaser automatically publishes the subject of `[feature]`, `[change]`, `[change!]`, `[deps]`, and `[fix]` commits, including scoped variants, in the changelog. Write those subjects in clear, user-friendly language suitable for release notes.
- Send new commits in response to review feedback instead of amending existing commits.

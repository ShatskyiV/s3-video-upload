Contributing to rs-automation
=============================

Purpose
-------
This document explains how to contribute code and changes via Pull Requests (PRs), and standard conventions the project expects for branches, commit messages, PR descriptions, reviews, and CI.

Quick start
-----------
- Fork or create a branch from `main`.
- Implement a small, focused change (one logical thing per PR).
- Run tests and linters locally.
- Push your branch and open a Pull Request.

Branch naming
-------------
Use structured and readable branch names:
- feature/<ticket>-short-description (e.g. `feature/RS-123-add-xray-import`)
- fix/<ticket>-short-desc
- chore/<area>/short-desc

Commit messages
---------------
Follow Conventional Commits:
- `feat(scope): short summary`
- `fix(scope): short summary`
- `chore: update deps`

Example: `feat(xray): add import step to CI`
Include ticket/Jira reference in body if applicable.

Pull Request conventions
------------------------
Title:
- Use imperative mood and be short, e.g. "Add Xray import step for CI"

Description sections (use the PR template):
- Summary: one-paragraph description of the change
- Motivation: why this change is required
- Implementation notes: key files / decisions
- Testing: how you tested it locally / in CI
- Rollout / Backwards compatibility notes
- Linked issues / Jira IDs

PR Checklist (fill before requesting review):
- [ ] Tests added/updated
- [ ] Linting passes locally
- [ ] CI checks are green
- [ ] Documentation updated (README/CHANGELOG/other)
- [ ] Code is reviewed and approved by required reviewers
- [ ] PR size rationale added if large (>400 LOC)

Review process
--------------
- Request reviews from `CODEOWNERS` automatically or manually add reviewers.
- Reviewers should aim to respond within 48 hours.
- Use GitHub review tools (`Request changes` / `Approve` / `Comment`).
- Prefer smaller follow-up PRs over very large PRs when possible.

CI and checks
-------------
Protected branches should require these checks before merge:
- Linting
- Unit tests
- Static analysis / type checks
- Security scans (dependabot / SCA)
- JUnit-style test result publication

Labels and sizing
-----------------
Use labels to classify PRs:
- `type/feature`, `type/bug`, `type/chore`
- `size/XS`, `size/S`, `size/M`, `size/L`, `size/XL`
- `needs-review`, `needs-qa`, `docs`

Merging strategy
----------------
- Prefer `Squash and merge` for single logical changes.
- Preserve meaningful commit info in the PR description when squashing.
- Use `Rebase` for fast-forward maintenance branches only if team agrees.

Templates & files
-----------------
This repo includes (or should include):
- `.github/PULL_REQUEST_TEMPLATE.md` — PR template with checklist
- `CONTRIBUTING.md` — this file
- `CODEOWNERS` — file to auto-request reviewers for paths

Contact / Questions
-------------------
If you're unsure which reviewers to add, ping the repo maintainers or use the team chat.


Guide for maintainers
---------------------
- Keep templates up to date.
- Periodically review labels and automation rules.
- Enforce branch protection rules and required status checks.
- Update `CODEOWNERS` whenever team ownership changes.

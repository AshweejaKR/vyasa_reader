# Claude Code prompt — Phase 06: secure AWS EC2 deployment

Prepare simple, copy-pasteable deployment for **my existing Amazon Linux AWS EC2 instance**, with Nginx + Gunicorn + Flask + HTTPS. Do **not** change infrastructure or touch a real EC2 server without explicit permission.

## Required workflow

1. Read `CLAUDE.md`, `README.md`, `PLAN.md`, `SOURCES_AND_RIGHTS.md`, `docs/PROGRESS.md`, this prompt, and only files relevant to this phase.
2. First respond with a short plan (1–3 steps) and file paths. **WAIT for `APPROVED` before editing.**
3. After approval, implement **this phase only**; keep code simple (functions, few files, ~150 lines/file), no factories, extra frameworks, tests, mocks, scraping, or unrelated work.
4. **Do not execute** shell/Python, builds, tests, installs, Git, deployment, or remote AWS actions. No fabricated verification. Document commands for user execution when needed.
5. Update `docs/PROGRESS.md` and prepend a concise entry in `docs/DEVELOPMENT_LOG.md` only after completing the phase. State `Verification: not run`. **STOP.**

## Work after approval

- Use only user-provided facts to identify Amazon Linux release, architecture and package manager. If unknown, include a **manual check** in the runbook with version-dependent alternatives; do not execute checks or assume an AMI.
- Create `deploy/DEPLOY_EC2.md` showing: Python/venv, install app, Gunicorn bound to `127.0.0.1:8000`, non-root systemd service, Nginx reverse proxy, startup/restart, log inspection, updates and rollback.
- Describe domain A/AAAA records pointing at stable EC2 address (Elastic IP if used), trusted HTTPS certificate issuance and renewal (e.g. Certbot if supported). Ask for actual domain/hostname only when needed, and use placeholders until supplied.
- Include exact Security Group guidance: inbound 443, 80 for redirect/challenge if needed, and SSH from the owner's IP only. Port 8000 must **not** be public. Do not expose Flask debug.
- Include **user-run manual verification steps** after HTTPS: install, close/reopen, resume, service reboot, certificate, port reachability, systemd logs and browser storage. Do not claim verification was performed.
- Avoid Docker, containers, RDS, Terraform, CI/CD, credentials in repo and paid add-ons. Explain domain and EC2 running costs without inventing amounts.
- If scripts/config files truly simplify deployment, keep them small and give a one-line purpose for each. Do not run destructive commands.

## Acceptance

Documentation provides HTTPS, loopback-only Gunicorn, reboot persistence, Android PWA and resume verification steps. **Deployment and runtime outcomes are unverified**; no AWS changes or command execution.

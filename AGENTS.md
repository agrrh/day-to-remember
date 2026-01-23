## Project Overview

This is a Python application with Docker-based deployment. Key components:
- Telegram bot (`tg_bot.py`) for user interaction
- Scheduler (`tg_schedule.py`) for periodic tasks
- Core logic in `app/` directory with layered architecture
- Docker containerization via `Dockerfile`

## Essential Commands

### Build
```bash
docker build . --progress=plain -f Dockerfile -t local/dev
```

### Run
```bash
docker run --rm -ti --env-file=.env local/dev uv run tg_bot.py
# For scheduler
docker run --rm -ti --env-file=.env local/dev uv run tg_schedule.py
```

### Lint
```bash
uv run ruff check
```

## Code Structure

```
day-to-remember/
├── tg_bot.py              # Main Telegram bot handler
├── tg_schedule.py         # Scheduled tasks for periodic reminders
├── app/                   # Application core
│   ├── use_cases/         # Business logic handlers
│   ├── infrastructure/    # Data access and external adapters
│   ├── domain/            # Core domain models
│   └── dto/               # Data transfer objects
├── Dockerfile             # Container configuration
├── pyproject.toml         # Dependencies and project configuration
└── README.md              # This file
```

## Conventions

- Docker-based deployment with `.env` file for environment variables
- Python project using `uv` as the Python version manager
- Ruff linter configured in `pyproject.toml`

## Testing

- Bot behavior verified through Telegram interaction
- Scheduler functionality validated via container runs
- Unit tests likely exist but not documented in this file

## Gotchas

1. Docker setup is critical - ensure `.env` file is properly configured
2. Linting uses Ruff - run `uv run ruff check` before commits
3. Bot and scheduler run as separate containers
4. No explicit test commands in README - verify through interaction

## Additional Notes

- Follow Conventional Commits standard working with `git`
- Environment variables in `.env` are crucial for API connections
- The project follows a layered architecture pattern

## Issue Tracking

This project uses **bd (beads)** for issue tracking.
Run `bd prime` for workflow context, or install hooks (`bd hooks install`) for auto-injection.

### 🚨 SESSION CLOSE PROTOCOL 🚨

**CRITICAL**: Before saying "done" or "complete", you MUST run this checklist:

```
[ ] 1. git status              (check what changed)
[ ] 2. git add <files>         (stage code changes)
[ ] 3. bd sync                 (commit beads changes)
[ ] 4. git commit -m "."     (commit code)
[ ] 5. bd sync                 (commit any new beads changes)
[ ] 6. git push                (push to remote)
```

**NEVER skip this.** Work is not done until pushed.

### Core Rules
- Track strategic work in beads (multi-session, dependencies, discovered work)
- Use `bd create` for issues, TodoWrite for simple single-session execution
- When in doubt, prefer bd—persistence you don't need beats lost context
- Git workflow: hooks auto-sync, run `bd sync` at session end
- Session management: check `bd ready` for available work

### Essential Commands

#### Finding Work
- `bd ready` - Show issues ready to work (no blockers)
- `bd list --status=open` - All open issues
- `bd list --status=in_progress` - Your active work
- `bd show <id>` - Detailed issue view with dependencies

#### Creating & Updating
- `bd create --title="..." --type=task|bug|feature --priority=2` - New issue
  - Priority: 0-4 or P0-P4 (0=critical, 2=medium, 4=backlog). NOT "high"/"medium"/"low"
- `bd update <id> --status=in_progress` - Claim work
- `bd update <id> --assignee=username` - Assign to someone
- `bd update <id> --title/--description/--notes/--design` - Update fields inline
- `bd close <id>` - Mark complete
- `bd close <id1> <id2> ...` - Close multiple issues at once (more efficient)
- `bd close <id> --reason="explanation"` - Close with reason
- **Tip**: When creating multiple issues/tasks/epics, use parallel subagents for efficiency
- **WARNING**: Do NOT use `bd edit` - it opens $EDITOR (vim/nano) which blocks agents

#### Dependencies & Blocking
- `bd dep add <issue> <depends-on>` - Add dependency (issue depends on depends-on)
- `bd blocked` - Show all blocked issues
- `bd show <id>` - See what's blocking/blocked by this issue

#### Sync & Collaboration
- `bd sync` - Sync with git remote (run at session end)
- `bd sync --status` - Check sync status without syncing

#### Project Health
- `bd stats` - Project statistics (open/closed/blocked counts)
- `bd doctor` - Check for issues (sync problems, missing hooks)

### Common Workflows

**Starting work:**
```bash
bd ready           # Find available work
bd show <id>       # Review issue details
bd update <id> --status=in_progress  # Claim it
```

**Completing work:**
```bash
bd close <id1> <id2> ...    # Close all completed issues at once
bd sync                     # Push to remote
```

**Creating dependent work:**
```bash
# Run bd create commands in parallel (use subagents for many items)
bd create --title="Implement feature X" --type=feature
bd create --title="Write tests for X" --type=task
bd dep add beads-yyy beads-xxx  # Tests depend on Feature (Feature blocks tests)
```

For full workflow details: `bd prime`
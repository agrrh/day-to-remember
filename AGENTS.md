# AGENTS.md

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

- Use `docker inspect` to debug container issues
- Environment variables in `.env` are crucial for API connections
- The project follows a layered architecture pattern
# General Recommendations

These recommendations apply to any project regardless of technology stack.

## Git

- Write clear, descriptive commit messages in the imperative mood
- Keep commits small and focused on a single concern
- Use feature branches and squash merges for pull requests
- Never commit secrets, credentials, or `.env` files
- Keep `.gitignore` up to date

## Documentation

- Keep a `README.md` with setup, run, and deploy instructions
- Document architecture decisions in an `ADR` or `docs/` folder
- Use docstrings/comments for public APIs and complex logic
- Maintain a `CHANGELOG.md` following keepachangelog.com

## Testing

- Write tests alongside features (TDD when possible)
- Aim for meaningful coverage, not 100% for its own sake
- Test behavior, not implementation details
- Use realistic fixtures and avoid mocks when integration tests suffice

## Security

- Validate and sanitize all user input
- Use parameterized queries to prevent injection
- Keep dependencies updated
- Follow the principle of least privilege

## Code Quality

- Keep functions small and single-purpose
- Prefer readability over cleverness
- Avoid deep nesting — early return when possible
- Use meaningful names for variables, functions, and classes
- Eliminate dead code and unused imports

# Bash

## Best Practices

- Use `set -euo pipefail` at the start of scripts
- Quote all variable expansions
- Use `[[ ]]` over `[ ]` for conditionals
- Prefer functions for reusable logic
- Use `shellcheck` to lint scripts
- Use meaningful exit codes

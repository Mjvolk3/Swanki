---
name: atq
description: Show a detailed table of all pending at jobs with their scheduled times and commands.
user_invocable: true
---

# atq -- Scheduled Jobs Dashboard

Show a detailed table of all pending `at` jobs.

**Usage:** `/atq`

## What to do

1. Run `atq` to get pending job IDs and times.
2. If no jobs, print "No scheduled jobs." and stop.
3. For each job, run `at -c <id> | tail -3` to extract the command (skip the env block).
4. Print a markdown table:

```
| Job | Scheduled        | Target                   | Command (truncated)                        |
|-----|------------------|--------------------------|--------------------------------------------|
| 1   | Mar 26 04:00 AM  | dev:exp-test             | ~/mini.../python scripts/...               |
```

- Truncate commands longer than 80 chars with `...`
- Strip the `}` line from `at -c` output
- Parse the tmux target from `send-keys -t "..."` if present and show it as a separate "Target" column

5. Print total count: `N jobs scheduled.`

## Rules

- Read-only -- never modify or cancel jobs
- If `atq` is not available, say so
- Keep output compact

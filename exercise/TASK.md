# Task: do theme entrants outperform?

You have two data files and a starter:

- `membership.csv` — month-end snapshots: `snapshot_date`, `micro_theme`,
  `company_id`. A company is a constituent of a theme on a snapshot date if
  a row exists.
- `prices.csv` — daily closes (trading days only; a company stops appearing
  after it delists).
- `starter.py` — the plumbing is already done: a daily returns matrix and
  `forward_return(company_id, start, n_days) -> (cumulative_return,
  days_used)`. Treat it as correct and build on it.

An **entrant** is a company present in a theme's snapshot that was absent
from that theme's previous snapshot.

**Write a script that answers: over the 63 trading days after a snapshot,
do that snapshot's entrants outperform the theme's incumbents?**

Suggested output: one row per (snapshot_date, micro_theme) with the mean
forward return of entrants, of incumbents, and the spread — plus whatever
aggregate you'd actually look at to answer the question.

Notes:

- Equal-weight within each group.
- State your assumptions out loud as you make them — several details are
  deliberately unspecified.
- Use whatever tools you'd normally use, including AI assistants.
- Finishing is not the goal.

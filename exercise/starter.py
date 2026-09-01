"""Thematic entrants back-test — starter.

The returns plumbing is done for you; treat it as correct. Your work
starts at the TODO. Running this file as-is prints the data shapes, so it
doubles as a check that your environment works.
"""

from pathlib import Path

import pandas as pd

HERE = Path(__file__).parent

membership = pd.read_csv(HERE / "membership.csv", parse_dates=["snapshot_date"])
prices = pd.read_csv(HERE / "prices.csv", parse_dates=["date"])

# Wide matrix of daily simple returns; NaN where a company didn't trade.
_wide = prices.pivot(index="date", columns="company_id", values="close").sort_index()
returns = _wide.pct_change(fill_method=None)


def forward_return(
    company_id: str, start: pd.Timestamp, n_days: int = 63
) -> tuple[float | None, int]:
    """Cumulative simple return over the n_days trading days strictly after
    `start`, returned as (cumulative_return, days_used).

    days_used can be less than n_days if the company stops trading, or the
    sample ends, inside the window — decide for yourself how to treat that.
    Returns (None, 0) if the company has no returns after `start`.
    """
    window = returns.loc[returns.index > start, company_id].dropna().iloc[:n_days]
    if window.empty:
        return None, 0
    return float((1 + window).prod() - 1), int(len(window))


print(f"{len(membership)} membership rows; returns matrix {returns.shape}")

# TODO (see TASK.md): for each (snapshot_date, micro_theme), compare the
# mean forward 63-trading-day return of that snapshot's entrants against
# its incumbents.

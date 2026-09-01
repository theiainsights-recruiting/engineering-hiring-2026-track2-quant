"""Daily equal-weighted return series per major theme.

Runs each morning after the price ingest. Produces the published
theme-return series consumed by the index calculation.
"""

import logging

import pandas as pd

logger = logging.getLogger(__name__)

# Guard against bad vendor prints (unadjusted splits, fat fingers).
CLIP_LOW, CLIP_HIGH = -1.0, 2.0


def daily_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """Wide matrix of daily close-to-close returns.

    prices: long frame of (date, company_id, close), trading days only.
    A company appears from its listing date and stops appearing after it
    delists or is suspended.
    """
    wide = prices.pivot(index="date", columns="company_id", values="close")
    wide = wide.sort_index().ffill()
    rets = wide.pct_change()
    return rets.clip(lower=CLIP_LOW, upper=CLIP_HIGH)


def basket_returns(rets: pd.DataFrame, members: pd.DataFrame) -> pd.DataFrame:
    """Equal-weighted daily return per major theme.

    members: (major_theme, company_id) — current constituents.
    """
    out = []
    for theme, group in members.groupby("major_theme"):
        cols = [c for c in group["company_id"] if c in rets.columns]
        if not cols:
            logger.warning("theme %s has no priced constituents", theme)
            continue
        series = rets[cols].mean(axis=1)
        out.append(
            pd.DataFrame(
                {
                    "date": series.index,
                    "major_theme": theme,
                    "daily_return": series.values,
                }
            )
        )
    return pd.concat(out, ignore_index=True)


def run(price_path: str, members_path: str, output_path: str) -> None:
    prices = pd.read_parquet(price_path)
    members = pd.read_parquet(members_path)
    logger.info(
        "computing returns for %d companies across %d themes",
        members["company_id"].nunique(),
        members["major_theme"].nunique(),
    )
    rets = daily_returns(prices)
    series = basket_returns(rets, members)
    series.to_parquet(output_path, index=False)
    logger.info("wrote %d rows to %s", len(series), output_path)

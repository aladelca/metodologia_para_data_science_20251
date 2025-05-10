"""Feature engineering module for time series data."""
import pandas as pd


def get_lags(df: pd.DataFrame, col: str, date_col: str, n: int) -> pd.DataFrame:
    """Get the lagged values of a DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame to lag.
    col : str
        The column to lag.
    date_col : str
        The date column used to order the lags.
    n : int
        The number of lags to create.

    Returns
    -------
    pd.DataFrame
        A DataFrame with the lagged values.
    """
    df = df.copy()
    df.set_index(date_col, inplace=True)
    df.sort_index(inplace=True)
    for i in range(1, n + 1):
        df[f"lag_{col}_{i}"] = df[col].shift(i)
    return df.reset_index()


def get_rolling_mean(
    df: pd.DataFrame, col: str, date_col: str, window: int
) -> pd.DataFrame:
    """Get the rolling mean of a DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame to calculate the rolling mean.
    col : str
        The column to calculate the rolling mean.
    date_col : str
        The date column.
    window : int
        The window size.

    Returns
    -------
    pd.DataFrame
        A DataFrame with the rolling mean.
    """
    df = df.copy()
    df.set_index(date_col, inplace=True)
    df.sort_index(inplace=True)
    df[f"rolling_mean_{col}"] = df[col].rolling(window=window).mean()
    return df.reset_index()

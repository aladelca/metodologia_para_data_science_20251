"""Test feature engineering module for time series data."""
import pandas as pd
import pytest

from pipeline.feature_engineering import get_lags


@pytest.fixture
def sample_data():
    """Fixture to create a sample DataFrame for testing."""
    data = {
        "date": pd.date_range(start="2023-01-01", periods=5, freq="D"),
        "value": [1, 2, 3, 4, 5],
    }
    return pd.DataFrame(data)


def test_get_lags(sample_data):
    """Test the get_lags function."""
    # Mock the DataFrame
    df = sample_data.copy()

    # Call the function with n=2
    result = get_lags(df, "value", "date", 2)

    # Check the shape of the result
    assert result.shape == (5, 4), "Shape of the result is incorrect"

    # Check the lagged values
    expected_lags = {
        "date": pd.date_range(start="2023-01-01", periods=5, freq="D"),
        "value": [1, 2, 3, 4, 5],
        "lag_value_1": [None, 1.0, 2.0, 3.0, 4.0],
        "lag_value_2": [None, None, 1.0, 2.0, 3.0],
    }

    expected_df = pd.DataFrame(expected_lags)

    pd.testing.assert_frame_equal(result, expected_df)


def test_get_lags_empty_df():
    """Test the get_lags function with an empty DataFrame."""
    # Create an empty DataFrame
    df = pd.DataFrame(columns=["date", "value"])

    # Call the function with n=2
    result_empty = get_lags(df, "value", "date", 2)

    # Check the shape of the result
    assert result_empty.shape == (0, 4), "Shape of the result is incorrect"

    # Check that the result is empty
    assert result_empty.empty, "Result should be empty"

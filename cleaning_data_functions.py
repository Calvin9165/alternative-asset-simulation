import pandas as pd
import matplotlib.pyplot as plt
import pandas_market_calendars as mcal
from datetime import timedelta


def clean_om_funds_from_dataphile(df, remove_cols):

    # set index
    df['Date'] = pd.to_datetime(df['Price Date'], dayfirst=False)
    df.set_index(keys='Date', inplace=True)
    df.sort_index(ascending=True, inplace=True)

    # rename the price column to whatever security we're using
    df.rename({'Last Trade Price': df['CUSIP'][0]}, axis=1, inplace=True)

    # remove all of the excess columns - we can specify which ones we want to remove
    df.drop(labels=remove_cols, axis=1, inplace=True)

    # remove prices with none values (i.e. weekends)
    df.dropna(how='any', axis=0, inplace=True)

    return df


def start_date_finder(dates, how):

    start_date = dates[0]

    if how == 'oldest':

        for date in dates[1:]:
            if date <= start_date:
                start_date = date

    elif how == 'newest':

        for date in dates[1:]:
            if date >= start_date:
                start_date = date

    else:
        return ValueError("Incorrect parameter entry for how parameter, must be 'newest' or 'oldest'")

    return start_date


def end_date_finder(dates, how):
    end_date = dates[0]

    if how == 'oldest':

        for date in dates[1:]:
            if date <= end_date:
                end_date = date

    elif how == 'newest':

        for date in dates[1:]:
            if date >= end_date:
                end_date = date

    else:
        return ValueError("Incorrect parameter entry for how parameter, must be 'newest' or 'oldest'")

    return end_date


def expected_index(df, exchange='nyse'):
    exchange_dates = mcal.get_calendar(name=exchange.upper())

    exchange_dates = exchange_dates.schedule(start_date=df.index[0], end_date=df.index[-1])

    return exchange_dates.index


def clean_str_to_float(df_to_clean, chars_to_remove):
    """
    :param df_to_clean: the pandas DataFrame we want to clean
    :param chars_to_remove: a list of desired characters we want to remove
    :return: a DataFrame with none of the desired characters and each element within the DataFrame converted to float
    """

    # goes through each column present
    for column in df_to_clean.columns:

        # goes through each character present in chars_to_remove
        for character in chars_to_remove:
            # removes characters from data that are present in comm_chars
            df_to_clean[column] = df_to_clean[column].apply(lambda x: str(x).replace(character, ''))

    # convert all columns to float
    return df_to_clean.apply(pd.to_numeric)


def rolling_drawdowns(df):

    drawdown = (df / df.cummax()) - 1

    return drawdown

def cagr(strategy_series, data_freq='calendar'):
    """
    :param strategy_series: float, price or dollar value of strategy/asset/stock we want to measure CAGR for
    :param data_freq: string, the frequency with which the data is produced. This is only taken into account
        if the index of strategy_series are integers
    :return: float, the CAGR over the entire time period for the strategy/asset/stock in question
    """

    # TODO Question to think about: Should we even let the cagr function work if the index provided is not a datetime
    #   index?

    # the number of days used on our denominator 365 for all cases, except data without datetime index
    num_days = timedelta(days=365)

    # beginning and ending value for the strategy/asset/stock in question
    start_val = strategy_series.iloc[0]
    end_val = strategy_series.iloc[-1]

    # if index of series is a datetime index

    print(strategy_series.index.dtype)
    if strategy_series.index.dtype is 'datetime[ns]':

        # period is equal to number of years the strategy has been invested for as a float
        period = (strategy_series.index[-1] - strategy_series.index[0]) / num_days

        return ((end_val / start_val) ** (1 / period)) - 1

    # if index is not a datetime index
    else:

        # if the trading data includes all calendar days
        if data_freq == 'calendar':

            period = (strategy_series.index[-1] - strategy_series.index[0]) / num_days

            return ((end_val / start_val) ** (1 / period)) - 1

        # if the trading data only includes trading days
        elif data_freq == 'trade':

            num_days = 252

            period = (strategy_series.index[-1] - strategy_series.index[0]) / 252

            return ((end_val / start_val) ** (1 / period)) - 1
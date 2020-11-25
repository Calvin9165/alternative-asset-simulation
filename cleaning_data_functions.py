import pandas as pd
import matplotlib.pyplot as plt
import pandas_market_calendars as mcal


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
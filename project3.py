# Nathan Wong 89086268
# Main Module

import API_handler
from indicators import *
from signal_strategies import *

# API KEY: 1MFU2WFQ2FSB419I


def _get_data_in_time_frame(start: str, end: str, info: dict) -> {str: list}:
    """
    Gets the start and end date for analysis and response dictionary
    Filters out the data not in the time frame specified by the user
    Returns a dictionary with data on each field
    """
    # Get the list of data from the dictionary with all historical data on the equity
    info_daily = info['Time Series (Daily)']
    # Get every date in the time frame specified from the user
    all_dates = list(info_daily.keys())

    # Get the index of the end date
    end_index = all_dates.index(start)
    # Get the index of the start date
    start_index = all_dates.index(end)

    dates = []
    opens = []
    highs = []
    lows = []
    closes = []
    volumes = []

    for index in range(end_index, start_index - 1, -1):
        # Iterate through the amount of days in the time frame
        dates.append(all_dates[index])
        opens.append(float(info_daily[all_dates[index]]['1. open']))
        highs.append(float(info_daily[all_dates[index]]['2. high']))
        lows.append(float(info_daily[all_dates[index]]['3. low']))
        closes.append(float(info_daily[all_dates[index]]['4. close']))
        volumes.append(int(info_daily[all_dates[index]]['5. volume']))

    # Return a new dictionary
    return {'date': dates, 'open': opens, 'high': highs, 'low': lows,
            'close': closes, 'volume': volumes, 'indicator': [], 'buy': [], 'sell': []}


def _get_user_indicator_input(user_input: str) -> list:
    """
    Takes the user input as a string and returns it split up as a list
    """
    indicator_type = user_input[:2]
    # The indicator type is the first two characters
    if indicator_type == 'TR':
        # If indicator type is True Range
        input_list = user_input.split(' ')
        return [input_list[0], input_list[1][0], input_list[1][1:], input_list[2][0], input_list[2][1:]]

    elif indicator_type == 'MP' or indicator_type == 'MV':
        # If the indicator type is Simple Moving Average
        input_list = user_input.split(' ')
        return input_list

    elif indicator_type == 'DP' or indicator_type == 'DV':
        # If the indicator type is Directional
        input_list = user_input.split(' ')
        return [input_list[0], input_list[1], input_list[2], input_list[3]]


def _print_report(stock_symbol: str, indicator_type: str, value_dict: {str: list}) -> None:
    """
    Prints a header given the stock symbol, amount of days specified by the user and the indicator chosen
    Prints a header for the table for each category of data
    Prints the final report that contains data on each day in the time frame specified by the user
    """
    # Print the header
    print(stock_symbol)
    print(len(value_dict['date']))
    print(indicator_type)

    indicator_type_list = indicator_type.split(' ')

    # Print header for the table
    print('Date\tOpen\tHigh\tLow\tClose\tVolume\tIndicator\tBuy?\tSell?')

    for i in range(len(value_dict['date'])):
        # Iterate through each day in the time frame
        print('%s' % value_dict['date'][i], end='')
        print('\t%.4f' % value_dict['open'][i], end='')
        print('\t%.4f' % value_dict['high'][i], end='')
        print('\t%.4f' % value_dict['low'][i], end='')
        print('\t%.4f' % value_dict['close'][i], end='')
        print('\t%d' % value_dict['volume'][i], end='')

        if indicator_type_list[0] == 'DP' or indicator_type_list[0] == 'DV':
            # If the indicator type is DP or DV print the indicator as a string
            print('\t%s' % value_dict['indicator'][i], end='')
        else:
            # If not print it as a float to the 0.0000 decimal place
            if not value_dict['indicator'][i]:
                print('\t', end='')
            else:
                print('\t%.4f' % value_dict['indicator'][i], end='')

        print('\t%s' % value_dict['buy'][i], end='')
        print('\t%s' % value_dict['sell'][i])


def _assign_indicator(indicator_type: str, indicator_input_split: list, value_dict: dict) -> list:
    """
    Assigns the correct indicator object given the indicator input from the user
    Assigns the correct signal strategy based on the indicator type
    Return the indicator object and signal strategy as a list
    """
    indicator = None
    signal_strategy = None

    if indicator_type == 'TR':
        # If the indicator type is True Range
        indicator = TrueRange()
        signal_strategy = TrueRangeSignal()

        # Assign values to the attributes of the signal object
        indicator._dates = value_dict['date']
        indicator._closes = value_dict['close']
        indicator._highs = value_dict['high']
        indicator._lows = value_dict['low']

        # Assign values to the attributes of the signal object
        signal_strategy._buy_sign = indicator_input_split[1]
        signal_strategy._buy_threshold = float(indicator_input_split[2])
        signal_strategy._sell_sign = indicator_input_split[3]
        signal_strategy._sell_threshold = float(indicator_input_split[4])

    elif indicator_type == 'MP':
        # If the indicator type is Simple Moving Average calculated with close prices
        indicator = SimpleMovingAverage()
        signal_strategy = SimpleMovingAverageSignal()

        # Assign the number of days for calculation
        indicator._num_days = int(indicator_input_split[1])
        # Assign the list of close prices to the indicator objects
        indicator._closes_or_volumes = value_dict['close']

        # Assign the list of close prices to the signal object
        signal_strategy._closes_or_volumes = value_dict['close']

    elif indicator_type == 'MV':
        # If the indicator type is Simple Moving Average calculated with volumes
        indicator = SimpleMovingAverage()
        signal_strategy = SimpleMovingAverageSignal()

        # Assign the number of days for calculation
        indicator._num_days = int(indicator_input_split[1])
        # Assign the list of volume prices to the indicator objects
        indicator._closes_or_volumes = value_dict['volume']

        # Assign the list of volumes to the signal object
        signal_strategy._closes_or_volumes = value_dict['volume']

    elif indicator_type == 'DP':
        # If the indicator type is Directional calculated with close prices
        indicator = DirectionalIndicator()
        signal_strategy = DirectionalSignal()

        # Assign the number of days for calculation
        indicator._num_days = int(indicator_input_split[1])
        # Assign the list of close prices to the indicator object
        indicator._closes_or_volumes = value_dict['close']

        # Assign the buy and sell threshold to the signal object
        signal_strategy._buy_threshold = int(indicator_input_split[2])
        signal_strategy._sell_threshold = int(indicator_input_split[3])

    elif indicator_type == 'DV':
        # If the indicator type is Directional calculated with volumes
        indicator = DirectionalIndicator()
        signal_strategy = DirectionalSignal()

        # Assign the number of days for calculation
        indicator._num_days = int(indicator_input_split[1])
        # Assign the list of volumes to the indicator object
        indicator._closes_or_volumes = value_dict['volume']

        # Assign the buy and sell threshold to the signal object
        signal_strategy._buy_threshold = int(indicator_input_split[2])
        signal_strategy._sell_threshold = int(indicator_input_split[3])

    # Return the indicator object and signal strategy as a list
    return [indicator, signal_strategy]


def _run_user_interface() -> None:
    """
    Run the user interface and get inputs from the user
    Call all functions to perform calculations and print the final report
    """
    # Get the path to the file containing the API key
    path_to_file = input()
    # Get the partial URL for the Alpha Vantage API
    partial_url = input()
    # Get the symbol associated with the stock
    ticker_symbol = input()
    # Get the start date for analysis
    start_date = input()
    # Get the end date for the analysis
    end_date = input()
    # Get input of indicator and signal strategy
    user_indicator = input()

    # Get response from Alpha Vantage
    api_key = API_handler.get_api_key_from_file(path_to_file)
    url = API_handler.build_url(partial_url, ticker_symbol, api_key)

    # This dictionary contains all historical data about the equity
    response_dict = API_handler.get_results(url)

    # Get the data within the specified time frame
    # This dictionary contains all the data in the specified time frame from the user
    data_dict = _get_data_in_time_frame(start_date, end_date, response_dict)

    # Get the user's input for the indicator and split it into a list
    indicator_input_list = _get_user_indicator_input(user_indicator)
    indicator_type = indicator_input_list[0]

    # Assign the correct indicator object to indicator and correct signal strategy
    indicator = _assign_indicator(indicator_type, indicator_input_list, data_dict)[0]
    signal_strategy = _assign_indicator(indicator_type, indicator_input_list, data_dict)[1]

    # Get the list indicator values
    indicator_value_list = indicator.calculate()

    # Generate the buy and sell signals and update the data dictionary with the indicator values
    # and buy and sell signals
    new_data_dict = signal_strategy.generate_signal(indicator_value_list, data_dict)

    # Print the report
    _print_report(ticker_symbol, user_indicator, new_data_dict)


if __name__ == '__main__':
    _run_user_interface()

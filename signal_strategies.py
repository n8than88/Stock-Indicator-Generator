# Nathan Wong 89086268
# Signal Objects


class TrueRangeSignal:
    def __init__(self):
        """Initialize the attributes used to calculate the True Range"""
        # Buy threshold
        self._buy_sign = ''
        self._buy_threshold = 0
        # Sell threshold
        self._sell_sign = ''
        self._sell_threshold = 0

    def generate_signal(self, indicator_values: [float], value_dict: dict) -> dict:
        """Generate the buy and sell signals based on the indicator calculated for True Range"""
        # Create buy and sell lists
        indexes_to_buy = []
        indexes_to_sell = []

        for i in range(len(indicator_values)):
            if indicator_values[i] == '':
                # If there are no indicator values there are no buy and sell signals
                indexes_to_buy.append('')
                indexes_to_sell.append('')

            else:
                if i > indicator_values.count('')-1:
                    buy_count = 0
                    if self._buy_sign == '>':
                        # If buy sign is greater than
                        if indicator_values[i] > self._buy_threshold:
                            # If the indicator value is greater than the buy threshold
                            indexes_to_buy.append('BUY')
                            buy_count += 1
                    elif self._buy_sign == '<':
                        # If buy sign is less than
                        if indicator_values[i] < self._buy_threshold:
                            # if the indicator value is less than the buy threshold
                            indexes_to_buy.append('BUY')
                            buy_count += 1

                    sell_count = 0
                    if self._sell_sign == '>':
                        # If the sell sign is greater than
                        if indicator_values[i] > self._sell_threshold:
                            # If the indicator value is greater than the sell threshold
                            indexes_to_sell.append('SELL')
                            sell_count += 1
                    elif self._sell_sign == '<':
                        # If the sell sign is less than
                        if indicator_values[i] < self._sell_threshold:
                            # If the indicator value is greater than the sell threshold
                            indexes_to_sell.append('SELL')
                            sell_count += 1

                    # If there are no buy or sell signals generated append empty strings
                    if buy_count == 0:
                        indexes_to_buy.append('')
                    if sell_count == 0:
                        indexes_to_sell.append('')

        # Update the dictionary with indicator values and buy and sell signals
        value_dict['indicator'] = indicator_values
        value_dict['buy'] = indexes_to_buy
        value_dict['sell'] = indexes_to_sell

        # Return the updated dictionary
        return value_dict


class SimpleMovingAverageSignal:
    def __init__(self):
        """Initialize the attributes needed to calculate the Simple Moving Average"""
        # A list for close prices or volume prices depending on the user input
        # MP for close prices and MV for volumes
        self._closes_or_volumes = []

    def generate_signal(self, indicator_values: [float], value_dict: dict) -> dict:
        """
        Generate the buy and sell signals based on the indicator values
        calculated by the simple moving average
        """
        # Create the buy and sell lists to hold the signals
        indexes_to_buy = []
        indexes_to_sell = []

        for i in range(len(indicator_values)):
            # Iterate through the indicator values
            if indicator_values[i] == '':
                # If there is no indicator value there are no buy and sell signals
                indexes_to_buy.append('')
                indexes_to_sell.append('')

            else:
                if i > indicator_values.count(''):
                    if self._closes_or_volumes[i] > indicator_values[i] and \
                            self._closes_or_volumes[i-1] <= indicator_values[i-1]:
                        # If the close price or volume crossed over the indicator value
                        indexes_to_buy.append('BUY')
                        indexes_to_sell.append('')

                    elif self._closes_or_volumes[i] < indicator_values[i] and \
                            self._closes_or_volumes[i-1] >= indicator_values[i-1]:
                        # If the close price or volumes crossed below the indicator value
                        indexes_to_buy.append('')
                        indexes_to_sell.append('SELL')

                    else:
                        # Append empty strings if no buy or sell signal is generated
                        indexes_to_buy.append('')
                        indexes_to_sell.append('')

                else:
                    indexes_to_buy.append('')
                    indexes_to_sell.append('')

        # Update the dictionary with the indicator values and buy and sell signals
        value_dict['indicator'] = indicator_values
        value_dict['buy'] = indexes_to_buy
        value_dict['sell'] = indexes_to_sell

        # Return the updated dictionary
        return value_dict


class DirectionalSignal:
    def __init__(self):
        """
        Initialize the attributes buy and sell threshold to calculate
         buy and sell signals for Directional indicators
         """
        self._buy_threshold = 0
        self._sell_threshold = 0

    def generate_signal(self, indicator_values: [str], value_dict: dict) -> dict:
        """Generate buy and sell signals for directional indicators"""
        # Create lists to store buy and sell signals
        indexes_to_buy = []
        indexes_to_sell = []

        for i in range(len(indicator_values)):
            # Iterate through all the indicators
            if i == 0:
                # If it is the first index append empty strings
                indexes_to_buy.append('')
                indexes_to_sell.append('')

            else:
                buy_count = 0
                sell_count = 0

                if int(indicator_values[i]) > self._buy_threshold >= int(indicator_values[i-1]):
                    # If the indicator value crossed over the buy threshold
                    indexes_to_buy.append('BUY')
                    buy_count += 1
                elif int(indicator_values[i]) < self._sell_threshold <= int(indicator_values[i-1]):
                    # If the indicator value crossed over the sell threshold
                    indexes_to_sell.append('SELL')
                    sell_count += 1

                if buy_count == 0:
                    # If there are no buy signals generated append an empty string
                    indexes_to_buy.append('')
                if sell_count == 0:
                    # If there are no sell signals generated append a empty string
                    indexes_to_sell.append('')

        # Update the dictionary with the indicator values and buy and sell signals generated
        value_dict['indicator'] = indicator_values
        value_dict['buy'] = indexes_to_buy
        value_dict['sell'] = indexes_to_sell

        # Return the updated dictionary
        return value_dict

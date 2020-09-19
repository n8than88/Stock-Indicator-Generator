# Nathan Wong 89086268
# Indicator objects


class TrueRange:
    def __init__(self):
        """Initialize the attributes needed for calculating the True Range"""
        self._dates = []
        self._closes = []
        self._highs = []
        self._lows = []

    def calculate(self) -> [float]:
        """
        Calculate the indicator values given a dictionary of all the data in the time frame
        Return a list of floats which represent all the indicator values
        Called when user inputs TR
        """
        # Create the indicator list
        indicator_value_list = []

        for i in range(len(self._dates)):
            # Iterate through every date in the time frame
            if i > 0:
                # The first day has no indicator value
                # Calculate the True Range for the current day
                if self._closes[i-1] > self._highs[i]:
                    # If the previous day close is greater than today's high
                    true_range = (self._closes[i-1] - self._lows[i]) / self._closes[i-1]

                elif self._closes[i-1] < self._lows[i]:
                    # If previous day close is less than today's low
                    true_range = (self._highs[i] - self._closes[i-1]) / self._closes[i-1]

                else:
                    true_range = (self._highs[i] - self._lows[i]) / self._closes[i-1]

                # Multiply by 100 to get the percentage
                indicator_value_list.append(true_range * 100)

            else:
                # If its the first day in the time frame append an empty string
                indicator_value_list.append('')

        # Return the list of indicators
        return indicator_value_list


class SimpleMovingAverage:
    def __init__(self):
        """When initiated create the _num_days attribute"""
        self._num_days = 0
        self._closes_or_volumes = []

    def calculate(self) -> [float]:
        """
        Calculate the indicator values given a list of close prices or volumes
        Returns a list of floats which represent all the indicator values of the data
        Called when user inputs MP or MV
        """
        # Create a list to store indicator values
        # Create a temporary list for calculation
        indicator_value_list = []
        temp_list = []

        for i in range(len(self._closes_or_volumes)):
            # Loop through every day in the time frame
            if i < self._num_days - 1:
                # Append 0 to indicator_value_list if N days has not been reached
                indicator_value_list.append('')

            # Append the close / volume value to temp_list
            temp_list.append(self._closes_or_volumes[i])

            if len(temp_list) == self._num_days:
                # After reaching N days add the values in temp list up and divide by N days to get
                # simple moving average for N days
                indicator_value_list.append(sum(temp_list) / self._num_days)
                temp_list.pop(0)

        return indicator_value_list


class DirectionalIndicator:
    def __init__(self):
        """Create the _num_days attribute when initialized"""
        self._num_days = 0
        self._closes_or_volumes = []

    def calculate(self) -> [str]:
        """
        Calculate the indicator values given a list of close prices or volumes
        Returns a list of strings representing the indicator values of the time frame
        Each indicator value can be an integer with a symbol in front such as + or -
        Called when user inputs DP or DV
        """
        # Create a list to store indicator values
        indicator_value_list = []

        for i in range(len(self._closes_or_volumes)):
            # Loop through every day in the time frame
            if i == 0:
                # If it is the first day no previous days to compare to
                indicator_value_list.append('0')

            else:
                days_greater = 0
                days_lower = 0

                if i < self._num_days:
                    # If i is still less than the number of days specified by the user then calculate
                    # the value with the days available
                    for j in range(1, i+1):
                        # Loop through the days available
                        if self._closes_or_volumes[j] > self._closes_or_volumes[j-1]:
                            # If the current day's close price is greater than previous day's then
                            # add one to days greater
                            days_greater += 1
                        else:
                            days_lower += 1
                else:
                    # If there are more than N days specified by the user
                    for j in range(i+1-self._num_days, i+1):
                        # Loop through the past N days
                        if self._closes_or_volumes[j] > self._closes_or_volumes[j-1]:
                            # If the current day's close price is greater than yesterday's close price
                            days_greater += 1
                        else:
                            days_lower += 1

                # Calculate the directional indicator
                directional_indicator = days_greater - days_lower

                if directional_indicator > 0:
                    # If the value is positive add a + sign to the front and change type to string
                    directional_indicator = '+' + str(directional_indicator)
                elif directional_indicator < 0:
                    # If it is negative just change the type to a string
                    directional_indicator = str(directional_indicator)
                else:
                    # If it is 0 change it to a string
                    directional_indicator = str(directional_indicator)

                # Append the value to the list
                indicator_value_list.append(directional_indicator)

        # Return the list of indicators for the data
        return indicator_value_list

# Nathan Wong 89086268
# API handler

import json
import urllib.parse
import urllib.request
from pathlib import Path
from urllib import error


# API KEY: 1MFU2WFQ2FSB419I

class StatusCodeError(Exception):
    pass


class FormatError(Exception):
    pass


def build_url(base_url: str, ticker_symbol: str, api_key: str) -> str:
    """Builds a URL given the base url, stock symbol and the api key and returns it"""
    query_parameters = [
        ('function', 'TIME_SERIES_DAILY'), ('symbol', ticker_symbol),
        ('outputsize', 'full'), ('apikey', api_key)
    ]
    # TIME_SERIES_DAILY gives the daily time series of the equity
    # Get the stock symbol from the user
    # Output size to full to get all historical data
    # Api key from alpha vantage

    # Return the url with the query parameters added to it
    return base_url + '/query?' + urllib.parse.urlencode(query_parameters)


def get_results(url: str) -> dict:
    """Takes a url and returns a Python dictionary that represents the parsed JSON response"""
    response = None
    status_code = 0

    try:
        # Open the url and get the response
        response = urllib.request.urlopen(url)

        # Get the HTTPS status code
        status_code = response.getcode()

        if status_code != 200:
            raise StatusCodeError

        # Decode the response into JSON text
        json_text = response.read().decode(encoding='utf-8')

        # Parse the response
        parsed_response = json.loads(json_text)

        # Check if Meta Data and Time Series are the attributes in the parsed response
        attributes = list(parsed_response.keys())
        if attributes != ['Meta Data', 'Time Series (Daily)']:
            raise FormatError

        # Check the attributes in Meta Data
        if not _check_meta_data_attributes(parsed_response):
            raise FormatError

        # Check the attributes in every date in Time Series (Daily)
        if not _check_time_series_attributes(parsed_response):
            raise FormatError

        # Return the parsed JSON response
        return parsed_response

    except json.decoder.JSONDecodeError:
        # If the response sent is not compatible
        print('FAILED')
        print(status_code)
        print('FORMAT')
        exit()

    except StatusCodeError:
        # If the status code is not 200
        print('FAILED')
        print(status_code)
        print('NOT 200')
        exit()

    except FormatError:
        # If there are missing attributes or the response is empty
        print('FAILED')
        print(status_code)
        print('FORMAT')
        exit()

    except urllib.error.HTTPError as CodeError:
        # If the status code is not 200 and can't connect
        print('FAILED')
        print(CodeError.code)
        print('NOT 200')
        exit()

    except urllib.error.URLError:
        # If there is no network connectivity and a API request couldn't be sent at all
        print('FAILED')
        print(0)
        print('NETWORK')
        exit()

    finally:
        # Close the response when done
        if response is not None:
            response.close()


def _check_meta_data_attributes(parsed_response: dict):
    """
    Check the attributes in Meta Data
    If there are missing attributes return False
    """
    # All the attributes in Meta Data should match this list
    meta_data_attribute_list = ['1. Information', '2. Symbol', '3. Last Refreshed', '4. Output Size',
                                '5. Time Zone']
    if list(parsed_response['Meta Data'].keys()) != meta_data_attribute_list:
        # If the attributes don't match return False
        return False
    else:
        # If the attributes are the same
        return True


def _check_time_series_attributes(parsed_response: dict) -> bool:
    """
    Check every attribute for every date in the data sent from Alpha Vantage
    """
    # Attributes in each date should match this list
    time_series_attribute_list = ['1. open', '2. high', '3. low', '4. close', '5. volume']
    # Dictionary of all the data in Time Series (Daily)
    info_dict = parsed_response['Time Series (Daily)']
    # Every date returned in Time Series (Daily)
    dates = list(parsed_response['Time Series (Daily)'].keys())

    for date in dates:
        # Check that each date has the required attributes
        if list(info_dict[date].keys()) != time_series_attribute_list:
            # If one attributes is missing from anywhere return False
            return False

    # If all the attributes are there return True
    return True


def get_api_key_from_file(path: str) -> str:
    """Read a text file containing the api key and return it"""
    file_path = Path(path)
    # Open the file for reading
    f = file_path.open('r')

    # Read the first line of the file to get the api key
    api_key = f.readline()
    # Close the file when done
    f.close()

    # Return the api key read from the file
    return api_key

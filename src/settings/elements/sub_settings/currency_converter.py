import requests
import json

class ExchangeRates:
    url = "https://api.coingecko.com/api/v3/exchange_rates"
    """
    A class to fetch, save, update, and manage exchange rates from CoinGecko API.

    Attributes:
        data_file (str): The name of the JSON file to save exchange rates data.
        rates (dict): The exchange rates data.

    Methods:
        get_exchange_rates(): Fetches exchange rates from CoinGecko API.
        save_to_json(): Saves the current exchange rates to a JSON file.
        update_data(): Updates the exchange rates and saves the new data to the JSON file.
        convert_currency(amount, from_currency, to_currency): Converts an amount from one currency to another.
        get_number_of_currencies(): Returns the number of fiat currencies.
        get_number_of_cryptos(): Returns the number of cryptocurrencies.
        get_number_of_commodities(): Returns the number of commodities.
        get_lists(): Returns a dictionary with lists of fiat currencies, cryptocurrencies, and commodities along with their values.
    """

    def __init__(self, data_file:str, load_from_file:bool = False):
        """
        Initializes the ExchangeRates class, fetches the exchange rates, and saves them to a JSON file.
        
        Parameters:
            data_file (str): The name of the JSON file(with location) to save exchange rates data.
            load_from_file (str): Load data from json file or load it from api call. Default is False.
        """
        self.data_file = data_file

        if load_from_file:
            with open(self.data_file, 'r') as json_file_with_exchange_rates:
                self.rates = json.load(json_file_with_exchange_rates)
            return
        
        self.rates = self.get_exchange_rates()
        self.save_to_json()

    def get_exchange_rates(self):
        """
        Fetches exchange rates from the CoinGecko API.
        
        Returns:
            dict: The exchange rates data.
        
        Raises:
            RuntimeError: If the API request fails.
        """
        response = requests.get(self.url)
        
        if response.status_code == 200:
            data = response.json()
            return data['rates']
        else:
            raise RuntimeError("Failed to fetch exchange rates")

    def save_to_json(self):
        """
        Saves the current exchange rates to a JSON file.
        """
        with open(self.data_file, 'w') as f:
            json.dump(self.rates, f, indent=4)

    def update_data(self):
        """
        Updates the exchange rates and saves the new data to the JSON file.
        """
        self.rates = self.get_exchange_rates()
        self.save_to_json()

    def convert_currency(self, amount, from_currency, to_currency):
        """
        Converts an amount from one currency to another using the current exchange rates.
        
        Parameters:
            amount (float): The amount to convert.
            from_currency (str): The currency code to convert from.
            to_currency (str): The currency code to convert to.
        
        Returns:
            float: The converted amount.
        
        Raises:
            ValueError: If the currency codes are not found in the exchange rates.
        """
        if from_currency in self.rates and to_currency in self.rates:
            from_rate = self.rates[from_currency]['value']
            to_rate = self.rates[to_currency]['value']
            converted_amount = (amount / from_rate) * to_rate
            return converted_amount
        else:
            raise ValueError(f"Currency {from_currency} or {to_currency} not found in rates")

    def get_number_of_currencies(self):
        """
        Returns the number of fiat currencies.
        
        Returns:
            int: The number of fiat currencies.
        """
        return sum(1 for rate in self.rates.values() if rate['type'] == 'fiat')

    def get_number_of_cryptos(self):
        """
        Returns the number of cryptocurrencies.
        
        Returns:
            int: The number of cryptocurrencies.
        """
        return sum(1 for rate in self.rates.values() if rate['type'] == 'crypto')

    def get_number_of_commodities(self):
        """
        Returns the number of commodities.
        
        Returns:
            int: The number of commodities.
        """
        return sum(1 for rate in self.rates.values() if rate['type'] == 'commodity')

    def get_lists(self):
        """
        Returns a dictionary with lists of fiat currencies, cryptocurrencies, and commodities along with their values.
        
        Returns:
            dict: A dictionary with keys 'currencies', 'cryptos', and 'commodities', each containing a list of exchange rates.
        """
        currencies = {code: rate for code, rate in self.rates.items() if rate['type'] == 'fiat'}
        cryptos = {code: rate for code, rate in self.rates.items() if rate['type'] == 'crypto'}
        commodities = {code: rate for code, rate in self.rates.items() if rate['type'] == 'commodity'}

        return {
            'currencies': dict(sorted(currencies.items())),
            'cryptos': dict(sorted(cryptos.items())),
            'commodities': dict(sorted(commodities.items()))
        }

if __name__ == "__main__":
    exchange = ExchangeRates()

    # conversions
    amount_in_inr = 1000  # Amount in INR
    converted_to_usd = exchange.convert_currency(amount_in_inr, 'inr', 'usd')
    print(f"{amount_in_inr} INR is equal to {converted_to_usd} USD")

    amount_in_usd = 100  # Amount in USD
    converted_to_btc = exchange.convert_currency(amount_in_usd, 'usd', 'btc')
    print(f"{amount_in_usd} USD is equal to {converted_to_btc} BTC")

    amount_in_btc = 0.01  # Amount in BTC
    converted_to_eth = exchange.convert_currency(amount_in_btc, 'btc', 'eth')
    print(f"{amount_in_btc} BTC is equal to {converted_to_eth} ETH")

    # Update data and get counts
    exchange.update_data()
    print(f"Number of fiat currencies: {exchange.get_number_of_currencies()}")
    print(f"Number of cryptocurrencies: {exchange.get_number_of_cryptos()}")
    print(f"Number of commodities: {exchange.get_number_of_commodities()}")

    # # Get lists of currencies, cryptos, and commodities
    # lists = exchange.get_lists()
    # print("Fiat Currencies:", lists['currencies'])
    # print("Cryptocurrencies:", lists['cryptos'])
    # print("Commodities:", lists['commodities'])

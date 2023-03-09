import requests
import time

# Using random UK octopus energy tariff, until suitable Polish alternative is available
OCTOPUS_ENERGY_API_URL = "https://api.octopus.energy/v1/products/AGILE-FLEX-22-11-25/electricity-tariffs/E-1R-AGILE" \
                         "-FLEX-22-11-25-C/standard-unit-rates/"
ENERGY_PRICES_API = 'http://127.0.0.1:8000/energy_price_api/v1/energy_prices/'
ENERGY_PRICES_API_LAST_ENTRY = 'http://127.0.0.1:8000/energy_price_api/v1/energy_prices/last_entry/'

MAX_CALLS = 15


def api_call(url, method, data=None):
    if data is None:
        data = {}
    print('Calling an API')
    call_count = 0

    while call_count <= MAX_CALLS:
        success = False
        if call_count == MAX_CALLS:
            raise SystemExit('API max calls exceeded')

        try:

            if method == 'GET':
                response = requests.get(url, timeout=5)
                response.raise_for_status()
                print(response.status_code)
                if response.status_code == 200:
                    success = True
                    print(response.json())
                    return response.json()
            if method == 'POST':
                response = requests.post(url, data=data)
                response.raise_for_status()
                print(response.status_code)
                if response.status_code == 201:
                    success = True

        except requests.exceptions.HTTPError as erra:
            print(erra)
            time.sleep(2 ** call_count)
            call_count += 1

        except requests.exceptions.ConnectionError as errb:
            print(errb)
            time.sleep(2 ** call_count)
            call_count += 1

        except requests.exceptions.Timeout as errc:
            print(errc)
            time.sleep(2 ** call_count)
            call_count += 1

        except requests.exceptions.RequestException as error:
            raise SystemExit('API Request error: ' + str(error)) from error

        if success:
            print('API request successful, status ' + str(response.status_code) + '.')
            break


def data_cleaning(item):
    item.pop('value_exc_vat')
    rounded_value = round(item['value_inc_vat'], 3)
    item['value_inc_vat'] = rounded_value
    return item


def get_energy_prices():
    return api_call(OCTOPUS_ENERGY_API_URL, 'GET')


def get_energy_prices_last_entry():
    return api_call(ENERGY_PRICES_API_LAST_ENTRY, 'GET')


def get_cleaned_data(data):
    last_entry = get_energy_prices_last_entry()
    return [data_cleaning(item) for item in data['results'] if item['valid_from'] > last_entry['valid_to']]


cleaned_data = get_cleaned_data(get_energy_prices())

for result in cleaned_data:
    api_call(ENERGY_PRICES_API, 'POST', result)

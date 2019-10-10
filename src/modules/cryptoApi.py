import requests
from binance.client import Client
from web3 import Web3, HTTPProvider
from money import Money


COINMARKETCAP_API_KEY = ''

BINANCE_API_KEY = ''
BINANCE_API_SECRET = ''

ETH_BLOCKCHAIN_CONNECTION = ""


def get_coin_market_cap_value_euro(symbol, currency):
    try:
        json_response = get_coin_market_cap_data(symbol, currency)
        if json_response['status']['error_code'] == 400:
            return 0

        return json_response['data'][symbol.upper()]['quote'][currency.upper()]['price']
    except Exception as e:
        print(e)
        raise e


def get_coin_market_cap_data(symbol, currency):
    try:
        response = requests.get(
            'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest',
            params={
                'symbol': symbol.upper(),
                'convert': currency.upper(),
                'aux': 'num_market_pairs,cmc_rank,date_added,tags,platform,max_supply,circulating_supply,total_supply,market_cap_by_total_supply,volume_24h_reported,volume_7d,volume_7d_reported,volume_30d,volume_30d_reported'
            },
            headers={
                'Accepts': 'application/json',
                'X-CMC_PRO_API_KEY': COINMARKETCAP_API_KEY,
            },
        )
        return response.json()
    except Exception as e:
        print(e)
        raise e


def get_binance_wallet_value(currency):
    try:
        client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)
        info = client.get_account()
        wallet = {
            'walletValue': {
                'FIAT': currency.upper(),
                'totalString': '',
                'total': 0.00
            },
            'assets': list()
        }

        for coin in info['balances']:
            coin_free = float(coin['free'])
            coin_locked = float(coin['locked'])

            if coin_free > 0 or coin_locked > 0:
                price = get_coin_market_cap_value_euro(coin['asset'], currency)
                amount = coin_free + coin_locked
                value = price * amount
                if value > 0.01:
                    wallet['walletValue']['total'] += value
                    wallet['assets'].append(
                        {
                            'asset': coin['asset'],
                            'amount': '%.2f' % amount,
                            'FIAT': currency.upper(),
                            currency.upper() + "/" + coin['asset']: '%.2f' % price,
                            'value': '%.2f' % value
                        }
                    )
        wallet['walletValue']['totalString'] = str(Money(wallet['walletValue']['total'], currency.upper()))
        return wallet
    except Exception as e:
        print(e)
        raise e


def get_eth_address_balance_from_blockchain(currency, address):
    try:
        w3 = Web3(HTTPProvider(ETH_BLOCKCHAIN_CONNECTION))
        connected = w3.isConnected()
        if connected:
            try:
                eth_balance = float(w3.fromWei(w3.eth.getBalance(address), 'ether'))
            except Exception:
                check_sum_address = w3.toChecksumAddress(address)
                eth_balance = float(w3.fromWei(w3.eth.getBalance(check_sum_address), 'ether'))
            eth_price = get_coin_market_cap_value_euro('ETH', currency.upper())
            wallet = {
                        'asset': 'ETH',
                        'amount': '%.2f' % eth_balance,
                        'FIAT': currency.upper(),
                        currency.upper() + "/" + 'ETH': '%.2f' % eth_price,
                        'value': '%.2f' % (eth_price * eth_balance)
                    }

            return wallet
        else:
            return False
    except Exception as e:
        print(e)
        raise e
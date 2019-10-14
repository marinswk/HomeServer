import requests
from binance.client import Client
from web3 import Web3, HTTPProvider
from money import Money
from src.modules.db_operations import get_crypto_wallet_config_by_key, get_manual_assets, get_eth_addresses


def get_coin_market_cap_value_euro(symbol, currency):
    try:
        coin_data = get_coin_market_cap_data(symbol, currency)

        if coin_data['status']['error_code'] == 400:
            return 0
        coin_id = str(coin_data['data'][symbol.upper()]['id'])
        coin_metadata = get_coin_market_cap_metadata(coin_id)
        return {
            'id': coin_id,
            'price': coin_data['data'][symbol.upper()]['quote'][currency.upper()]['price'],
            'logo': coin_metadata['data'][coin_id]['logo']
        }
    except Exception as e:
        print(e)
        return False


def get_coin_market_cap_data(symbol, currency):
    try:
        COINMARKETCAP_API_KEY = get_crypto_wallet_config_by_key('COINMARKETCAP_API_KEY')

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


def get_coin_market_cap_metadata(coin_id):
    try:
        COINMARKETCAP_API_KEY = get_crypto_wallet_config_by_key('COINMARKETCAP_API_KEY')
        response = requests.get(
            'https://pro-api.coinmarketcap.com/v1/cryptocurrency/info',
            params={
                'id': coin_id,
                'aux': 'urls,logo,description,tags,platform,date_added,notice,status'
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
        BINANCE_API_KEY = get_crypto_wallet_config_by_key('BINANCE_API_KEY')
        BINANCE_API_SECRET = get_crypto_wallet_config_by_key('BINANCE_API_SECRET')

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
                coin_data = get_coin_market_cap_value_euro(coin['asset'], currency)
                if coin_data:
                    amount = coin_free + coin_locked
                    value = coin_data['price'] * amount
                    if value > 1:
                        wallet['walletValue']['total'] += value
                        wallet['assets'].append(
                            {
                                'asset': coin['asset'],
                                'amount': '%.2f' % amount,
                                'FIAT': currency.upper(),
                                'pairValue': '%.2f' % coin_data['price'],
                                'value': '%.2f' % value,
                                'logo': coin_data['logo'],
                                'exchange': 'Binance'
                            }
                        )
        wallet['walletValue']['totalString'] = str(Money(wallet['walletValue']['total'], currency.upper()))
        return wallet
    except Exception as e:
        print(e)
        raise e


def get_eth_address_balance_from_blockchain(currency):
    try:
        ETH_BLOCKCHAIN_CONNECTION = get_crypto_wallet_config_by_key('ETH_BLOCKCHAIN_CONNECTION')
        w3 = Web3(HTTPProvider(ETH_BLOCKCHAIN_CONNECTION))
        connected = w3.isConnected()

        wallet = {
            'walletValue': {
                'FIAT': currency.upper(),
                'totalString': '',
                'total': 0.00
            },
            'assets': list()
        }

        if connected:
            eth_data = get_eth_addresses()

            for eth in eth_data:
                try:
                    eth_balance = float(w3.fromWei(w3.eth.getBalance(eth.address), 'ether'))
                except Exception:
                    check_sum_address = w3.toChecksumAddress(eth.address)
                    eth_balance = float(w3.fromWei(w3.eth.getBalance(check_sum_address), 'ether'))

                coin_data = get_coin_market_cap_value_euro('ETH', currency.upper())
                if coin_data:
                    value = coin_data['price'] * eth_balance

                    if value > 1:
                        wallet['walletValue']['total'] += value
                        wallet['assets'].append(
                            {
                                'asset': 'ETH',
                                'amount': '%.2f' % eth_balance,
                                'FIAT': currency.upper(),
                                'pairValue': '%.2f' % coin_data['price'],
                                'value': '%.2f' % value,
                                'logo': coin_data['logo'],
                                'exchange': eth.exchange
                            }
                        )
            wallet['walletValue']['totalString'] = str(Money(wallet['walletValue']['total'], currency.upper()))
            return wallet

        else:
            return False
    except Exception as e:
        print(e)
        raise e


def get_manual_assets_wallet(currency):
    try:
        manual_assets = get_manual_assets()

        wallet = {
            'walletValue': {
                'FIAT': currency.upper(),
                'totalString': '',
                'total': 0.00
            },
            'assets': list()
        }

        for coin in manual_assets:

            coin_data = get_coin_market_cap_value_euro(coin.asset, currency.upper())
            if coin_data:
                amount = coin.amount
                value = coin_data['price'] * amount
                if value > 1:
                    wallet['walletValue']['total'] += value
                    wallet['assets'].append(
                        {
                            'asset': coin.asset,
                            'amount': '%.2f' % amount,
                            'FIAT': currency.upper(),
                            'pairValue': '%.2f' % coin_data['price'],
                            'value': '%.2f' % value,
                            'logo': coin_data['logo'],
                            'exchange': coin.exchange
                        }
                    )
        wallet['walletValue']['totalString'] = str(Money(wallet['walletValue']['total'], currency.upper()))
        return wallet

    except Exception as e:
        print(e)
        raise e


def get_total_wallet(currency):
    try:
        wallet = {
            'walletValue': {
                'FIAT': currency.upper(),
                'totalString': '',
                'total': 0.00
            },
            'assets': list()
        }

        binance_wallet = get_binance_wallet_value(currency)
        eth_wallet = get_eth_address_balance_from_blockchain(currency)
        manual_wallet = get_manual_assets_wallet(currency)

        wallet['assets'].extend(
            binance_wallet['assets']
        )
        wallet['assets'].extend(
            eth_wallet['assets']
        )
        wallet['assets'].extend(
            manual_wallet['assets']
        )

        wallet['walletValue']['total'] = binance_wallet['walletValue']['total'] + \
            eth_wallet['walletValue']['total'] + manual_wallet['walletValue']['total']
        wallet['walletValue']['totalString'] = str(Money(wallet['walletValue']['total'], currency.upper()))

        return wallet
    except Exception as e:
        print(e)
        raise e
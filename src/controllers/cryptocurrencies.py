from flask import Blueprint, render_template
import json
from src.modules import cryptoApi

crypto_endpoints = Blueprint('crypto_endpoints', __name__, template_folder='templates')


@crypto_endpoints.route('/quotes/<string:symbol>/<string:currency>', methods=['GET'])
def get_quotes(symbol, currency):
    try:
        json_response = cryptoApi.get_coin_market_cap_data(symbol, currency)
        return json.dumps(json_response)
    except Exception as e:
        print(e)


@crypto_endpoints.route('/binance/wallet/<string:currency>', methods=['GET'])
def get_binance_wallet(currency):
    try:
        wallet = cryptoApi.get_binance_wallet_value(currency)
        return render_template('wallet.html', total=wallet['walletValue'], assets=wallet['assets'],
                               title='Binance Wallet')
    except Exception as e:
        print(e)


@crypto_endpoints.route('/manual/wallet/<string:currency>', methods=['GET'])
def get_manual_wallet(currency):
    try:
        wallet = cryptoApi.get_manual_assets_wallet(currency)
        return render_template('wallet.html', total=wallet['walletValue'], assets=wallet['assets'],
                               title='Manual Assets Wallet')
    except Exception as e:
        print(e)


@crypto_endpoints.route('/eth/wallet/<string:currency>', methods=['GET'])
def get_eth_address_balance(currency):
    try:
        wallet = cryptoApi.get_eth_address_balance_from_blockchain(currency)
        if wallet:
            return render_template('wallet.html', total=wallet['walletValue'], assets=wallet['assets'],
                                   title='ETH Addresses Wallet')
        else:
            return "There was a problem retrieving the ETH address balance"
    except Exception as e:
        print(e)


@crypto_endpoints.route('/wallet/<string:currency>', methods=['GET'])
def get_wallet(currency):
    try:
        wallet = cryptoApi.get_total_wallet(currency)
        return render_template('wallet.html', total=wallet['walletValue'], assets=wallet['assets'], title='Wallet')
    except Exception as e:
        print(e)
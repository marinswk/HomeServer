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
        return json.dumps(wallet)
    except Exception as e:
        print(e)


@crypto_endpoints.route('/eth/balance/<string:currency>/<string:address>', methods=['GET'])
def get_eth_address_balance(currency, address):
    try:
        wallet = cryptoApi.get_eth_address_balance_from_blockchain(currency, address)
        if wallet:
            return json.dumps(wallet)
        else:
            return "There was a problem retrieving the ETH address balance"
    except Exception as e:
        print(e)
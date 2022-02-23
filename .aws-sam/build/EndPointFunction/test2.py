# This example uses Python 2.7 and the python-request library.
from asyncio.constants import LOG_THRESHOLD_FOR_CONNLOST_WRITES
from inspect import Parameter
import os
from symtable import Symbol
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

import Receive


"""
APIを消してからデプロイすること！！！！！
"""

coin_market_api = os.getenv('COIN_MARKET_API')
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': coin_market_api,
}


# 子クラスからシンボル名を受け取り処理、通貨名と価格をobjectで返す
class CryptSymbolObject(object):

    # 入力値を全て大文字に変更(symbolが全て大文字である必要があるため)
    def capital_upper(self, *words):
        self.words = words
        list_upperd = []
        for word in words:
            word_upperd = word.upper()
            list_upperd.append(word_upperd)
        return list_upperd

    # 入力値を全て小文字に変更(nameが全て小文字である必要があるため)
    def lower_case(self, symbol):
        self.symbol = symbol
        lower_symbol = symbol.lower()
        return lower_symbol

    # symbol名を受け取って通貨名と金額を返す
    def receive_symbol(self, *crypt):

        # output Key: 通貨名　value: 価格
        output = {}
        # CoinMarketのテンプレ
        url = 'https://pro-api.coinmarketcap.com/v1/tools/price-conversion'
        upperd_crypt = self.capital_upper(*crypt)
        for symbol in upperd_crypt:
            parameters = {
                'amount': '1',
                'symbol': symbol,
                'convert': 'JPY',
            }
            session = Session()
            session.headers.update(headers)

            try:
                response = session.get(url, params=parameters)
                print(response)
                data = json.loads(response.text)
                output[data['data']['name']
                       ] = data['data']['quote']['JPY']['price']

            except (ConnectionError, Timeout, TooManyRedirects, KeyError) as e:
                output[symbol] = 0.000
                print(output)
        return output


# 仮想通貨名を受け取り、名前とシンボルで処理を分ける、シンボルを親クラスへ渡す
class CryptNameObject(CryptSymbolObject):

    # 通貨名を受け取ってsymbolを返す
    def receive_name(self, crypt):
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
        lower_crypt = self.lower_case(crypt)
        count = 0
        output = {}
        symbol_list = []
        received_lists = Receive.separate_word.split_each(lower_crypt)
        for received_list in received_lists:
            try:
                count += 1
                parameters = {
                    'slug': received_list,
                    'convert': 'JPY',
                }
                session = Session()
                session.headers.update(headers)
                responese = session.get(url, params=parameters)
                print(responese)
                data = json.loads(responese.text)
                # idに各通貨のID(番号)を値として取得する
                id = list(data['data'].keys())[0]
                output[data['data'][id]['name']
                       ] = data['data'][id]['quote']['JPY']['price']

            except (ConnectionError, Timeout, TooManyRedirects, KeyError, TypeError) as e:
                print(e)
                # symbolで入力された場合、その値だけsymbol_listにデータを入れておく
                x = received_lists[count - 1]
                symbol_list.append(x)
        # symbolデータだけををreceive_symbolに渡しす
        symbol_data = self.receive_symbol(*symbol_list)
        # symbolのデータとoutputを合体させる
        output.update(symbol_data)
        return output


crypt_symbol_object = CryptSymbolObject()
crypt_name_object = CryptNameObject()

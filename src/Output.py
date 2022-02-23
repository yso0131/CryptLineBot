import CoinMarket


# タプルで渡されるので*をつけて情報を展開

class Output(object):

    def output_value(self, word):
        self.word = word
        return_sentense = []
        input_text = CoinMarket.crypt_name_object.receive_name(word)
        for k, v in input_text.items():
            comma_price = "{:.2f}".format(v)
            str_cut_num = str(comma_price)
            sentense = k + 'の価格は' + str_cut_num + '円です。\n'
            return_sentense.append(sentense)
            response = ''.join(return_sentense)
        return response.rstrip('\r\n')


output = Output()

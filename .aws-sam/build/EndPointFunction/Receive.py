"""一括入力の際にスペースで区切り、リスト型に変換する"""


class SeparateWord(object):

    def split_each(self, word):
        self.word = word
        list = word.split()
        each_list = []
        for each in list:
            each_list.append(each)
        return each_list


separate_word = SeparateWord()

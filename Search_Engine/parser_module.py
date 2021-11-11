import operator
import re
from nltk.corpus import stopwords
from document import Document
from stemmer import Stemmer
import json


class Parse:
    def __init__(self):
        self.stop_words = stopwords.words('english')
        self.stop_words_set = set(self.stop_words)
        self.add_stop_words()
        self.count = 0
        self.__max_term_appearance = 0
        self.__max_term = ''
        self.__length_of_all_terms = 0

    def add_stop_words(self):
        """
        This function add stop words to stop word set .
        """
        stop_word_list = ['www', 'http', 'https', 'html', 'com', 'co', 'il', 'ru', 'fr' 'a', 'b', 'c', 'd', 'e', 'f'
                          , 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'ad', 'ae', 'af', 'ag', 'ai', 'al', 'al', 'an', 'ao'
                          , 'ar', 'as', 'at', 'au', 'ca', 'rktnjsg', 'cm', 'li', 'qu', 'de', 'wo', 'bui', 'am', 'pm'                                                                                       
                          'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', ':', '', ' ', 'rt' ':', ',',
                          '.', '/', '<', '>', ';', "'", '|', '*', '-', '=', 'rt', '+', '_', 'bit', 'ly', 'qu', 'ny'
                          '(', ')', '{', '}', '[', ']', '"', '%', '!', '$', '`', '~', '’', '#', '@', 'please', 'bn', 'tge'
                          , 'yo', 'aj', 'ach', 'st', 'cesspoo', 'ex', 'nd', 'heeh', 'ie', 'cannot', 'would'
                          ]
        stop_word_set = set(stop_word_list)
        self.stop_words_set.update(stop_word_set)

    def parse_corona(self):
        """
        this function parsing words that represent corona virus and turn all this words to covid
        :return: corona_list - list that contains string of "covid"
        """
        corona_list = ['covid']
        return corona_list

    def split_on_uppercase(self, s, keep_contiguous=True):

        """
        Args: s (str): string
        keep_contiguous (bool): flag to indicate we want to keep contiguous uppercase chars together
        Returns:
        """
        string_length = len(s)
        is_lower_around = (lambda: s[i - 1].islower() or string_length > (i + 1) and s[i + 1].islower())
        start = 0
        parts = []
        for i in range(1, string_length):
            if s[i] == '_':
                parts.append(s[start:i].lower())
                start = i + 1
                continue
            if s[i].isupper() and (not keep_contiguous or is_lower_around()) and start != i:
                parts.append(s[start: i].lower())
                start = i
        parts.append(s[start:].lower())
        return parts

    def hash_tags_parse(self, hash_tag_term):
        """
        this function parsing word that contain hash tag
        :param hash_tag_term : term that contain hash tag
        :return hash_tag_terms_list: list that contains tokens of hash_tag_term
        """


        hash_tag_terms_list = []
        if not hash_tag_term.isascii():
            return hash_tag_terms_list
        hash_tag_terms_list.append
        if "covid" in hash_tag_term.lower() or 'corona' in hash_tag_term:
            hash_tag_terms_list.extend(self.parse_corona())
        if not any(char.isdigit() for char in hash_tag_term):
            splited_hash_tag = self.split_on_uppercase(hash_tag_term[1:])
            for cur_word in splited_hash_tag:
                hash_tag_terms_list.append(cur_word)
        if '_' in hash_tag_term:
            hash_tag_term = hash_tag_term.lower().replace('_', '')
        else:
            hash_tag_term = hash_tag_term.lower()
        hash_tag_terms_list.append(hash_tag_term)
        return hash_tag_terms_list

    def percent_parse(self, percent_number):
        """
        this function parsing number that contain percent
        :param percent_number : number contains percent from text
        :return percent_list list that contains the percent_number parsed:
        """
        if not percent_number.isascii():
            return list()
        percent_list = []
        if percent_number[-1] == '%':
            percent_list.append(percent_number)
        elif 'percent' in percent_number.lower():
            percent = ''
            for char in percent_number:
                if char == ' ':
                    break
                else:
                    percent += char
            percent_number += '%'
            percent_list.append(percent)
        return percent_list

    def help_number_parse(self, num, kind=None):
        if not str(num).isascii():
            return list()
        """
        Function that help parse numbers by several rules
        :param num : number contains percent from text
        :param kind: represent the letter after the number
        :return numbers_list: list that contain the number parsed
        """
        try:
            numbers_list = []
            if type(num) is int or type(num) is float:
                if num < 1000:
                    numbers_list.append(str(num))
                elif num < 1000000:
                    num = round((float(num) / 1000), 3)
                    if num.is_integer():
                        num = int(num)
                    else:
                        num = round(num, 3)
                    numbers_list.append(str(num) + 'K')
                elif num < 1000000000:
                    num = round((float(num) / (1000 ** 2)), 3)
                    if num.is_integer():
                        num = int(num)
                    else:
                        num = round(num, 3)
                    numbers_list.append(str(num) + 'M')
                else:
                    num = round((float(num) / (1000 ** 3)), 3)
                    if num.is_integer():
                        num = int(num)
                    else:
                        num = round(num, 3)
                    numbers_list.append(str(num) + 'B')

            else:
                if round(float(num), 3) < 1000:
                    if float(num).is_integer():
                        numbers_list.append(str(int(num)) + kind)
                    else:
                        numbers_list.append(str(round(float(num))) + kind)
                elif round(float(num), 3) < 1000000:
                    if float(int(num) / 1000).is_integer():
                        if kind == 'K':
                            numbers_list.append(str(int(int(num) / 1000)) + 'M')
                        elif kind == 'M':
                            numbers_list.append(str(int(int(num) / 1000)) + 'B')
                    else:
                        if kind == 'K':
                            numbers_list.append(str(round(float(int(num) / 1000), 3)) + 'M')
                        elif kind == 'M':
                            numbers_list.append(str(round(float(int(num) / 1000), 3)) + 'B')
            return numbers_list
        except:
            return []

    def number_parse(self, number):
        """
        This function parsing numbers from text, the function is using additional function
        that help decide how to do the parse
        :param number : number contains percent from text
        :return list: the list contains the the parsed number
        """
        if not number.isascii():
            return list()
        if number.lower() == 'thousand':
            return self.help_number_parse('1', 'K')
        elif number.lower() == 'million':
            return self.help_number_parse('1', 'M')
        elif number.lower() == 'billion':
            return self.help_number_parse('1', 'B')
        if 'thousand' in number.lower():
            num = number[:len(number) - len('thousand')]
            return self.help_number_parse(num, "K")
        elif 'million' in number.lower():
            num = number[:len(number) - len('million')]
            return self.help_number_parse(num, "M")
        elif 'billion' in number.lower():
            num = number[:len(number) - len('billion')]
            return self.help_number_parse(num, "B")
        else:
            try:
                number = round(float(number), 3)
                if number.is_integer():
                    number = int(number)
                return self.help_number_parse(number)
            except:
                return []

    def urls_parse(self, url):
        """
        this function parsing word that represent url
        :param url : url from text
        :return url_terms_list: list of url tokens without junk words
        """
        if not url.isascii():
            return list()
        url_terms = re.split('=|://|-|www.|/|\?|#|_|\+|%|\$|!|@|^|&|\*|\(\|\)|\.|~', url)
        url_terms_list = []
        is_unnecessary = (lambda: url_term == '' or url_term.lower() in self.stop_words_set)
        for url_term in url_terms:
            if len(url_terms) == 3:
                break
            elif len(url_terms) == 4 and url_terms[2] == '':
                break
            if not is_unnecessary or len(url_term) < 1 or url_term.isdigit() or '.X' in url_term:
                continue
            if url_term in self.stop_words_set:
                continue
            if not url_term.lower():
                continue
            if any(char.isdigit() for char in url_term):
                continue
            if 'covid' in url_term or 'corona' in url_term:
                url_terms_list.extend(self.parse_corona())
                continue
            url_terms_list.append(url_term.lower())
        return url_terms_list

    def tagging_word(self, tagging_word):
        """
        :param - tagging_word : word that contains @
        :return tagging_word_in_list: list that contains tagging_word
        """
        if not tagging_word.isascii():
            return list()
        tagging_word_in_list = [tagging_word]
        return tagging_word_in_list

    def belong_number(self, term):
        """
        This function get a word and return true if that word attached to a number that came before this word
        :param term: word that came after a number
        :returns tuple (boolean,string): the boolean tell us if the word attached to a number or not
                 and the string is the word we need to add to the number that came before the word that we check
        """
        term = term.lower()
        if 'million' == term or 'milion' == term:
            return True, 'million'
        if 'thousand' == term or 'thousands' == term:
            return True, 'thousand'
        if 'billion' == term or 'bilion' == term:
            return True, 'billion'
        if term == '%' or 'percent' in term:
            return True, '%'
        return False, ''

    def operate_tokens(self, tokens_list_before_operation):
        """
        :param tokens_list_before_operation: list of tokens
        :return operated_tokens: list of right tokens after several processes
        """
        operated_tokens = []
        need_pass = False
        for index, token in enumerate(tokens_list_before_operation):
            if need_pass:
                need_pass = False
                continue
            if token.isdigit():
                if index + 1 < len(tokens_list_before_operation):
                    next_term = tokens_list_before_operation[index + 1]
                    is_belong_to_number, add_to_term = self.belong_number(next_term)
                    if is_belong_to_number:
                        term_with_next = token + add_to_term
                        operated_tokens.append(term_with_next.lower())
                        need_pass = True
                    else:
                        operated_tokens.append(token.lower())
                else:
                    operated_tokens.append(token.lower())
            else:
                if 'covid' in token.lower() or "corona" in token.lower() or 'coronna' in token.lower():
                    if index + 1 < len(tokens_list_before_operation):
                        next_term = tokens_list_before_operation[index + 1]
                        if next_term == '19':
                            need_pass = True
                            operated_tokens.append('covid')
                        else:
                            operated_tokens.append('covid')
                    else:
                        operated_tokens.append('covid')
                else:
                    operated_tokens.append(token)
        return operated_tokens

    def parse_sentence(self, text, stemming=False, tweet_urls=None):
        """
        This function tokenize, remove stop words and apply lower case for every word within the text
        :param tweet_urls:
        :param stemming:
        :param text:
        :return:
        """
        list_of_parsed_terms = []
        regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
        urls = re.findall(regex, text)
        string = text
        if tweet_urls and len(tweet_urls) > 2:
            for url in urls:
                if url[0] in text:
                    string = string.replace(url[0], ' ', 1)
                    try:
                        tweet_urls = json.loads(tweet_urls)
                        list_of_parsed_terms.extend(self.urls_parse(tweet_urls[url[0]]))
                    except:
                        pass
        elif tweet_urls is None:
            for url in urls:
                try:
                    string = string.replace(url[0], ' ', 1)
                except:
                    pass
        else:
            for url in urls:
                if url[0] in text:
                    string = string.replace(url[0], ' ', 1)
        string = re.sub(r'(\D)(\d+)%', r'\1 \2% ', string)
        string = re.sub(r'(\S)@', r'\1 @', string)
        string = re.sub(r'(\S)#', r'\1 #', string)
        string = re.sub(r'\$', 'S', string)
        string = re.sub(r'(\d+)([a-zA-Z])', r'\1 \2', string)
        string = re.sub(r'(\d),(\d)', r'\1\2', string)
        string = re.sub(r'(\D)\.', r'\1 ', string)
        regx_string = re.split('\s|\b|!|\a|\(|\)|-|\?|~|[^a-zA-Z0-9_@#%]', string)
        text_tokens_without_stopwords = [term for term in regx_string if term.lower() not in self.stop_words_set and len(term) > 0]
        operated_tokens = self.operate_tokens(text_tokens_without_stopwords)

        for term in operated_tokens:

            if '#' == term[0]:
                list_of_parsed_terms.extend(self.hash_tags_parse(term))
            elif term[0].isdigit():
                if '%' in term:
                    if len(term) > 6:
                        continue
                    else:
                        list_of_parsed_terms.extend(self.percent_parse(term))
                else:
                    if len(term) > 14:
                        continue
                    else:
                        list_of_parsed_terms.extend(self.number_parse(term))

            elif term[0] == '@':
                list_of_parsed_terms.extend(self.tagging_word(term))
            elif 'covid' in term.lower() or 'corona' in term.lower():
                list_of_parsed_terms.extend(self.parse_corona())
            else:
                list_of_parsed_terms.append(term)
        if stemming:
            stemming_list = self.return_finished_parsed_tokens_list(list_of_parsed_terms, stem=True)
            return stemming_list
        finished_parsed_terms = self.return_finished_parsed_tokens_list(list_of_parsed_terms)
        return finished_parsed_terms

    def return_finished_parsed_tokens_list(self, list_of_parsed_terms, stem=False):
        """
        This function check all the tokens in list_of_parsed_terms, and decide if there is not relevant tokens,
        if token is relvent the function add the token to finished_parsed_terms. also this function check if token in
        index '0' is lower case, if it is lower the function make all the token to be lower case, if token in index '0'
        is upper case the function make all the toke be upper case
        :param list_of_parsed_terms:
        :param stem:
        :return finished_parsed_terms:
        """
        finished_parsed_terms = []
        for token in list_of_parsed_terms:
            if stem:
                stem = Stemmer()
                token = stem.stem_term(token)
            if len(token) < 1:
                continue
            if token.lower() in self.stop_words_set:
                continue
            if not token[0] == '#' and not token[0] == '@':
                if token[0].islower():
                    token = token.lower()
                else:
                    token = token.upper()
            count_chars = 1
            for idx, char in enumerate(token):
                if idx + 1 < len(token) and char == token[idx+1]:
                    count_chars += 1
                if count_chars == 3 and not char.isdigit():
                    count_chars = 1
                    continue
                if count_chars == 11:
                    count_chars = 1
                    continue
            finished_parsed_terms.append(token)
        return finished_parsed_terms

    def add_term(self, term, term_dict, entities_dict):
        """
        This function get word and 2 dictionaries , and decide to what dictionary we need to add the word
        :param term: token as string(word)
        :param term_dict: dictionary that the keys is the term and the value is the number of appearance of that term in
               the text
        :param entities_dict:
        """
        if term[0].isupper():
            if term.lower() in term_dict.keys():
                term_dict[term.lower()] = term_dict[term.lower()] + 1
                upper_term = term.upper()
                if upper_term in entities_dict.keys():
                    if entities_dict[upper_term] > 1:
                        entities_dict[upper_term] = entities_dict[upper_term] - 1
                    else:
                        del entities_dict[upper_term]
        else:
            if term in term_dict.keys():
                term_dict[term] = term_dict[term] + 1
            else:
                term_dict[term] = 1

    def find_entities(self, entities_dict, tokenized_text):
        """
        This function get text and find entities in the text, all the entities will be put to the entities dictionary
        :param entities_dict:
        :param tokenized_text:
        """
        entity_sentance = ''
        for word in tokenized_text:
            if word[0].isupper():
                upper_word = word.upper()
                if upper_word in entities_dict.keys():
                    entities_dict[upper_word] = entities_dict[upper_word] + 1
                else:
                    entities_dict[upper_word] = 1
                if entity_sentance == '':
                        entity_sentance = upper_word
                else:
                    entity_sentance = entity_sentance + ' ' + upper_word
                    if entity_sentance in entities_dict.keys():
                        entities_dict[entity_sentance] = entities_dict[entity_sentance] + 1
                    else:
                        entities_dict[entity_sentance] = 1
            else:
                entity_sentance = ''

    def parse_doc(self, doc_as_list, stemm=False):
        """
        This function takes a tweet document as list and break it into different fields
        :param stemm:
        :param doc_as_list: list re-presenting the tweet.
        :return: Document object with corresponding fields.
        """
        tweet_id = doc_as_list[0]
        tweet_date = doc_as_list[1]
        full_text = doc_as_list[2]
        url = doc_as_list[3]
        retweet_text = doc_as_list[4]
        retweet_url = doc_as_list[5]
        quote_text = doc_as_list[6]
        quote_url = doc_as_list[7]
        entities_dict = {}
        term_dict = {}
        all_terms = set()
        tokenized_text = self.parse_sentence(full_text, stemming=stemm, tweet_urls=url)
        doc_length = len(tokenized_text)  # after text operations.
        self.find_entities(entities_dict, tokenized_text)
        for term in tokenized_text:
            self.add_term(term, term_dict, entities_dict)
            all_terms.add(term)

        length_of_uniqe_term = len(all_terms)

        max_from_entitiy = False
        try:
            term_max = max(term_dict.values())
            try:
                entities_max = max(entities_dict.values())
                if entities_max > term_max:
                    max_from_entitiy = True
                self.__max_term_appearance = max(term_max, entities_max)
            except:
                self.__max_term_appearance = term_max
        except:
            try:
                entities_max = max(entities_dict.values())
                self.__max_term_appearance = entities_max
                max_from_entitiy = True
            except:
                self.__max_term_appearance = 0
        if self.__max_term_appearance > 1:
            if max_from_entitiy:
                self.__max_term = max(entities_dict.items(), key=operator.itemgetter(1))[0]
            else:
                self.__max_term = max(term_dict.items(), key=operator.itemgetter(1))[0]

        else:
            self.__max_term = ''
        self.__length_of_all_terms = len(tokenized_text)
        document = Document(tweet_id, tweet_date, full_text, url, retweet_text, retweet_url, quote_text,
                            quote_url, term_dict, entities_dict, doc_length, length_of_uniqe_term,
                            self.__length_of_all_terms, self.__max_term, self.__max_term_appearance)
        return document

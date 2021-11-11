import os
import utils


class Indexer:

    number_of_file = 0

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def __init__(self, config):
        self.postingDict = {}
        self.entities = dict()
        self.config = config
        self.files_list = []
        self.documents_dict = dict()
        self.number_of_tweets_in_corpus = 0
        self.sum_of_length = 0

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def add_new_doc(self, document):
        """
        This function perform indexing process for a document object.
        Saved information is captures via two dictionaries ('inverted index' and 'posting')
        :param document: a document need to be indexed.
        """
        self.number_of_tweets_in_corpus += 1
        self.documents_dict[document.tweet_id] = str(document.length_of_all_terms)
        self.number_of_tweets_in_corpus += 1
        self.sum_of_length += document.length_of_all_terms
        document_dictionary = document.term_doc_dictionary
        document_entities_dict = document.entities_doc_dictionary
        # Go over each term in the doc
        for term in document_entities_dict.keys():
            self.add_term(term, document.tweet_id, document_entities_dict[term], True)
        for term in document_dictionary.keys():
            try:
                self.add_term(term, document.tweet_id, document_dictionary[term], False)
            except:
                pass

    def add_details(self):
        """
        This function saves details about the corpus
        """
        self.documents_dict["sum_of_length"] = self.sum_of_length
        self.documents_dict["number_of_tweets_in_corpus"] = self.number_of_tweets_in_corpus

    def save_documents_dict(self):
        """"
        This function using utils class to save file as pickle
        file that contains details about the corpus and tweets
        """
        utils.save_obj(self.documents_dict, os.getcwd() + '\\documents_dict')

    def add_term(self, term, tweet_id, appearance_number_in_tweet, is_entity):
        """
               This function add term to dictionary .
               Saved information and the term himself  or in the dictionary  ('entities') or in dictionary  ('posting')
               :param term: the term we want to add
               :param tweet_id: id of document that term showes in it
               :param appearance_number_in_tweet: number of appearance that term showes in document
               :param is_entity: this variable tell us if the term is entity or not
               """
        if not is_entity:
            if term.upper() not in self.postingDict.keys() and term.lower() not in self.postingDict.keys():
                tweet_list_details = dict()
                tweet_list_details[tweet_id] = appearance_number_in_tweet
                self.postingDict[term] = [tweet_list_details, appearance_number_in_tweet]
            else:
                self.lower_or_upper(term, tweet_id, appearance_number_in_tweet)
        else:
            if term not in self.entities.keys():
                if term.lower() not in self.postingDict.keys() and term not in self.postingDict.keys():
                    tweet_list_details = dict()
                    tweet_list_details[tweet_id] = appearance_number_in_tweet
                    self.entities[term] = [tweet_list_details, appearance_number_in_tweet]
                else:
                    self.lower_or_upper(term, tweet_id, appearance_number_in_tweet)
            else:
                if term.lower() not in self.postingDict.keys():
                    pre_appearance_number = self.entities[term][1]
                    tweet_list_details = dict()
                    for key in self.entities[term][0].keys():
                        tweet_list_details[key] = self.entities[term][0][key]
                    tweet_list_details[tweet_id] = appearance_number_in_tweet
                    self.postingDict[term] = [tweet_list_details, pre_appearance_number+appearance_number_in_tweet]
                    self.postingDict[term][0][tweet_id] = appearance_number_in_tweet
                    self.postingDict[term][1] = pre_appearance_number + appearance_number_in_tweet
                    del self.entities[term]
                else:
                    pre_appearance_number = self.entities[term][1]
                    tweet_list_details = dict()
                    for key in self.entities[term][0].keys():
                        tweet_list_details[key] = self.entities[term][0][key]
                    tweet_list_details[tweet_id] = appearance_number_in_tweet
                    number_of_entity = int(pre_appearance_number) + int(appearance_number_in_tweet)
                    self.postingDict[term.lower()][0].update(tweet_list_details)
                    self.postingDict[term.lower()][1] = int(self.postingDict[term.lower()][1]) + number_of_entity

    def lower_or_upper(self, term, tweet_id, appearance_number_in_tweet):
        """
        This function check if the term will be in the dictionary in upper case or on lower case.

        :param term: the term we want to check
        :param tweet_id: id of document that term showes in it
        :param appearance_number_in_tweet: number of appearance that term showes in document
        """
        appearance_number_in_tweet = int(appearance_number_in_tweet)
        tweet_list_details = {}
        if term == term.lower():
            upper_term = term.upper()
            if upper_term in self.postingDict.keys():
               values_posting = self.postingDict[upper_term]
               tweet_list_details[tweet_id] = appearance_number_in_tweet
               self.postingDict[term] = [tweet_list_details, appearance_number_in_tweet]
               self.postingDict[term][0].update(values_posting[0])
               self.postingDict[term][1] = appearance_number_in_tweet+int(values_posting[1])
               del self.postingDict[upper_term]
            elif term in self.postingDict.keys():
                tweet_list_details[tweet_id] = appearance_number_in_tweet
                self.postingDict[term][0].update(tweet_list_details)
                self.postingDict[term][1] += appearance_number_in_tweet
            else:
                tweet_list_details[tweet_id] = appearance_number_in_tweet
                self.postingDict[term] = [tweet_list_details, appearance_number_in_tweet]

        elif term == term.upper():
            lower_term = term.lower()
            if lower_term in self.postingDict.keys():
                tweet_list_details[tweet_id] = appearance_number_in_tweet
                self.postingDict[term] = [tweet_list_details, appearance_number_in_tweet]
                values_doc_dict = self.postingDict[term]
                self.postingDict[lower_term][0].update(values_doc_dict[0])
                self.postingDict[lower_term][1] = int(self.postingDict[lower_term][1]) + values_doc_dict[1]
                del self.postingDict[term]
            elif term in self.postingDict.keys():
                tweet_list_details[tweet_id] = appearance_number_in_tweet
                self.postingDict[term][0].update(tweet_list_details)
                self.postingDict[term][1] += appearance_number_in_tweet
            else:
                tweet_list_details[tweet_id] = appearance_number_in_tweet
                self.postingDict[term] = [tweet_list_details, appearance_number_in_tweet]

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def load_index(self, fn):
        """
        Loads a pre-computed index (or indices) so we can answer queries.
        Input:
            fn - file name of pickled index.
        """

        path = os.getcwd() + '\\' + fn
        return utils.load_obj(path)

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def save_index(self, fn):
        """
        Saves a pre-computed index (or indices) so we can save our work.
        Input:
              fn - file name of pickled index.
        """
        utils.save_obj(self.postingDict, os.getcwd() + '\\' + fn)

    # feel free to change the signature and/or implementation of this function 
    # or drop altogether.
    def _is_term_exist(self, term):
        """
        Checks if a term exist in the dictionary.
        """
        return term in self.postingDict

    # feel free to change the signature and/or implementation of this function 
    # or drop altogether.
    def get_term_posting_list(self, term):
        """
        Return the posting list from the index for a term.
        """
        return self.postingDict[term] if self._is_term_exist(term) else []

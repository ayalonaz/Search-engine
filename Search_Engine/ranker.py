# you can change whatever you want in this module, just make sure it doesn't 
# break the searcher module
from BM25 import BM25
import utils

class Ranker:
    def __init__(self):
        pass

    @staticmethod
    def rank_relevant_docs(relevant_docs, k=None, weight=None):
        """
        This function provides rank for each relevant document and sorts them by their scores.
        The current score considers solely the number of terms shared by the tweet (full_text) and query.
        :param k: number of most relevant docs to return, default to everything.
        :param relevant_docs: dictionary of documents that contains at least one term from the query.
        :return: sorted list of documents by score
        """

        documents = utils.load_obj("documents_dict")
        doc_score = {}
        average_of_corpus_doc = float(documents["sum_of_length"])/float(documents["number_of_tweets_in_corpus"])
        corpus_size = int(documents["number_of_tweets_in_corpus"])
        bm25 = BM25()
        for term in relevant_docs.keys():
            for doc in relevant_docs[term][0].keys():
                score = bm25.score_BM25(relevant_docs[term][1], int(relevant_docs[term][0][doc][1]), 1, 0, corpus_size,
                                        relevant_docs[term][0][doc][0], average_of_corpus_doc)
                if doc in doc_score.keys():
                    doc_score[doc] += score*weight[term]
                else:
                    try:
                        doc_score[doc] = score*weight[term]
                    except:

                        print(f'doc_score[doc] : {doc_score[doc]}')
                        print(f'weight[term] : {weight[term]}')
        sorted_doc_score = sorted(doc_score.items(), key=lambda item: item[1], reverse=True)
        new_sorted_list = []
        for tweet_tuple in sorted_doc_score:
            new_sorted_list.append(tweet_tuple[0])
        if k is not None:
            return new_sorted_list[:k]
        else:

            return new_sorted_list

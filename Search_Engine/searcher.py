
from ranker import Ranker


# DO NOT MODIFY CLASS NAME
class Searcher:
    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit. The model
    # parameter allows you to pass in a precomputed model that is already in
    # memory for the searcher to use such as LSI, LDA, Word2vec models.
    # MAKE SURE YOU DON'T LOAD A MODEL INTO MEMORY HERE AS THIS IS RUN AT QUERY TIME.
    def __init__(self, parser, indexer, model=None, thesaurus=None, spell_checker=None, similar=None, word_net=None):
        self._parser = parser
        self._indexer = indexer
        self.inverted_index = self._indexer.load_index('inverted_idx')
        self.dict_of_all_doc = self._indexer.load_index('documents_dict')
        self._ranker = Ranker()
        self._model = model
        self.synonyms = thesaurus
        self.spell = spell_checker
        self.similar = similar
        self.word_net = word_net

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def search(self, query, k=None, stem=False):
        """
        Executes a query over an existing index and returns the number of
        relevant docs and an ordered list of search results (tweet ids).
        Input:
            query - string.
            k - number of top results to return, default to everything.
        Output:
            A tuple containing the number of relevant search results, and
            a list of tweet_ids where the first element is the most relavant
            and the last is the least relevant result.
        """
        if len(query) == 0:
            return 0, []
        query_as_list = self._parser.parse_sentence(query, stem)
        # ------------------------ Thesaurus + Word 2 Vec  + word net + spell checker ----------------------------#
        all_synonyms = []
        all_similars = []
        all_spells = []
        word_net = []
        weight_dict = dict()
        if self.spell is not None:
            for word in query_as_list:

                try:
                    correct_word = self.spell.correction(word)
                    all_spells.append(correct_word)
                    weight_dict[correct_word] = 0.5
                except:
                    all_spells.append(word)
                    weight_dict[word] = 0.5
            query_as_list = all_spells
        if self.synonyms is not None or self.similar is not None or self.word_net is not None:
            for cur_word in query_as_list:
                weight_dict[cur_word] = 0.5
                if self.synonyms is not None:
                    word_synonyms = self.synonyms.get_synonyms(cur_word)
                    for syn_word in word_synonyms:
                        weight_dict[syn_word] = 0.5/len(word_synonyms)
                    all_synonyms.extend(word_synonyms)
                if self.similar is not None:
                    word_similars = self.similar.get_similar_word_list(cur_word)
                    for similar_word in word_similars:
                        weight_dict[similar_word] = 0.5/len(word_similars)
                    all_similars.extend(word_similars)
                if self.word_net is not None:
                    try:
                        synset = self.word_net.synsets(cur_word)
                        count_lemmas_name = 0
                        for sys in synset:
                            if count_lemmas_name == 2:
                                break
                            for lemma in sys.lemmas():
                                if count_lemmas_name == 2:
                                    break
                                if lemma.name() == cur_word:
                                    continue
                                else:
                                    word_net.append(lemma.name())
                                    count_lemmas_name += 1
                        for lemma_name in word_net:
                            weight_dict[lemma_name] = 0.5 / len(word_net)
                    except:
                        pass

            query_as_list.extend(all_synonyms)
            query_as_list.extend(all_similars)
            query_as_list.extend(word_net)

        # ------------------------ Thesaurus + Word 2 Vec + word net + spell checker----------------------------#
        try:
            relevant_docs = self._relevant_docs_from_posting(query_as_list)
            n_relevant = 0
            for key in relevant_docs.keys():
                n_relevant += len(relevant_docs[key][0])
            ranked_doc_ids = Ranker.rank_relevant_docs(relevant_docs, k, weight=weight_dict)
            return n_relevant, ranked_doc_ids
        except:
            return 0, []

    def _relevant_docs_from_posting(self, query_as_list):
        """
        This function loads the posting list and count the amount of relevant documents per term.
        :param query_as_list: parsed query tokens
        :return: dictionary of relevant documents mapping doc_id to document frequency.
        """
        doc_dict = {}
        query_result = dict()
        term_dict = dict()
        information_docs_dict = {}
        sorted_list_of_query_terms = sorted(query_as_list, key=str.casefold)
        terms_list = []
        curr_term = sorted_list_of_query_terms[0]
        terms_list.append(curr_term)
        for term in sorted_list_of_query_terms:
            if term in self.inverted_index.keys():
                dict_of_doc_terms = self.inverted_index[term][0]
            else:
                continue
            for element in dict_of_doc_terms:
                doc_dict[element] = dict_of_doc_terms[element]
            term_dict[term] = dict(doc_dict)
            doc_dict = dict()
        for term in term_dict.keys():
            if len(term_dict[term].keys()) > 0:
                list_of_term_documents = set(term_dict[term].keys())
                for doc in list_of_term_documents:
                    information_docs_dict[doc] = [self.dict_of_all_doc[doc], self.inverted_index[term][0][doc]]
                list_of_details_by_term = [information_docs_dict, len(information_docs_dict)]
                query_result[term] = list_of_details_by_term
                information_docs_dict = {}
            else:
                continue
        return query_result

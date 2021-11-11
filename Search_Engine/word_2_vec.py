import linecache
import os
from gensim.models import Word2Vec


class Word_2_vec:
    file_counter = 0
    write_counter = 0

    def __init__(self, list_of_sentences=None, load_index=False):
        if load_index:
            self.index_word_2_vec = self.get_index()
        else:
            self.list_of_sentences = list_of_sentences
            if list_of_sentences is not None:
                self.model = Word2Vec(window=10, min_count=1, workers=4, iter=100)
                self.model.build_vocab(list_of_sentences)
            else:
                print('loads')
                self.model = Word2Vec.load('word2vec.model')

    def train(self):
        """
        This function train a model that contains vocabulary of sentences and save the model as 'word2vec.model'
        """
        self.model.train(self.list_of_sentences, total_examples=self.model.corpus_count, epochs=self.model.iter)
        self.model.save("word2vec.model")


    def get_index(self):
        """
        This function load to the memory the index file of word-2-vec
        :return similars:
        """
        word2vec_index_file = os.getcwd() + "\\word2vec\\index_similar.txt"
        file = open(word2vec_index_file, 'r')
        similars = {}
        for line in file:
            split_line = line.split('~')
            similars[split_line[0]] = split_line[1]
        return similars

    def get_similar_word_list(self, word):
        """
        This function get word and return the similar word that can be in the same sentence(after train model of
        sentences) , the function read the words from file that contains the similar words
        :param word:
        :return list_of_similars_words:
        """
        list_of_similars_words = []
        if word.lower() in self.index_word_2_vec.keys():
            line_of_similar = int(self.index_word_2_vec[word.lower()]) + 1
            line = linecache.getline(os.getcwd() + '\\word2vec\\similar.txt', line_of_similar)
            line_split = line.split('~', 1)
            similar_word_split = line_split[1].split('|')
            if similar_word_split[len(similar_word_split) - 1][len(similar_word_split[len(similar_word_split) - 1]) - 1] == '\n':
                similar_word_split[len(similar_word_split) - 1] = similar_word_split[len(similar_word_split) - 1].replace('\n', '')
            list_of_similars_words.extend(similar_word_split)
            return list_of_similars_words
        elif word in self.index_word_2_vec.keys():
            line_of_similar = int(self.index_word_2_vec[word]) + 1
            line = linecache.getline(os.getcwd() + '\\word2vec\\similar.txt', line_of_similar)
            line_split = line.split('~', 1)
            similar_word_split = line_split[1].split('|')
            if similar_word_split[len(similar_word_split) - 1][
                len(similar_word_split[len(similar_word_split) - 1]) - 1] == '\n':
                similar_word_split[len(similar_word_split) - 1] = similar_word_split[
                    len(similar_word_split) - 1].replace('\n', '')
            list_of_similars_words.extend(similar_word_split)
            return list_of_similars_words
        else:
            return list_of_similars_words

    def write_word2vec_file(self):
        vec_dict = {}
        for word in self.model.wv.vocab:
            similar_words = self.model.wv.most_similar([word], topn=4)
            similar_words_list = [x[0] for x in similar_words]
            vec_dict[word] = similar_words_list
            self.write_counter += 1
            if self.write_counter == 100000:
                self.write_to_disk(vec_dict)
                vec_dict = {}
                self.write_counter = 0
        if 100000 > self.write_counter > 0:
            self.write_to_disk(vec_dict)
            self.write_counter = 0

    def write_to_disk(self, vec_dict):
        path = os.getcwd() + "\\word2vec"
        file_path = path + "\\word2vec" + str(self.file_counter) + ".txt"
        f = open(file_path, "w")
        print("write to disk file number " + str(self.file_counter))
        self.file_counter += 1
        try:
            os.mkdir(path)
        except:
            print("folder already exsists")
        similar_word_lines = []
        for idx, word in enumerate(vec_dict):
            cur_line = str(word) + '~'
            for index, similar_word in enumerate(vec_dict[word]):
                if index < len(vec_dict[word]) - 1:
                    cur_line += str(similar_word) + '|'
                else:
                    cur_line += str(similar_word) + '\n'
                    similar_word_lines.append(cur_line)
        f.writelines(similar_word_lines)

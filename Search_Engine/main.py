
if __name__ == '__main__':
    import os
    import pandas as pd
    import time
    import importlib
    tweets_text = dict()
    df = pd.read_parquet(os.getcwd() + '\\data\\benchmark_data_train.snappy.parquet', engine="pyarrow")
    documents_list = df.values.tolist()
    for idx, tweet in enumerate(documents_list):
        tweets_text[tweet[0]] = tweet[2]
    engine_modules = ['search_engine_' + name for name in ['1', '3', 'best']]
    for engine in engine_modules:
        se = importlib.import_module(engine)
        # logging.info(f"Successfully imported module {engine_module}.")
        engine = se.SearchEngine(config=None)
        print('\n\n')
        print(f'Current engine: {engine}')
        queries = pd.read_csv(os.path.join('data', 'queries_train.tsv'), sep='\t')
        for i, row in queries.iterrows():
            if i == 0:
                q_id = row['query_id']
                q_keywords = row['keywords']
                start_time = time.time()
                q_n_res, q_res = engine.search(q_keywords, 5)
                if q_n_res is None or q_res is None or q_n_res < 1 or len(q_res) < 1:
                    print("Query number 1 resultes : None")
                    break
                else:
                    print("Query number 1 resultes :")
                    for res in q_res:
                        print('\n')
                        print(f'Tweet id: {res}')
                        print("Text : ")
                        counter = 0
                        for idx, tweet_text in enumerate(tweets_text[res].split(' ')):
                            if counter == 17:
                                print(tweet_text)
                                counter = 0
                            else:
                                print(tweet_text, end=' ')
                                counter += 1
                        print('\n')
            if i == 1:
                q_id = row['query_id']
                q_keywords = row['keywords']
                start_time = time.time()
                q_n_res, q_res = engine.search(q_keywords, 5)
                if q_n_res is None or q_res is None or q_n_res < 1 or len(q_res) < 1:
                    print("Query number 2 resultes : None")
                    break
                else:
                    print("Query number 2 resultes : ")
                    for res in q_res:
                        print('\n')
                        print(f'Tweet id: {res}')
                        print("Text : ")
                        counter = 0
                        for idx, tweet_text in enumerate(tweets_text[res].split(' ')):
                            if counter == 17:
                                print(tweet_text)
                                counter = 0
                            else:
                                print(tweet_text, end=' ')
                                counter += 1
                        print('\n')
            if i == 3:
                q_id = row['query_id']
                q_keywords = row['keywords']
                start_time = time.time()
                q_n_res, q_res = engine.search(q_keywords, 5)
                if q_n_res is None or q_res is None or q_n_res < 1 or len(q_res) < 1:
                    print("Query number 4 resultes : None")
                    break
                else:
                    print("Query number 4 resultes : ")
                    for res in q_res:
                        print('\n')
                        print(f'Tweet id: {res}')
                        print("Text : ")
                        counter = 0
                        for idx, tweet_text in enumerate(tweets_text[res].split(' ')):
                            if counter == 17:
                                print(tweet_text)
                                counter = 0
                            else:
                                print(tweet_text, end=' ')
                                counter += 1
                        print('\n')


            if i == 6:
                q_id = row['query_id']
                q_keywords = row['keywords']
                start_time = time.time()
                q_n_res, q_res = engine.search(q_keywords, 5)
                if q_n_res is None or q_res is None or q_n_res < 1 or len(q_res) < 1:
                    print("Query number 7 resultes : None")
                    break
                else:
                    print("Query number 7 resultes : ")
                    for res in q_res:
                        print('\n')
                        print(f'Tweet id: {res}')
                        print("Text : ")
                        counter = 0
                        for idx, tweet_text in enumerate(tweets_text[res].split(' ')):
                            if counter == 17:
                                print(tweet_text)
                                counter = 0
                            else:
                                print(tweet_text, end=' ')
                                counter += 1
                        print('\n')
            if i == 7:
                q_id = row['query_id']
                q_keywords = row['keywords']
                start_time = time.time()
                q_n_res, q_res = engine.search(q_keywords, 5)
                if q_n_res is None or q_res is None or q_n_res < 1 or len(q_res) < 1:
                    print("Query number 8 resultes : None")
                    break
                else:
                    print("Query number 8 resultes : ")
                    for res in q_res:
                        print('\n')
                        print(f'Tweet id: {res}')
                        print("Text : ")
                        counter = 0
                        for idx, tweet_text in enumerate(tweets_text[res].split(' ')):
                            if counter == 17:
                                print(tweet_text)
                                counter = 0
                            else:
                                print(tweet_text, end=' ')
                                counter += 1
                        print('\n')

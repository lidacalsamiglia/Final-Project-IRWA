from myapp.search.algorithms import *
import random 

class SearchEngine:
    """educational search engine"""

    def search(self, search_query, search_id, corpus, alg, corpus_df):
        print("Search query:", search_query)

        results = []
        results = search_in_corpus(corpus, search_query, alg, corpus_df, search_id)

        return results
    
   
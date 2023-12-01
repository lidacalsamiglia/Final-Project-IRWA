import collections
from collections import defaultdict
import numpy as np
import math
from numpy import linalg as la
from myapp.core.utils import preprocess_tweet
import re
import array as arr_module
from myapp.search.objects import ResultItem, Document
import gensim
from gensim.models.word2vec import Word2Vec # Model for word embedding

def create_index_tfidf(corpus, num_documents):
    inv_index = defaultdict(list)
    tf = defaultdict(list)
    df = defaultdict(int)
    idf = defaultdict(float)

    for index, item in enumerate(corpus.values()):
        processed_hashtags = []
        
        for hashtag in item.hashtags:
            words = re.findall(r'[A-Z][a-z]*', hashtag)
            for i in words:
                processed_hashtags.append(preprocess_tweet(i, stemming=False, split=False))

        terms = np.union1d(item.prepro, processed_hashtags)
        doc_id = index 
        current_page_index = {}

        for position, term in enumerate(terms):
            try:
                current_page_index[term][1].append(position)
            except KeyError:
                current_page_index[term] = [doc_id, arr_module.array('I', [position])]

        norm = 0
        for term, posting in current_page_index.items():
            norm += len(posting[1]) ** 2
        norm = math.sqrt(norm)

        for term, posting in current_page_index.items():
            tf[term].append(np.round(len(posting[1]) / norm, 4))
            df[term] += 1

        for term_page, posting_page in current_page_index.items():
            inv_index[term_page].append(posting_page)

    for term in df:
        idf[term] = np.round(np.log(float(num_documents / df[term])), 4)

    return inv_index, tf, df, idf

###########################################
#### TF-DF + COSINE SIMILARITY RANKING ####
###########################################

def rank_documents(terms, docs, index, idf, tf):
    doc_vectors = defaultdict(lambda: [0] * len(terms))
    query_vector = [0] * len(terms)

    query_terms_count = collections.Counter(terms)

    for termIndex, term in enumerate(terms):
        if term not in index:
            continue

        query_vector[termIndex] = query_terms_count[term] * idf[term]
        for doc_index, (doc, postings) in enumerate(index[term]):
            if doc in docs:
                doc_vectors[doc][termIndex] = tf[term][doc_index] * idf[term]

    query_vector /= la.norm(query_vector)
    for doc in docs:
        if doc in doc_vectors:
            doc_vector = doc_vectors[doc]
            norm = la.norm(doc_vector)

            if norm > 0:
                doc_vectors[doc] = [x / norm for x in doc_vector]

    doc_scores = [[np.dot(curDocVec, query_vector), doc] for doc, curDocVec in doc_vectors.items()]
    doc_scores.sort(reverse=True)

    result_docs = [x[1] for x in doc_scores]

    if len(result_docs) == 0:
        print("No results found, try again")
        query = input()
        docs = search_tf_idf(query, index)

    return result_docs, doc_scores

def search_tf_idf(query, index, idf, tf):
    query = preprocess_tweet(query, stemming=True, split=True)
    first_term = query[0]
    try:
        docs = set(posting[0] for posting in index[first_term])
    except KeyError:
        return []
    for term in query[1:]:
        try:
            term_docs = {posting[0] for posting in index[term]}
            docs &= term_docs
        except KeyError:
            pass

    docs = list(docs)
    ranked_docs, doc_scores = rank_documents(query, docs, index, idf, tf)

    return ranked_docs, doc_scores

###############################################
#### OUR SCORE + COSINE SIMILARITY RANKING ####
###############################################

def our_rank_documents(terms, docs, index, idf, tf, corpus):
    """
    Perform the ranking of the results of a search based on our score the cosine similarity

    Argument:
    terms -- list of query terms
    docs -- list of documents, to rank, matching the query
    index -- inverted index data structure
    idf -- inverted document frequencies
    tf -- term frequencies

    Returns:
    Print the list of ranked documents
    """

    # We're only interested on the element of the docVector corresponding to the query terms the remaining elements would became 0 when multiplied to the query_vector
    doc_vectors = defaultdict(lambda: [0] * len(terms))
    query_vector = [0] * len(terms)

    # Compute the norm for the query tf
    query_terms_count = collections.Counter(terms)  # get the frequency of each term in the query.

    ll = list(corpus.values())

    for termIndex, term in enumerate(terms):  #termIndex is the index of the term in the query
        if term not in index:
            continue

        # Compute vector of the query
        query_vector[termIndex]=query_terms_count[term] * idf[term]

        # Generate doc_vectors for matching docs
        for doc_index, (doc, postings) in enumerate(index[term]):
            # OUR SCORE HERE
            if doc in docs:
                # Apply a logarithm to normalize the counts
                fav_log = np.log(ll[doc].likes + 1)  # +1 to avoid log(0)
                rt_log = np.log(ll[doc].retweets + 1)
                weighting_factor = 0.3
                # Calculate the popularity score
                popularity_score = fav_log * weighting_factor + rt_log * (1 - weighting_factor)

                doc_vectors[doc][termIndex] = tf[term][doc_index] * idf[term] * popularity_score


    # Normalize query vector and doc vectors
    query_vector /= la.norm(query_vector)
    for doc in docs:
      if doc in doc_vectors:
          doc_vector = doc_vectors[doc]

          norm = la.norm(doc_vector)

          if norm > 0:
              doc_vectors[doc] = [x / norm for x in doc_vector]

    # Calculate the score of each doc
    # compute the cosine similarity between queryVector and each docVector, which becomes dot product since vectors are normalized
    doc_scores = [[np.dot(curDocVec, query_vector), doc] for doc, curDocVec in doc_vectors.items()]
    doc_scores.sort(reverse=True)

    result_docs = [x[1] for x in doc_scores]

    if len(result_docs) == 0:
        print("No results found, try again")
        query = input()
        docs = search_tf_idf(query, index)

    return result_docs, doc_scores

def our_search(query, index, idf, tf, corpus):
    """
    output is the list of documents that contain all of the query terms.
    So, we will get the list of documents for each query term, and take the union of them.
    """
    query = preprocess_tweet(query,stemming=True, split=True)
    # initialize docs with the documents contining the first term
    first_term = query[0]
    try:
        docs = set(posting[0] for posting in index[first_term])
    except KeyError:
        # if the first term is not in index, return empty lists
        return []
    # iterate over the remaining terms and take intersection with docs, having then only the docs that contain all the terms in the query
    for term in query[1:]:
        try:
            # store in term_docs the ids of the docs that contain term
            term_docs = {posting[0] for posting in index[term]}

            # take the intersection of docs and term_docs
            docs &= term_docs
        except KeyError:
            # term is not in index
            pass

    docs = list(docs)
    ranked_docs, doc_scores = our_rank_documents(query, docs, index, idf, tf, corpus)
    return ranked_docs, doc_scores


###############################################
#### WORD2VEC + COSINE SIMILARITY RANKING ####
###############################################

def cos_similarity(v1, v2):
    dot_product = np.dot(v1, v2)
    norm_v1 = la.norm(v1)
    norm_v2 = la.norm(v2)

    if norm_v1 == 0 or norm_v2 == 0:
        return 0  # To avoid division by zero

    return dot_product / (norm_v1 * norm_v2)

# Calculate whole tweet embeddings by averaging the words in the tweet
def tweet_avg(tweet, model):
    vectors = [model.wv[word] for word in tweet if word in model.wv.key_to_index] # Obtains word vector for each word in tweet
    if not vectors:
        return None
    return np.mean(vectors, axis=0) # Average over the word vectors to obtain tweet embedding

def ranking_word2vec_cosine(terms, docs, model, corpus):
    """
    Perform ranking of the results of a search based on Word2Vec embeddings and cosine similarity.

    Arguments:
    terms -- list of query terms
    docs -- list of documents to rank, matching the query
    model -- pre-trained Word2Vec model

    Returns:
    Print the list of ranked documents
    """

    # get word2vec embeddings for the query terms
    query_embeddings = [model.wv[term] for term in terms if term in model.wv]

    # average the query embeddings to get a single vector for the query
    query_vector = np.mean(query_embeddings, axis=0)

    ll = list(corpus.values())


    doc_vectors = defaultdict(lambda: np.zeros(model.vector_size))
    for doc in docs:
        # average the document embeddings to get a single vector for the document
        doc_embedding = tweet_avg(ll[doc].prepro, model)

        if doc_embedding is not None:
            doc_vectors[doc] = doc_embedding

    # calculate cosine similarity between the query vector and each document vector
    doc_scores = [[cos_similarity(doc_vector, query_vector), doc] for doc, doc_vector in doc_vectors.items()]
    doc_scores.sort(reverse=True)

    result_docs = [x[1] for x in doc_scores]

    if len(result_docs) == 0:
        print("No results found, try again")

    return result_docs, doc_scores

def word2vec_search(query, index, model, corpus):
    """
    output is the list of documents that contain all of the query terms.
    So, we will get the list of documents for each query term, and take the union of them.
    """
    query = preprocess_tweet(query,stemming=True, split=True)

    # initialize docs with the documents contining the first term
    first_term = query[0]
    try:
        docs = set(posting[0] for posting in index[first_term])
    except KeyError:
        # if the first term is not in index, return empty lists
        return []

    # iterate over the remaining terms and take intersection with docs, having then only the docs that contain all the terms in the query
    for term in query[1:]:
        try:
            # store in term_docs the ids of the docs that contain term
            term_docs = {posting[0] for posting in index[term]}

            # take the intersection of docs and term_docs
            docs &= term_docs
        except KeyError:
            # term is not in index
            pass

    docs = list(docs)
    ranked_docs, doc_scores  = ranking_word2vec_cosine(query, docs, model, corpus)

    return ranked_docs, doc_scores

def search_in_corpus(corpus, query, alg, corpus_df, search_id):
    inv_index, tf, df, idf = create_index_tfidf(corpus, len(corpus))
    if alg == 1:
        ranked_docs, doc_scores = search_tf_idf(query, inv_index, idf, tf)
    elif alg == 2:
        ranked_docs, doc_scores = our_search(query, inv_index, idf, tf, corpus)
    else:
        model = Word2Vec(corpus_df['Preprocessed_tweet'], vector_size=100, min_count=20, window=5)
        ranked_docs, doc_scores = word2vec_search(query, inv_index, model, corpus)

    results = []
    ll = list(corpus.values())
    for rank, index in enumerate(ranked_docs):
        if 0 <= index < len(corpus):
            item: Document = ll[index]
            result_item = ResultItem(
                item.id, item.title, item.description, item.doc_date, item.url,
                "doc_details?id={}&search_id={}&param2=2".format(item.id, search_id),
                item.likes, item.retweets, rank + 1  # Adding 1 to make it 1-based index
            )
            results.append(result_item)

    return results


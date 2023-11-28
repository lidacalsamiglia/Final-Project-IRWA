import pandas as pd

from myapp.core.utils import load_json_file
from myapp.search.objects import Document
from myapp.core.utils import preprocess_tweet
import json

_corpus = {}

def load_corpus(path1, path2) -> [Document]:
    """
    Load file and transform to dictionary with each document as an object for easier treatment when needed for displaying
     in results, stats, etc.
    :param path:
    :return:
    """
    df = _load_corpus_as_dataframe(path1, path2)
    df.apply(_row_to_doc_dict, axis=1)
    return _corpus


def _load_corpus_as_dataframe(path1, path2):
    """
    Load documents corpus from file in 'path'
    :return:
    """
    data = []
    with open(path1, 'r') as file:
        for line in file:
            try:
                # Parse each line as a JSON object
                json_data = json.loads(line)
                data.append(json_data)
            except json.JSONDecodeError:
                print(f"Invalid JSON: {line}")
    tweets_df = pd.json_normalize(data)
    #print("TWEET BEFORE CLEANING: ", tweets_df)
    df_csv = pd.read_csv(path2,sep='\t', header=None)
    df_csv.columns = ['doc_id','Id']
    #tweets_df = _load_tweets_as_dataframe(json_data)
    _clean_tweets(tweets_df)
  
    # Rename columns to obtain: Tweet | Username | Date | Hashtags | Likes | Retweets | Url | Language
    corpus = tweets_df.rename(
        columns={"id": "Id", "full_text": "Tweet", "created_at": "Date",
                 "favorite_count": "Likes",
                 "retweet_count": "Retweets", "lang": "Language"})

    # select only interesting columns
    filter_columns = ["Id", "Tweet", "Date", "Likes", "Retweets", "Hashtags", "Url", "Language", "Preprocessed_tweet"]
    corpus = corpus[filter_columns]
    final_corpus = pd.merge(corpus, df_csv, on='Id', how='inner').set_index("doc_id")
    return final_corpus


def _build_tags(row):
    return [item['text'] for item in row]


def _build_url(row):
    return row[0]['url'] if pd.notna(row) and len(row) > 0 else 'no url'

def _clean_tweets(df):
    df["Hashtags"]= df['entities.hashtags'].apply(_build_tags)
    #print("HASHTAGS: ", df["Hashtags"])
    df["Url"] = df['entities.media'].apply(_build_url)
    df["Preprocessed_tweet"] = df['full_text'].apply(lambda x: preprocess_tweet(x,stemming=True, split=True))


def _row_to_doc_dict(row: pd.Series):
    _corpus[row['Id']] = Document(row['Id'], row['Tweet'][0:100], row['Tweet'], row['Date'], row['Likes'],
                                  row['Retweets'], row['Url'], row['Hashtags'], row['Preprocessed_tweet'])

 
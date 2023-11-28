import datetime
import json
from random import random
import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords   
import re
from faker import Faker

fake = Faker()


# fake.date_between(start_date='today', end_date='+30d')
# fake.date_time_between(start_date='-30d', end_date='now')
#
# # Or if you need a more specific date boundaries, provide the start
# # and end dates explicitly.
# start_date = datetime.date(year=2015, month=1, day=1)
# fake.date_between(start_date=start_date, end_date='+30y')

def get_random_date():
    """Generate a random datetime between `start` and `end`"""
    return fake.date_time_between(start_date='-30d', end_date='now')


def get_random_date_in(start, end):
    """Generate a random datetime between `start` and `end`"""
    return start + datetime.timedelta(
        # Get a random amount of seconds between `start` and `end`
        seconds=random.randint(0, int((end - start).total_seconds())), )


def load_json_file(path):
    """Load JSON content from file in 'path'

    Parameters:
    path (string): the file path

    Returns:
    JSON: a JSON object
    """

    # Load the file into a unique string
    with open(path) as fp:
        text_data = fp.readlines()[0]
    # Parse the string into a JSON object
    json_data = json.loads(text_data)
    return json_data

nltk.download('stopwords')
def preprocess_tweet(tweet, stemming, split):
    """
    Preprocess the tweet removing stop words, stemming,
    transforming in lowercase and return the tokens of the text.

    Argument:
    tweet to be preprocessed

    Returns:
    tweet - a list of tokens corresponding to the input text after the preprocessing
    """

    stemmer = PorterStemmer()
    stop_words = set(stopwords.words("english"))
    tweet = re.sub(r'https\S+','',tweet) # Removing URLs, both "http" and "https" ones.
    tweet = re.sub(r'http\S+','',tweet) # Removing URLs, both "http" and "https" ones.
    tweet = tweet.lower() ## Transform in lowercase
    tweet = re.sub(r'[^\w\s@#]', '', tweet) # Remove punctuation marks except @,#
    tweet = re.sub(r'#\S+', '', tweet) # Remove hashtags

    if split:
      tweet = tweet.split() ## Tokenize the text to get a list of terms
      tweet = [word for word in tweet if word not in stop_words]  # Eliminate the stopwords
    if stemming:
      tweet = [stemmer.stem(word) for word in tweet] # Perform stemming

    return tweet
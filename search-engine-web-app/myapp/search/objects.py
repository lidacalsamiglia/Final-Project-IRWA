import json
from datetime import datetime


class Document:
    """
    Original corpus data as an object
    """

    def __init__(self, id, title, description, doc_date, likes, retweets, url, hashtags, prepro_text):
        self.id = id
        self.title = title
        self.description = description
        self.doc_date = doc_date
        self.likes = likes
        self.retweets = retweets
        self.url = url
        self.hashtags = hashtags
        self.prepro = prepro_text

    def to_json(self):
        return self.__dict__

    def __str__(self):
        """
        Print the object content as a JSON string
        """
        return json.dumps(self)


class StatsDocument:
    """
    Original corpus data as an object
    """

    def __init__(self, id, title, description, doc_date, url, count):
        self.id = id
        self.title = title
        self.description = description
        self.doc_date = doc_date
        self.url = url
        self.count = count
        self.dwell_time = 0
    def __str__(self):
        """
        Print the object content as a JSON string
        """
        return json.dumps(self)


class ResultItem:
    def __init__(self, id, title, description, doc_date, url, doc_stats, likes, retweets, ranking):
        self.id = id
        self.title = title
        self.description = description
        self.doc_date = doc_date
        self.url = url
        self.doc_stats = doc_stats
        self.likes = likes
        self.retweets = retweets
        self.ranking = ranking
        
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'doc_date': self.doc_date,
            'ranking': self.ranking, 
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data['id'],
            title=data['title'],
            description=data['description'],
            doc_date=data['doc_date'],
            url=data.get('url', ''),  
            doc_stats=data.get('doc_stats', ''),
            likes=data.get('likes', ''),
            retweets=data.get('retweets', ''),
            ranking=data.get('ranking', '')
        )
    
class Query:
    def __init__(self, id, terms, num_results, order):
        self.id = id
        self.terms = terms
        self.num_terms = len(terms.split())
        self.num_results = num_results
        self.order = order
    
    def __str__(self):
        """
        Print the object content as a JSON string
        """
        return json.dumps(self)

    def to_dict(self):
        return {
            'id': self.id,
            'terms': self.terms,
            'num_terms': self.num_terms,
            'num_results': self.num_results
        }
   

class Visitor:
    def __init__(self, id, username, ip_address, country, city, browser, device):
        self.id = id
        self.username = username
        self.ip_address = ip_address
        self.country = country
        self.city = city
        self.browser = browser
        self.device = device
        self.start_time = datetime.utcnow()

    
    def __str__(self):
        """
        Print the object content as a JSON string
        """
        return json.dumps(self)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'ip_address': self.ip_address,
            'country': self.country,
            'city': self.city,
            'browser': self.browser,
            'device': self.device,
            'start_time': self.start_time
        }
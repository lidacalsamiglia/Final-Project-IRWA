import json


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

    def __init__(self, id, title, description, doc_date, url, count, ranking):
        self.id = id
        self.title = title
        self.description = description
        self.doc_date = doc_date
        self.url = url
        self.count = count
        self.ranking = ranking
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
            url=data.get('url', ''),  # You can use get() to provide a default value if 'url' is not present
            doc_stats=data.get('doc_stats', ''),
            likes=data.get('likes', ''),
            retweets=data.get('retweets', ''),
            ranking=data.get('ranking', '')
        )
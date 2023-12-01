import json
import random


class AnalyticsData:
    """
    An in memory persistence object.
    Declare more variables to hold analytics tables.
    """
    # statistics table 1
    # fact_clicks is a dictionary with the click counters: key = doc id | value = click counter
    fact_clicks = dict([])

    # statistics table 2
    # fact_time is a dictionary with the second counter: key = doc id | value = time spent in seconds

    fact_time = dict([])

    # statistics table 3
    fact_three = dict([])

    def save_query_terms(self, terms: str) -> int:
        print(self)
        return random.randint(0, 100000)
    
    def count_query_terms(self, terms: int) -> int:
        return (len(terms.split()))
    
    def save_click(self, doc_id: int) -> None:
        if doc_id in self.fact_clicks.keys():
            self.fact_clicks[doc_id] += 1
        else:
            self.fact_clicks[doc_id] = 1

    def save_time(self, doc_id: int, time: int) -> None:
        if doc_id in self.fact_time.keys():
            self.fact_time[doc_id] += time
        else:
            self.fact_time[doc_id] = time
    

class ClickedDoc:
    def __init__(self, doc_id, description, counter):
        self.doc_id = doc_id
        self.description = description
        self.counter = counter

    def to_json(self):
        return self.__dict__
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'doc_date': self.doc_date,
            'url': self.url,
            'count': self.count,
            'ranking': self.ranking
        }

    def __str__(self):
        """
        Print the object content as a JSON string
        """
        return json.dumps(self)
    
    def update_counter(self):
        self.counter += 1
        return self.counter
    


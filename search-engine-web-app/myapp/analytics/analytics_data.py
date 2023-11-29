import json
import random
'''import geoip2.database

def get_country(ip_address):
    reader = geoip2.database.Reader('GeoLite2-Country.mmdb')
    response = reader.country(ip_address)
    return response.country.name

def get_city(ip_address):
    reader = geoip2.database.Reader('GeoLite2-City.mmdb')
    response = reader.city(ip_address)
    return response.city.name'''

class AnalyticsData:
    """
    An in memory persistence object.
    Declare more variables to hold analytics tables.
    """
    # statistics table 1
    # fact_clicks is a dictionary with the click counters: key = doc id | value = click counter
    fact_clicks = dict([])

    # statistics table 2
    fact_two = dict([])

    # statistics table 3
    fact_three = dict([])

    def save_query_terms(self, terms: str) -> int:
        print(self)
        return random.randint(0, 100000)
    
    def count_query_terms(self, terms: int) -> int:
        return (len(terms.split()))


class ClickedDoc:
    def __init__(self, doc_id, description, counter):
        self.doc_id = doc_id
        self.description = description
        self.counter = counter

    def to_json(self):
        return self.__dict__

    def __str__(self):
        """
        Print the object content as a JSON string
        """
        return json.dumps(self)


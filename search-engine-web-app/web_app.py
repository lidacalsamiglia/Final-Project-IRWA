import os
from json import JSONEncoder

# pip install httpagentparser
import httpagentparser  # for getting the user agent as json
#import nltk
from flask import Flask, render_template, session
from flask import request

from myapp.analytics.analytics_data import AnalyticsData, ClickedDoc
from myapp.search.load_corpus import load_corpus
from myapp.search.load_corpus import _load_corpus_as_dataframe

from myapp.search.objects import Document, StatsDocument, ResultItem, Query, Visitor
from myapp.search.search_engine import SearchEngine
import json
import random
from datetime import datetime
import plotly.express as px
import pandas as pd


visitors = []
queries = []


# *** for using method to_json in objects ***
def _default(self, obj):
    return getattr(obj.__class__, "to_json", _default.default)(obj)


_default.default = JSONEncoder().default
JSONEncoder.default = _default

# end lines ***for using method to_json in objects ***


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ResultItem):
            # Convert ResultItem to a dictionary for serialization
            return obj.to_dict()
        return super().default(obj)

app = Flask(__name__)
app.json_encoder = CustomJSONEncoder


# random 'secret_key' is used for persisting data in secure cookie
app.secret_key = 'afgsreg86sr897b6st8b76va8er76fcs6g8d7'
# open browser dev tool to see the cookies
app.session_cookie_name = 'IRWA_SEARCH_ENGINE'

# instantiate our search engine
search_engine = SearchEngine()

# instantiate our in memory persistence
analytics_data = AnalyticsData()

# print("current dir", os.getcwd() + "\n")
# print("__file__", __file__ + "\n")
full_path = os.path.realpath(__file__)
path, filename = os.path.split(full_path)
print(path + ' --> ' + filename + "\n")
# load documents corpus into memory.
file_path1 = path + "/Rus_Ukr_war_data.json"
file_path2 = path + "/Rus_Ukr_war_data_ids.csv"

# file_path = "../../tweets-data-who.json"
corpus = load_corpus(file_path1, file_path2)
corpus_df = _load_corpus_as_dataframe(file_path1,file_path2)
#print("loaded corpus. first elem: ", corpus.head(1) )


# Sign In route
@app.route('/', methods=['GET', 'POST'])
def sign_in():
    '''This function is called when the user first visits the website, it
    renders the signin.html template which asks for username, password, country and city'''
    return render_template('signin.html', page_title="Sign In")

# Home URL "/"
@app.route('/index', methods=['POST'])
def index():
    '''This function is called when the user submits the sign in form, it
    gets the username from the form and stores it in the session object. It
    then renders the index.html template and passes the username as a parameter'''
    
    print("starting home url /...")
    # flask server stores the data in the session object
    session['id'] = random.randint(0, 100000)
    # store the username in the session object
    session['username'] = request.form['username']
    session['device'] = httpagentparser.detect(request.headers.get('User-Agent'))['platform']['name']
    session['browser'] = httpagentparser.detect(request.headers.get('User-Agent'))['browser']['name']
    session['user_ip'] = request.headers.get('X-Forwarded-For', request.remote_addr)
    session['country'] = request.form['country']
    session['city'] = request.form['city']
    session['query_counter'] = 0
    session['start_time'] = datetime.utcnow()

    # store in listo of objects visitor
    visitor = Visitor(session['id'], session['username'], session['user_ip'], 
                      session['country'], session['city'], session['browser'], session['device'])
    visitors.append(visitor)

    print('visitors until now: ', visitors)

    #print(session)
    

    return render_template('index.html', page_title="Welcome")



@app.route('/search', methods=['POST'])
def search_form_post():
    '''This function is called when the user submits the search form, it 
    gets the search query from the form and calls the search function from
    the search engine. It then renders the results.html template and passes'''

    # get the search query from the form
    search_query = request.form['search-query']
    search_algorithm = request.form.get('search-algorithm', 'algorithm_1')

    # store the search query in the session object
    if 'query_counter' in session:
        session['query_counter'] += 1
    else:
        session['query_counter'] = 1
    session['last_search_query'] = search_query

    search_id = analytics_data.save_query_terms(search_query)
    count_query_terms = analytics_data.count_query_terms(search_query)
    print("SEARCH ID: ", search_id)
    print("NUMBER OF QUERY TERMS: ", count_query_terms)

    # show results depending on the selected search algorithm
    if search_algorithm == 'algorithm_1':
        # Call the search function for Algorithm I
        results = search_engine.search(search_query, search_id, corpus, 1, corpus_df)
    elif search_algorithm == 'algorithm_2':
        # Call the search function for Algorithm II 
        results = search_engine.search(search_query, search_id, corpus, 2, corpus_df)
    elif search_algorithm == 'algorithm_3':
        # Call the search function for Algorithm II 
        results = search_engine.search(search_query, search_id, corpus, 3, corpus_df)
    else:
        # Handle unknown search algorithms
        return render_template('error.html', error_message="Unknown search algorithm")

    # store search information in the session object
    found_count = len(results)
    session['last_found_count'] = found_count
    serializable_results = [result.to_dict() for result in results]
    session['results'] = serializable_results

    # store data in query dataframe in same tuple with query_id as key
    query = Query(search_id, search_query, found_count, session['query_counter'])
    queries.append(query.to_dict())

    print("queries until now: ", queries)
 
    #print(session)

    return render_template('results.html', results_list=results, page_title="Results", search_algorithm=search_algorithm, found_counter=found_count)

@app.route('/doc_details', methods=['GET', 'POST'])
def doc_details():
    # getting request parameters:
    # user = request.args.get('user')

    '''print("doc details session: ")
    print(session)

    res = session["some_var"]

    print("recovered var from session:", res)'''

    # get the query string parameters from request
    clicked_doc_id = request.args["id"]
    p1 = int(request.args["search_id"])  # transform to Integer
    p2 = int(request.args["param2"])  # transform to Integer
    print("click in id={}".format(clicked_doc_id))

    analytics_data.save_click(clicked_doc_id)
    

    print("fact_clicks count for document id={} is {}".format(clicked_doc_id, analytics_data.fact_clicks[clicked_doc_id]))

    return render_template('doc_details.html')



@app.route('/stats', methods=['GET'])
def stats():

    docs = []

    for doc_id in analytics_data.fact_clicks:
        row: Document = corpus[int(doc_id)]
        count = analytics_data.fact_clicks[doc_id]

        serializable_results = session.get('results', [])
        results = [ResultItem.from_dict(result) for result in serializable_results]

        result_item = next((item for item in results if item.id == doc_id), None)

        if result_item:
            ranking = result_item.ranking
        else:
            ranking = None

        doc = StatsDocument(row.id, row.title, row.description, row.doc_date, row.url, count, ranking)
        docs.append(doc)

    
    # Create a DataFrame from StatsDocument instances
    df = pd.DataFrame([vars(doc) for doc in docs])
    df['id'] = df['id'].astype(str)

    # Create a bar chart using plotly
    fig = px.bar(df, x='id', y='count', color='ranking', labels={'id': 'Document ID', 'count': 'Visits'}, title='Clicks Stats')

    # Convert the plot to HTML
    chart_html = fig.to_html(full_html=False)

    '''for doc_id in analytics_data.fact_time:
        row: Document = corpus[int(doc_id)]x
        time = analytics_data.fact_time[doc_id]

        doc = next((item for item in docs if item.id == doc_id), None)
        if doc:
            doc.dwell_time = time'''

    docs.sort(key=lambda doc: (doc.count, doc.ranking), reverse=True)

    return render_template('stats.html', clicks_data=docs, chart_html=chart_html)



@app.route('/dashboard', methods=['GET'])
def dashboard():
    visited_docs = []
    print(analytics_data.fact_clicks.keys())
    for doc_id in analytics_data.fact_clicks.keys():
        d: Document = corpus[int(doc_id)]
        doc = ClickedDoc(doc_id, d.description, analytics_data.fact_clicks[doc_id])
        #visited_docs.append(doc)
        visited_docs.append({
            'doc_id': doc.doc_id,
            'description': doc.description,
            'counter': doc.counter,
        })

    # simulate sort by ranking
    #visited_docs.sort(key=lambda doc: doc.counter, reverse=True)
    visited_docs.sort(key=lambda doc: doc['counter'], reverse=True)


    for doc in visited_docs: print(doc)

    global visitors
    global queries
    return render_template('dashboard.html', visited_docs=visited_docs, visitors=visitors, queries=queries)


@app.route('/sentiment')
def sentiment_form():
    return render_template('sentiment.html')


@app.route('/sentiment', methods=['POST'])
def sentiment_form_post():
    text = request.form['text']
    nltk.download('vader_lexicon')
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    sid = SentimentIntensityAnalyzer()
    score = ((sid.polarity_scores(str(text)))['compound'])
    return render_template('sentiment.html', score=score)


if __name__ == "__main__":
    app.run(port=8088, host="0.0.0.0", threaded=False, debug=True)

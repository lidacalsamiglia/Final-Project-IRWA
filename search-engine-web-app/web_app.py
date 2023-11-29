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

from myapp.search.objects import Document, StatsDocument, ResultItem
from myapp.search.search_engine import SearchEngine
import json

from flask_sqlalchemy import SQLAlchemy

from myapp.analytics.data_storage import Session, Click, Request



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
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

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
print("loaded corpus. first elem:", list(corpus.values())[0])
corpus_df = _load_corpus_as_dataframe(file_path1,file_path2)
#print("loaded corpus. first elem: ", corpus.head(1) )


# Sign In route
@app.route('/', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        password = request.form['password']

        # Validate the username and password (implement your authentication logic)

        # For this example, let's assume a simple check
        new_session = Session(username=username, start_time=datetime.utcnow())
        db.session.add(new_session)
        db.session.commit()

        
    return render_template('signin.html')

# Home URL "/"
@app.route('/index', methods=['POST'])
def index():
    print("starting home url /...")

    # flask server creates a session by persisting a cookie in the user's browser.
    # the 'session' object keeps data between multiple requests
    session['some_var'] = "IRWA 2023 home"

    user_agent = request.headers.get('User-Agent')
    print("Raw user browser:", user_agent)

    user_ip = request.remote_addr
    agent = httpagentparser.detect(user_agent)

    print("Remote IP: {} - JSON user browser {}".format(user_ip, agent))

    print(session)

    return render_template('index.html', page_title="Welcome")

'''@app.route('/search', methods=['POST'])
def search_form_post():
    search_query = request.form['search-query']

    session['last_search_query'] = search_query

    search_id = analytics_data.save_query_terms(search_query)

    results = search_engine.search(search_query, search_id, corpus)

    found_count = len(results)
    session['last_found_count'] = found_count

    print(session)

    return render_template('results.html', results_list=results, page_title="Results", found_counter=found_count)'''

@app.route('/search', methods=['POST'])
def search_form_post():
    search_query = request.form['search-query']
    search_algorithm = request.form.get('search-algorithm', 'algorithm_1')

    session['last_search_query'] = search_query

    search_id = analytics_data.save_query_terms(search_query)
    print("SEARCH ID: ", search_id)

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

    found_count = len(results)
    session['last_found_count'] = found_count
    serializable_results = [result.to_dict() for result in results]
    session['results'] = serializable_results
   
    print(session)

    return render_template('results.html', results_list=results, page_title="Results", search_algorithm=search_algorithm, found_counter=found_count)

@app.route('/doc_details', methods=['GET'])
def doc_details():
    # getting request parameters:
    # user = request.args.get('user')

    print("doc details session: ")
    print(session)

    res = session["some_var"]

    print("recovered var from session:", res)

    # get the query string parameters from request
    clicked_doc_id = request.args["id"]
    p1 = int(request.args["search_id"])  # transform to Integer
    p2 = int(request.args["param2"])  # transform to Integer
    print("click in id={}".format(clicked_doc_id))

    # store data in statistics table 1
    if clicked_doc_id in analytics_data.fact_clicks.keys():
        analytics_data.fact_clicks[clicked_doc_id] += 1
    else:
        analytics_data.fact_clicks[clicked_doc_id] = 1

    print("fact_clicks count for id={} is {}".format(clicked_doc_id, analytics_data.fact_clicks[clicked_doc_id]))

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

    docs.sort(key=lambda doc: (doc.count, doc.ranking), reverse=True)

    return render_template('stats.html', clicks_data=docs)



@app.route('/dashboard', methods=['GET'])
def dashboard():
    visited_docs = []
    print(analytics_data.fact_clicks.keys())
    for doc_id in analytics_data.fact_clicks.keys():
        d: Document = corpus[int(doc_id)]
        doc = ClickedDoc(doc_id, d.description, analytics_data.fact_clicks[doc_id])
        visited_docs.append(doc)

    # simulate sort by ranking
    visited_docs.sort(key=lambda doc: doc.counter, reverse=True)

    for doc in visited_docs: print(doc)
    return render_template('dashboard.html', visited_docs=visited_docs)


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

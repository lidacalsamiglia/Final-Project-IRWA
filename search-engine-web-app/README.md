# Search Engine with Web Analytics
# IRWA Final Project

This projects contains the Flask files for running our web application.

## To download this repo locally

Open a terminal console and execute:

```
cd <your preferred projects root directory>

git clone https://github.com/lidacalsamiglia/Final-Project-IRWA/tree/c9916b4356c32c093bd1fba3f93fd493982ee200/search-engine-web-app

```



## Starting the Web App

```bash
python -V
# Make sure we use Python 3

cd search-engine-web-app

```

## Virtualenv for the project (first time use)
### Install virtualenv
Having different version of libraries for different projects.  
Solves the elevated privilege issue as virtualenv allows you to install with user permission.

In the project root directory execute:
```bash
pip3 install virtualenv
virtualenv --version
```
virtualenv 20.10.0

### Prepare virtualenv for the project
In the root of the project folder run:
```bash
virtualenv .
```

If you list the contents of the project root directory, you will see that it has created several sub-directories, including a bin folder (Scripts on Windows) that contains copies of both Python and pip. Also, a lib folder will be created by this action.

The next step is to activate your new virtualenv for the project:

```bash
source bin/activate
```

or for Windows...
```cmd
myvenv\Scripts\activate.bat
```

This will load the python virtualenv for the project.

### Installing Flask and other packages in your virtualenv
```bash
pip install Flask pandas nltk faker json os httpagentparser random datetime plotly gensim certifi
pip install collections numpy math re array flask_sqlalchemy
python -m nltk.downloader stopwords
```

## Running the project
```bash
python web_app.py
```
The above will start a web server with the application:
```
 * Serving Flask app 'web-app' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:8088/ (Press CTRL+C to quit)
```
Open Web app in your Browser:  
[http://127.0.0.1:8088/](http://127.0.0.1:8088/) or [http://localhost:8088/](http://localhost:8088/)


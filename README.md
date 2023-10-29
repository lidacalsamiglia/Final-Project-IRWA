# Final IRWA Project 2023


## Overview
For the subject "Information Retrieval and Web Analysis" taught by the UPF University, we conducted a project with the aim of building a search engine implementing different indexing and ranking algorithms. We specifically worked with Russian-Ukrainian tweets. 

The project is structured in the following way:

| Part | Topic
|----------|----------
| Part 1| Text Processing and Exploratory Data Analysis |
| Part 2 | Indexing and Evaluation |
| Part 3 | Ranking |
| Part 4 | User Interface and Web Analytics |

(Note: This README is cumulative, meaning we will add the information of each part as we complete it.)


## Part 1: Text Processing and Exploratory Data Analysis

This part is divided in two steps: 
1. **Text Preprocessing**: this initial step involves preprocessing the tweets. This includes the removal of stop words, tokenization, elimination of punctuation marks, stemming, and any other necessary techniques to enhance the data quality. Our goal is to refine the tweets for meaningful analysis, ensuring accuracy and relevance in the subsequent stages of the project. 
2. **Exploratory Data Analysis**: in this step the goal is to gain insights from the preprocessed dataset. This involved a thorough examination and statistical analysis of the content, such as word counting distribution, average sentence length, vocabulary size, identification of the most retweeted tweets, creation of word clouds to visualize the most frequent words, sentiment analysis and social network analysis. By conducting this comprehensive analysis, we uncovered patterns and information related to the Russo-Ukrainian War tweets.

## Prerequisites

Before running the Python Notebook, ensure that you have the following prerequisites installed on your system:

- **Python**: Make sure you have Python installed on your system. You can download Python from the [official Python website](https://www.python.org/).

- **Python Libraries**:

    - **pandas**: Install pandas, a popular data manipulation library, by running:
      ```bash
      pip install pandas
      ```

    - **nltk**: Install the Natural Language Toolkit (NLTK) for natural language processing tasks:
      ```bash
      pip install nltk
      ```

    - **matplotlib**: Install matplotlib for data visualization:
      ```bash
      pip install matplotlib
      ```

    - **numpy**: Install numpy for numerical and mathematical operations:
      ```bash
      pip install numpy
      ```

    - **seaborn**: Install seaborn for enhanced data visualization:
      ```bash
      pip install seaborn
      ```

    - **WordCloud**: Install the WordCloud library for creating word clouds:
      ```bash
      pip install wordcloud
      ```

    - **networkx**: Install networkx for graph-based analysis:
      ```bash
      pip install networkx
      ```


## How to Use
### Running Locally

If you want to run this python notebook on your local machine, follow these steps:

1. **Clone the Repository**:
   ```
   git clone https://github.com/lidacalsamiglia/Final-Project-IRWA.git
   ```

2. **Install Dependencies:**
Ensure you have the required dependencies installed as mentioned in the "Prerequisites" section.

4. **Run the Jupyter Notebook**: 
- If you are using Visual Studio: 
  - Open the project file.
  - Use the "Run" or "Execute" option provided by your IDE.
- If you are using Jupyter Notebook:
  - Open the Jupyter Notebook file (.ipynb) associated with the project.
  - You can run individual code cells by clicking the play button in each cell or run all cells at once selecting "Run All".


### Running in Google Colab
You will need to download or clone the project file from the source repository, or you can manually upload it to Google Colab.
To run this project in Google Colab, follow these steps:


1. **Access Google Colab**: Go to [Google Colab](https://colab.research.google.com/).

2. **Log in with Google Account**: You'll need a Google account to use Colab. Log in with your Google credentials if you aren't already logged in.

3. **Open the Notebook**: Click on "File" and then select "Open notebook." Upload a the notebook from your computer or access from your Google Drive.

4. **Mount Google Drive**: the notebook requires access to csv of data ids, and JSON file that contains a set of tweets related to the Russo- Ukrainian War the tweets in your Google Drive. You can mount your Google Drive by adding the following code at the beginning of your notebook:
   
   ```python
   from google.colab import drive
   drive.mount('/content/drive')

5. **Run the Project**:
You can run individual code cells by clicking the play button in each cell or run all cells at once using the "Runtime" menu.
   
   
## Part 2: Indexing and evaluation

This part is also divided in two steps: 
1. **Indexing**: this step involves the organization and structuring of the dataset in order to ensure efficient information retrieval. This includes creating an inverted index, defining proposed test queries to check our index and ranking the results by implementing TF-IDF mechanism. 
2. **Evaluation**: in this step the goal is ensure that our implementation provides the user with the most relevant information. We use different evaluation metrics to understand the mechanism's effectiveness such as: Precision@K, Recall@K, Average Precision@K, F1-Score@K, Mean Average Precision, Mean Reciprocal Rank, Normalized Discounted Cumulative Gain.  

- **New Python Libraries**:
There are new libraries that will be used for this second part of the project:
    - **gensim**: Install gensim for document similarity analysis:
      ```bash
      pip install gensim
      ```
    - **sklearn**: Install sklearn to use TSNE for dimensionality reduction:
      ```bash
      pip install sklearn
      ```



## Authors

Lida Calsamiglia, Patricia Castelijns, Francesca Mees

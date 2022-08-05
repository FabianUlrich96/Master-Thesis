# Comment Data Preparation & Analysis

## data_preparation.ipynb
Reads raw comment and reply files and:
* Removes entries with less than 10 characters. 
* Labels spam using the UCI spam/ham dataset and Support Vector Machine (SVM)

## vader_sentiment.ipynb
* Reads prepared comments and replies dataframe and labels it with a Vader score.

## btm-topic-modelling.ipynb
* File for biterm topic modelling.
* Merge videos to topics.
* Merge video topics with comments and replies file.

## topic-modelling-benchmark.csv
* Benchmark to evaluate the number of topics.

## topic_map.xlsx
* Label for topic numbers. 

## SentimentTool_Error-Rate.ipynb
* Jupyter Notebook for evaluating [Vader Sentiment](https://github.com/cjhutto/vaderSentiment).
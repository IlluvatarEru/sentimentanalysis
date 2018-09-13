# Sentiment Analysis

This project is meant to perform sentiment analysis on text documents using two different approaches: <br />
    - Bag of words <br />
    - Machine Learning
    
As of today (12th of September 2018) only the bag of words approach is implemented.

## Bag of words

This approach is based on lists of positive and negative words.

First, all the words in the documents are lemmatized (eg: "leaves" -> "leaf").<br />
Then, it will compute a score for each word in the document:<br />
    - if the word is present in the list of positive words, its score is 1 (eg: "good")<br />
    - if the word is present in the list of negative words, its score is -1 (eg: "bad")<br />
    - otherwise it is 0<br />
    
Then the score of the word is updated to take into account the context:
    - if there is a diminisher in the previous words it will multiply the score by 0.5 ("This is a partially nad"; "bad" will have a score of: -1 * 0.5 = -0.5 ) <br />
    - if there is an intensifier in the previous words it will multiply the score by 2 (eg: "It is very bad"; "bad" will have a score of: -1 * 2 = -2) <br />
    - if there is a negation in the previous words it will multiply the score by -1 (eg: "It is not bad"; "bad" will have a score of: -1 * -1 = 1) <br />

The user has the choice of different list of words:<br />
    - Loughan and McDonald: (https://sraf.nd.edu/textual-analysis/resources/#LM%20Sentiment%20Word%20Lists)<br />
    - The Harvard Inquirer: (http://www.wjh.harvard.edu/~inquirer/) (to be implemented)<br />
    
*Example:*

get_sentiment_doc("He is a good developper, I like the way he adds insightful comments in his code")<br />
-> 2

## Machine Learning

To be implemented.

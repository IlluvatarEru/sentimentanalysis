# -*- coding: utf-8 -*-
"""
Created on Sat Jul  21 17:42:44 2018

@author: Arthurim
"""

import pandas as pd
from nltk import word_tokenize, pos_tag
from nltk.stem import WordNetLemmatizer
import os
from nltk.corpus import stopwords

PATH = os.path.dirname(os.path.realpath(__file__))
    
def get_lemma_text(txt):
    """
    Returns a list of the lemma for each word in a text
    
    :param txt: (string) the text
    :return: (list of strings) the lemmas
    """
    
    wnl = WordNetLemmatizer()
    return [wnl.lemmatize(i,j[0].lower()) if j[0].lower() in ['a','n','v'] else wnl.lemmatize(i) for i,j in pos_tag(word_tokenize(txt))]
    

def word_score(word,positive_words,negative_words):
    """
    Returns the sentiment score of a given word: 1 if positive, -1 if negative and else 0
    
    :param word: (string) the word to get the sentiment of
    :param positive_words: (list of strings) list of positive words
    :param negative_words: (list of strings) list of negative words
    :return: (int) score of the word
    """
    
    if word in positive_words:
        return 1
    elif word in negative_words:
        return -1
    else:
        return 0
    

def context_score(word_score, context, negations, diminishers, intensifiers):
    """
    Returns the modified word score based on the context around the word:
        - if a negation preceeds the word, its score is multiplied by -1
        - if a diminishier preceeds the word, its score is mutliplied by 0.5
        - if an intensifier preceeds the word, its score is mutliplied by 2
        
    :param word_score: (float) the word score
    :param context: (list of strings) the words preceeding the word of which we get the sentiment score
    :param negations: (list of strings) list of words comprising of negations
    :param diminishers: (list of strings) list of words comprising of diminshier words
    :param intensifiers: (list of strings) list of words comprising of intensifier words
    :return: (float) the modified score
    """
    
    for word in context:
        if word in negations:
            word_score*=-1
        if word in diminishers:
            word_score*=0.5
        elif word in intensifiers:
            word_score*=2
    return word_score


def is_stop_word(word):
    """
    Returns True if the word is a stop word, else False
    
    :param word: (string)
    :return: (boolean)
    """
    if word in stopwords.words("english"):
        return True
    else:
        return False        
    
      
def get_sentiment_doc(doc,positive_words, negative_words,negations,diminishers, intensifiers,log=False):
    """
    Returns the sentiment of a document following a bag of words approach.
        - the document is first lemmatized
        - then for each positive (negative) word the score is incremented by 1 (-1)
        - the word score is multiplied by -1 if there is a negation among the three previous words (eg: "this is not bad"; "bad" will have a score of 1 * -1 = 1)
        - the word score is multiplied by 2 (0.5) if there is an intensifer (diminisher) among the previous three words (eg: "this is very bad"; "bad" will have a score of 2 * -1 = -2)
    
    
    :param doc: (string) the document text to analyze
    :param positive_words: (list of strings) the list of positive words (eg: "good")
    :param negative_words: (list of strings) the list of negative words (eg: "bad")
    :param negations: (list of strings) the list of negations (eg: "not")
    :param diminishers: (list of strings) the list of diminishers (eg: "negligibly")
    :param intensifiers: (list of strings) the list of intensifiers (eg: "very")
    :param log: (boolean) if True prints the document, the score of each word, the list of words with negative/positive score
    :return: the sentiment score of the document
    """
    
    doc = get_lemma_text(doc)
    if log==True:
        print(doc)
    pos = []
    neg = []
    net = []
    s = 0
    sp = 0
    sn = 0
    for i in range(3, len(doc)):
        word = doc[i]
        if not is_stop_word(word):
            if log == True:
                print(word)
            context = doc[i-3:i]
            if log == True:
                print(context)
            s_w = context_score(word_score(word,positive_words,negative_words),context, negations, diminishers, intensifiers)
            if log == True:
                print(s_w)
            if s_w>0:
                pos.append(word)
                sp+=s_w
            elif s_w <0:
                neg.append(word)
                sn+=s_w
            else:
                net.append(word)
            s+=s_w
    if log == True:
        print("Words scored as positive: ", pos)
        print("Words scored as negative: ", neg)
        print("Words scored as neutral: ", net)
        print("Total positive score :", sp)
        print("Total negative score :", sn)
        print("Total document score :", s)
    return s


def load_list_of_words(choice):
    """
    Returns the list of words to use for sentiment analysis, the user can choose to use the positive/negative words from:
        - Loughan and McDonald
        - the Harvard Inquirer
        - both
        
    :param choice: (string) must be "LM" for the Loughran and McDonald list of words, "HI" for the Harvard Inquirer list of words or "LMHI" for a combination of both
    :return: (list of 5 lists of strings) the different lists of words to use for sentiment analysis
    """
    
    if choice == "LM":
        positive_words = pd.read_csv(PATH +"\\Data\\"+ "loughranAndMcDonald_positive_words_lemmatized" +".csv",header=None)[0].values.tolist()
        negative_words = pd.read_csv(PATH +"\\Data\\"+ "loughranAndMcDonald_negative_words_lemmatized" +".csv",header=None)[0].values.tolist()
    #elif choice == "HI":
    #elif choice == "LMHI":
    else:
        raise ValueError("Unknown choice parameter, must be 'LM', 'HI' or 'LMHI'.")
    negations = pd.read_csv(PATH +"\\Data\\"+ "negations_lemmatized" +".csv",header=None)[0].values.tolist()
    diminishers = pd.read_csv(PATH +"\\Data\\"+ "diminishers_lemmatized" +".csv",header=None)[0].values.tolist()
    intensifiers = pd.read_csv(PATH +"\\Data\\"+ "intensifiers_lemmatized" +".csv",header=None)[0].values.tolist()
    return positive_words, negative_words, negations, diminishers, intensifiers

def main():
    positive_words, negative_words, negations, diminishers, intensifiers = load_list_of_words("LM")
    score = get_sentiment_doc("This is a very bad programmer, he cannot comment his code properly, he is the worst developper I ever saw!",positive_words, negative_words,negations,diminishers, intensifiers, log = True)
    print(score)

if __name__ == '__main__':
    main()





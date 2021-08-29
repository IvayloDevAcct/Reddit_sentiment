import os

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords as sw
from nltk.stem.porter import PorterStemmer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import math


class TextAnalyser:
    def __init__(self, lang, ):
        self.__language = lang
        self.positive = self.load_positive_words()
        self.negative = self.load_negative_words()
        self.vader = SentimentIntensityAnalyzer()

    def load_positive_words(self):
        """Load predefined lists of words (ideally from database)"""

        with open(os.path.dirname(os.getcwd()) + '\\Reddit_sentiment\\files\\positive_words.txt') as p_file:
            return [line.rstrip(",\n") for line in p_file if line]

    def load_negative_words(self):
        with open(os.path.dirname(os.getcwd()) + '\\Reddit_sentiment\\files\\negative_words.txt') as n_file:
            return [line.rstrip(",\n") for line in n_file if line]

    def process_text(self, text):
        """Parses the text into words and filters out the stopwords"""

        ingore_words = set(sw.words(self.__language))
        punctuations = "?:!.,;[]()'%&/*''"

        words = word_tokenize(text.lower())

        return [word for word in words if word not in ingore_words and word not in punctuations
                and not word.isnumeric()]

    def score_post(self, post, comments):
        """Applies scores to the words derived from the text based on predefined set of positive / negative words"""

        words = post + comments

        # Count number of positive words
        positive_words_count = len([w for w in words if w in self.positive])

        # Count number of negative words
        negative_words_count = len([w for w in words if w in self.negative])

        # Calculate the score
        if words:
            score = ((positive_words_count - negative_words_count) / len(words)) * 100

            # Normalize the scores similarly to Vader in order for the two scores to be comparable
            normalized_score = score/math.sqrt((score * score) + 10)

            return {
                "overall": normalized_score,
                "positive": positive_words_count,
                "negative": negative_words_count,
                "words_count": len(words)
                }

    def score_post_vader(self, text):
        """Applies scores to the words derived from the text using the vader Sentiment intensity analyser of nltk"""
        return self.vader.polarity_scores(text)['compound']

    @staticmethod
    def stem_words(words):
        """Reduces the words to stems"""
        stemmer = PorterStemmer()

        return [stemmer.stem(word) for word in words]





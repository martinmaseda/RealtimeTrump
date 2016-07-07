import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
from nltk.stem.porter import *
from nltk.corpus import twitter_samples
import pickle


def get_words_from_sentence(list_of_tokenized_words):
    stemmer = PorterStemmer()
    list_of_tokenized_words = [cap_word.lower() for cap_word in list_of_tokenized_words]
    list_of_tokenized_words = [each_word for each_word in list_of_tokenized_words if each_word not in stopwords.words('english')]
    list_of_tokenized_words = [each_word for each_word in list_of_tokenized_words if each_word not in [",", ".", "..", "...", ":", "?", "!", "\'", "\"", "#", "-", "_", "(", ")"]]
    list_of_tokenized_words = [stemmer.stem(each_word) for each_word in list_of_tokenized_words]
    print(list_of_tokenized_words)
    return list_of_tokenized_words


def word_feats(words):
    return dict([(word, True) for word in get_words_from_sentence(words)])


def tokenize_sentence_into_list_of_words(sentence):
    tknzr = TweetTokenizer()
    list_of_tokenized_words = tknzr.tokenize(sentence)
    return list_of_tokenized_words

negative_tokenizedWordsFromTwitter = twitter_samples.tokenized('negative_tweets.json')
positive_tokenizedWordsFromTwitter = twitter_samples.tokenized('positive_tweets.json')

negfeats = [(word_feats(f), 'neg') for f in negative_tokenizedWordsFromTwitter]
posfeats = [(word_feats(f), 'pos') for f in positive_tokenizedWordsFromTwitter]

negcutoff = int(len(negfeats)*3/4)
poscutoff = int(len(posfeats)*3/4)

trainfeats = negfeats[:negcutoff] + posfeats[:poscutoff]
testfeats = negfeats[negcutoff:] + posfeats[poscutoff:]
print('train on %d instances, test on %d instances' % (len(trainfeats), len(testfeats)))

classifier = NaiveBayesClassifier.train(trainfeats)
print('accuracy:', nltk.classify.util.accuracy(classifier, testfeats))
print(classifier.show_most_informative_features())

prediction = classifier.prob_classify(word_feats(tokenize_sentence_into_list_of_words("The first nine elements of the list are attributes of the Tweet, while the last one")))

print(prediction._prob_dict)
print(prediction.max())
print(type(prediction.max()))

f = open('./my_tweet_classifier.pickle', 'wb')
pickle.dump(classifier, f)
f.close()

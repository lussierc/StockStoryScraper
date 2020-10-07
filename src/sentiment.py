import spacy
from spacy import displacy
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
from sklearn.svm import LinearSVC
import string
import en_core_web_sm
nlp = en_core_web_sm.load()
from spacy.lang.en.stop_words import STOP_WORDS
stopwords = list(STOP_WORDS)
print(len(stopwords))

#TRAIN
data_yelp = pd.read_csv('data/data.txt', sep='\t', header= None)
columnName = ['Review','Sentiment']
data_yelp.columns = columnName
print(data_yelp.head(5))
print(data_yelp.shape)

data = data_yelp

punct = string.punctuation
print(punct)


def dataCleaning(sentence):
  doc = nlp(sentence)
  tokens = []
  for token in doc:
    if token.lemma_ != '-PRON-':
      temp = token.lemma_.lower().strip()
    else:
      temp = token.lower_
    tokens.append(temp)
  clean_tokens = []
  for token in tokens:
    if token not in punct and token not in stopwords:
      clean_tokens.append(token)
  return clean_tokens

test = dataCleaning("Today we are having heavy rainfall, We recommend you to stay at your home and be safe, Do not start running here and there")

print(test)

X = data['Review']
y = data['Sentiment']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)
print(X_train.shape,y_test.shape)


#preparing the model:
tfidf = TfidfVectorizer(tokenizer = dataCleaning)
svm = LinearSVC()
steps = [('tfidf',tfidf),('svm',svm)]
pipe = Pipeline(steps)

pipe.fit(X_train,y_train)

y_pred = pipe.predict(X_test)
print(classification_report(y_test,y_pred))
print("\n\n")
print(confusion_matrix(y_test,y_pred))

print("THE REAL TEST", pipe.predict(["I am testing a sad bad sentence here"]))

from stop_words import get_stop_words
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import numpy as np
from nltk import FreqDist
from string import punctuation
from uk_stemmer import UkStemmer
import re

stopwords = set(get_stop_words('ukrainian'))
stopwords.update(['бо', 'із', 'а', 'те', 'й', 'би', 'всі', 'яку', 'уже', 'не', 'які', 'очі', 'усі'])

for code in range(1040, 1111):
    stopwords.update(chr(code))


def preprocess_text(text):
    REGEXES = [re.compile("(\.)|(\;)|(\:)|(\!)|(\')|(\?)|(\,)|(\")|(\()|(\))|(\[)|(\])"),
               re.compile("(<br\s*/><br\s*/>)|(\-)|(\/)"),
               re.compile("як\S+"),
               re.compile("\s?—\s?")]
    for regex in REGEXES:
        text = regex.sub(" ", text)

    text = [w for w in text.lower().split() 
            if not w in stopwords 
            and w != " " and not w in punctuation]
            
    return text


def generate_wordcloud(text, title):
    wordcloud = WordCloud(width=1200, height=800,
                          relative_scaling=1.0, stopwords=stopwords).generate(text)

    fig = plt.figure(figsize=(15, 10))
    plt.axis('off')
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.title(title)
    plt.rcParams['toolbar'] = 'None'
    plt.show()

def generate_frequency(text, title, lemmatize=False):
    words = preprocess_text(text)
    number_of_words = len(words)
    stemmer = UkStemmer()

    if lemmatize:
        for i in range(len(words)):
            words[i] = stemmer.stem_word(words[i])

    freq = FreqDist(words)
    most_common = freq.most_common(10)

    print('\n')
    print('Частота входження слів: ')
    for key_val in most_common:
        print(key_val[0] + ": 1/" + str(int(number_of_words/key_val[1])))


    keys = [key_val[0] for key_val in most_common]
    values = [key_val[1] for key_val in most_common]
    plt.figure(figsize=(15, 10))
    index = np.arange(len(keys))
    plt.barh(index, values)
    plt.xlabel('Кількість входжень', fontsize=12)
    plt.ylabel('Слово', fontsize=12)
    plt.yticks(index, keys, fontsize=12, rotation=30)
    if lemmatize:
        plt.title('10 найчастотніших слів (з лемматизацією) у творі "' + title + '"')
    else:
        plt.title('10 найчастотніших слів у творі "' + title + '"')
    for index, value in enumerate(values):
        plt.text(value, index, str(value))
    plt.show()

def number_of_paragraphs(text, title):
    count = len(text.split("\n"))
    print("Кількість абзаців у творі \"" + title + "\": " + str(count))

def number_of_sentences(text, title):
    count = len(re.split(r'[.!?]+', text))
    print("Кількість речень у творі \"" + title + "\": " + str(count))

def number_of_words(text, title):
    count = len(preprocess_text(text))
    print("Кількість слів у творі \"" + title + "\": " + str(count))

def number_of_letters(text, title):
    count = 0
    for letter in text:
        if ord(letter) > 1040 and ord(letter) < 1111:
            count +=1
    print("Кількість букв у творі \"" + title + "\": " + str(count))

for item in [['./data/Idoly padyt.txt', 'Ідоли падуть'], ['./data/Idu na vas.txt', 'Іду на вас']]:
    with open(item[0], 'r') as file:
        print('\n')
        print(('started working with:  ' + item[0]).center(80, '*'))
        print('\n')
        data = file.read()
        number_of_paragraphs(data, item[1])
        number_of_sentences(data, item[1])
        number_of_words(data, item[1])
        number_of_letters(data, item[1])
        generate_wordcloud(data, item[1])
        generate_frequency(data, item[1])
        generate_frequency(data, item[1], True)
        print('\n')
        print((' finished working with:  ' + item[0]).center(80, '*'))
        print('\n')
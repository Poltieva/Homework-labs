import pymorphy2
import sqlite3
import tokenize_uk
from string import Template

morph_analyzer = pymorphy2.MorphAnalyzer(lang='uk')

with open('C:/Users/user/Desktop/Навчання/Тексти/Holubyi_olen.txt', 'r') as file:
    text = file.read()
sentences = tokenize_uk.tokenize_sents(text)

db = sqlite3.connect('dictionary.db')
cursor = db.cursor()
cursor.execute("""DROP TABLE sentences;""")
cursor.execute("""DROP TABLE morphs;""")
cursor.execute("""DROP TABLE word_forms;""")
cursor.execute("""DROP TABLE lemmas;""")
cursor.execute("""CREATE TABLE sentences
           (index_of_sent INTEGER PRIMARY KEY,
           sentence VARCHAR(100) NOT NULL);""")
cursor.execute("""CREATE TABLE morphs
           (position_in_text INTEGER PRIMARY KEY,
           morph VARCHAR(20) NOT NULL);""")
cursor.execute("""CREATE TABLE word_forms 
                (word_form VARCHAR(20) PRIMARY KEY,
                lemma VARCHAR(20) NOT NULL,
                num_of_ocurrences INTEGER NOT NULL);""")
cursor.execute("""CREATE TABLE lemmas
                (lemma VARCHAR(20) PRIMARY KEY NOT NULL,
                num_of_ocurrences INTEGER NOT NULL);""")

word_forms = {}
count = 1
for index, sentence in enumerate(sentences):
    t = Template('INSERT INTO sentences VALUES ($index , "$sentence");')
    command = t.substitute(index=index + 1, sentence=sentence)
    cursor.execute(command)
    tokens = tokenize_uk.tokenize_words(sentence)
    for token in tokens:
        if token.isalpha():
            t = Template('INSERT INTO morphs VALUES ($count, "$token");')
            command = t.substitute(count=count, token=token)
            cursor.execute(command)
            count += 1
            if token not in word_forms.keys():
                word_forms[token] = 1
            else:
                word_forms[token] += 1

lemmas = {}
for word_form, num_of_ocurrences in word_forms.items():
    lemma = morph_analyzer.parse(word_form)[0].normal_form
    t = Template('INSERT INTO word_forms VALUES ("$word_form", "$lemma", $num);')
    command = t.substitute(word_form=word_form, lemma=lemma, num=num_of_ocurrences)
    cursor.execute(command)

    if lemma not in lemmas.keys():
        lemmas[lemma] = num_of_ocurrences
    else:
        lemmas[lemma] += num_of_ocurrences

for lemma, num_of_ocurrences in lemmas.items():
    command = 'INSERT INTO lemmas VALUES ("' + lemma + '" ,' + str(num_of_ocurrences) + ");"
    cursor.execute(command)

db.commit()
db.close()

# Корпус 156 481‬ слів, 11 339 речень

import pymorphy2
import os
import docx2txt
import sqlite3
import tokenize_uk
from string import Template
import time

start = time.time()
texts = []
with os.scandir('C:/Users/user/Desktop/Навчання/Тексти/') as entries:
    for entry in entries:
        text = docx2txt.process("C:/Users/user/Desktop/Навчання/Тексти/" + entry.name)
        sentences = tokenize_uk.tokenize_sents(text)
        texts.append(sentences)

db = sqlite3.connect('dictionary.db')
cursor = db.cursor()

word_forms = {}
count = 1
index = 1
for sents in texts:
    for sentence in sents:
        sentence = sentence.replace("\n", " ").replace("\"", "")
        t = Template('INSERT INTO sentences VALUES ($index_of_sent , "$sentence");')
        command = t.substitute(index_of_sent=index, sentence=sentence)
        cursor.execute(command)
        index += 1
        tokens = tokenize_uk.tokenize_words(sentence)
        for token in tokens:
            if token.isalnum():
                t = Template('INSERT INTO morphs VALUES ($count, "$token", $index_of_sent);')
                command = t.substitute(count=count, token=token, index_of_sent=index + 1)
                cursor.execute(command)
                count += 1
                if token not in word_forms.keys():
                    word_forms[token] = 1
                else:
                    word_forms[token] += 1

morph_analyzer = pymorphy2.MorphAnalyzer(lang='uk')
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
    t = Template('INSERT INTO lemmas VALUES ("$lemma", "$num_of_ocurrences");')
    command = t.substitute(lemma=lemma, num_of_ocurrences=num_of_ocurrences)
    cursor.execute(command)

db.commit()
db.close()
end = time.time()
print("Process finished in", end - start, "seconds")

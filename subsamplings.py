# Вибірка 20 000 слів, 20 підвибірок

import sqlite3
import random
from string import Template

db = sqlite3.connect('dictionary.db')
cursor = db.cursor()

count = 0
for el in cursor.execute("""SELECT COUNT(index_of_sent) FROM sentences;"""):
    count = el[0]


def subsampling(cnt=0):
    i = 0
    while i < 1000:
        t = Template("""SELECT sentence FROM sentences
                        WHERE index_of_sent = $rand;""")
        command = t.substitute(rand=random.randint(1, count+1))
        sentence = cursor.execute(command)
        for sent in sentence:
            words = sent[0].split(" ")
            i += len(words)
            with open("sampling" + str(cnt) + ".txt", "a", encoding="utf-8") as file:
                file.write(sent[0])
                file.write("\n")


for j in range(20):
    subsampling(j)
db.commit()
db.close()
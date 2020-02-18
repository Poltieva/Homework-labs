import sqlite3

db = sqlite3.connect('dictionary.db')
cursor = db.cursor()

cursor.execute("""DROP TABLE sentences;""")
cursor.execute("""DROP TABLE morphs;""")
cursor.execute("""DROP TABLE word_forms;""")
cursor.execute("""DROP TABLE lemmas;""")
cursor.execute("""CREATE TABLE sentences
           (index_of_sent INTEGER PRIMARY KEY NOT NULL,
           sentence TEXT NOT NULL);""")
cursor.execute("""CREATE TABLE morphs
           (position_in_text INTEGER PRIMARY KEY NOT NULL,
           morph VARCHAR(20) NOT NULL,
           index_of_sent INTEGER NOT NULL);""")
cursor.execute("""CREATE TABLE word_forms
                (word_form VARCHAR(20) PRIMARY KEY NOT NULL,
                lemma VARCHAR(20) NOT NULL,
                num_of_ocurrences INTEGER NOT NULL);""")
cursor.execute("""CREATE TABLE lemmas
                (lemma VARCHAR(20) PRIMARY KEY NOT NULL,
                num_of_ocurrences INTEGER NOT NULL);""")

db.commit()
db.close()
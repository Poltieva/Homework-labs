import pymorphy2
import tokenize_uk

morph_analyzer = pymorphy2.MorphAnalyzer(lang='uk')

for i in range(20):
    with open("sampling" + str(i) + ".txt", "r", encoding="utf-8") as file:
        sents = file.readlines()

    pos = {}
    for sentence in sents:
        tokens = tokenize_uk.tokenize_words(sentence)
        for token in tokens:
            if token.isalnum():
                token_pos = morph_analyzer.parse(token)[0].tag.POS
                if token_pos not in pos.keys():
                    pos[token_pos] = 1
                else:
                    pos[token_pos] += 1
    print("Sampling ", i + 1)
    for k, v in pos.items():
        print(k, "-", v)

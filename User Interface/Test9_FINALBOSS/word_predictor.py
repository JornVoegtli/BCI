import re, collections

def words(text): return re.findall('[a-z]+', text.lower()) 

def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model

NWORDS = train(words(file('dep_files/big.txt').read()))
alphabet = 'abcdefghijklmnopqrstuvwxyz'

def edits1(word):
    splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes    = [a + b[1:] for a, b in splits if b]
    transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
    replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
    inserts    = [a + c + b     for a, b in splits for c in alphabet]
    return set(deletes + transposes + replaces + inserts)

def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

def known(words): return set(w for w in words if w in NWORDS)

def correct(word):
    word.lower()
    # #word1 = word + "a"
    # #word2 = word + "e"
    # if(word == ""):
    #     candidate0 = "PT1"
    #     candidate1 = "PT2"
    #     candidate2 = "PT3"
    #     return[candidate0,candidate1,candidate2]
    #else:
    candidate0 = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
        # candidate1 = known([word1]) or known(edits1(word1)) or known_edits2(word1) or [word]
        # candidate2 = known([word2]) or known(edits1(word2)) or known_edits2(word2) or [word]
    return max(candidate0, key=NWORDS.get) 
            # max(candidate2, key=NWORDS.get)]
            # max(candidate1, key=NWORDS.get),
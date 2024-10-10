import pickle

with open("avigad_out.pickle", 'rb') as f:
        avigad_out = pickle.load(f)
with open("out.pickle", 'rb') as f:
        out = pickle.load(f)

with open("avigad_words_dict.pickle", 'rb') as f:
        avigad_words_dict = pickle.load(f)
with open("words_dict.pickle", 'rb') as f:
        words_dict = pickle.load(f)

with open("avigad_ranking_dict.pickle", 'rb') as f:
        avigad_ranking_dict = pickle.load(f)
with open("ranking_dict.pickle", 'rb') as f:
        ranking_dict = pickle.load(f)

with open('avigad_results.txt', 'r') as f:
        avigad_results = f.read()
with open('results.txt', 'r') as f:
        results = f.read()


assert avigad_out == out
assert avigad_words_dict == words_dict
assert avigad_ranking_dict == ranking_dict
assert avigad_results == results

print ('you made it!')
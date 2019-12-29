from sqlitedict import SqliteDict
import pickle
import itertools

t = []
c = 0
with SqliteDict("/../../../../../scratch/manoelribeiro/helpers/authors_dict.sqlite", tablename="authors",
                         flag="r") as mydict:
    
    for _, value in mydict.items():
        if len(value)>1:
            t.append(value)
        if(c%100000) == 0:
            print(c, len(t))
        c += 1

with open("authors_split_new.pickle", "wb") as fp:
    pickle.dump(t, fp, protocol=pickle.HIGHEST_PROTOCOL)

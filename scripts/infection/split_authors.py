from sqlitedict import SqliteDict
import pickle
import itertools

t = []
ct=0
c = 0
mydict = SqliteDict("/../../../../../scratch/manoelribeiro/helpers/authors_dict.sqlite", tablename="authors", flag="r")


for _, value in mydict.items():
    if len(value)>1:
        t.append(value)
        ct+=1
    if(c>=11300000):
        break
    if(c%100000) == 0:
        print(c, ct)
    c += 1

with open("authors_split_new2.pickle", "wb") as fp:
    pickle.dump(t, fp, protocol=pickle.HIGHEST_PROTOCOL)

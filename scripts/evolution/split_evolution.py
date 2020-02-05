from sqlitedict import SqliteDict
import pickle

t10 = []
tall = []
c = 0
c_t10 = 0
c_tall = 0
mydict = SqliteDict("/../../../../../scratch/manoelribeiro/helpers/authors_dict.sqlite", tablename="authors", flag="r")
    
for _, value in mydict.iteritems():
    if(c % 100000) == 0:
        print(f"c = {c}, c_all = {c_tall}, c_t10 = {c_t10}")
    c += 1
    if c >= 11900000:
        break
        
    diff_comm = set()
    for comm in value:
        cat = comm["category"]
        if cat == "Alt-right" or cat == "Alt-lite" or cat == "Intellectual Dark Web":
            diff_comm.add(cat)
        else:
            diff_comm.add("control")
        
    if len(value) < 3 or len(diff_comm)>1: continue
  
    if len(value) >= 10:
        t10.append(value)
        c_t10 += 1
    tall.append(value)
    c_tall += 1
    
with open("authors_10.pickle", "wb") as fp:
    pickle.dump(t10, fp, protocol=pickle.HIGHEST_PROTOCOL)
with open("authors_evolution.pickle", "wb") as fp:
    pickle.dump(tall, fp, protocol=pickle.HIGHEST_PROTOCOL)

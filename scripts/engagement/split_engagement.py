from sqlitedict import SqliteDict
import pickle

tall = []
c = 0
c_tall = 0
mydict = SqliteDict("/../../../../../scratch/manoelribeiro/helpers/authors_dict.sqlite", tablename="authors", flag="r")

for _, value in mydict.iteritems():
    if (c % 100000) == 0:
        print(f"c = {c}, c_all = {c_tall}")
    c += 1
    if c >= 11400000:
        break

    diff_comm = set()
    for comm in value:
        cat = comm["category"]
        if cat == "Alt-right" or cat == "Alt-lite" or cat == "Intellectual Dark Web":
            diff_comm.add(cat)
        else:
            diff_comm.add("control")

    if len(diff_comm) > 1:
        continue

    tall.append(value)
    c_tall += 1

with open("authors_engagement.pickle", "wb") as fp:
    pickle.dump(tall, fp, protocol=pickle.HIGHEST_PROTOCOL)

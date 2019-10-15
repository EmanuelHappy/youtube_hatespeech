from sqlitedict import SqliteDict
from datetime import datetime
import pickle

names_list = ["right-center", "Alt-right", "center", "right", "left", "left-center", "IDW", "Alt-lite"]
for name in names_list:
    community = SqliteDict(f"./../Sqlite/split_texts/{name}.sqlite", tablename="value", flag="r")
    ks = {}
    c = 0
    for key, value in community.items():
        if c % 1000000 == 0:
            print("Iteration number", c)
        c += 1

        ks[key] = datetime.fromtimestamp(value["timestamp"]//1000).year

    with open(f'{name}.pickle', 'wb') as handle:
        pickle.dump(ks, handle, protocol=pickle.HIGHEST_PROTOCOL)
    print("pickle")

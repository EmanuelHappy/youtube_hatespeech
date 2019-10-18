from sqlitedict import SqliteDict
import pickle

source = "./../data/sqlite/community_texts/"
path = "./../data/sentiment/community_id/time/"
names_list = ["right-center", "Alt-right", "center", "right", "left", "left-center", "IDW", "Alt-lite"]
names_list = ["Alt-lite"]


bins_t_s = ["2006-2012", "2013-2015", "2016", "2017", "2018"]

bins_y_s = [
    (1146398400000, 1367323200000),  # Apr 30,06 - Apr 30,13
    (1367323200000, 1462017600000),  # Apr 30,13 - Apr 30,16
    (1462017600000, 1493553600000),  # Apr 30,16 - Apr 30,17
    (1493553600000, 1525089600000),  # Apr 30,17 - Apr 30,18
    (1525089600000, 1556625600000)  # Apr 30,18 - Apr 30,19
]

for name in names_list:
    not_collected = 0
    per_year = [0, 0, 0, 0, 0]
    ks = {}
    c = 0
    community = SqliteDict(f"{source}{name}.sqlite", tablename="value", flag="r")

    for key, value in community.items():
        if c % 1000000 == 0:
            print("Iteration number", c)
        c += 1
        date = value["timestamp"]
        if date < bins_y_s[0][1]:
            per_year[0] += 1
            ks[key] = bins_t_s[0]
        elif date < bins_y_s[1][1]:
            per_year[1] += 1
            ks[key] = bins_t_s[1]
        elif date < bins_y_s[2][1]:
            per_year[2] += 1
            ks[key] = bins_t_s[2]
        elif date < bins_y_s[3][1]:
            per_year[3] += 1
            ks[key] = bins_t_s[3]
        elif date < bins_y_s[4][1]:
            per_year[4] += 1
            ks[key] = bins_t_s[4]
        else:
            not_collected += 1
            
        if(c==18000000):
                print(f"{not_collected} ids not collected")
                print(f"The number of files are organized in that way:\n {bins_t_s}\n {per_year}")
                with open(f'{path}{name}.pickle', 'wb') as handle:
                    pickle.dump(ks, handle, protocol=pickle.HIGHEST_PROTOCOL)

    print(f"{not_collected} ids not collected")
    print(f"The number of files are organized in that way:\n {bins_t_s}\n {per_year}")
    with open(f'{path}{name}.pickle', 'wb') as handle:
        pickle.dump(ks, handle, protocol=pickle.HIGHEST_PROTOCOL)

    print(f"pickle {name}")

import pickle

bins_t_s = ["2016", "2017", "2018"]
bins_y_s = [
    (1462017600000, 1493553600000),  # Apr 30,16 - Apr 30,17
    (1493553600000, 1525089600000),  # Apr 30,17 - Apr 30,18
    (1525089600000, 1556625600000)  # Apr 30,18 - Apr 30,19
]
t0 = t1 = t2 = t3 = 0
bins_eng_y = [(1, 1), (2, 3), (4, 9), (10, float('inf'))]
bins_eng_t = ["1", "2_3", "4_9", "10"]
communities = ["Alt-right", "IDW", "Alt-lite", "control"]
communities_real = ["Alt-right", "Intellectual Dark Web", "Alt-lite", "control"]
comm_transl = dict(zip(communities_real, communities))
comment = {}
for cat in communities:
    comment[cat] = {}
    for year in bins_t_s:
        comment[cat][year] = {}
        for eng in bins_eng_t:
            comment[cat][year][eng] = []
c = 0
not_comm = 0
with open("authors_engagement.pickle", "rb") as fp:
    authors = pickle.load(fp)

for value in authors:
    if c % 100000 == 0:
        print(f"it\t{bins_eng_t[0]}\t{bins_eng_t[1]}\t{bins_eng_t[2]}\t{bins_eng_t[3]}\tnot commented")
        print(f"{c}\t{t0}\t{t1}\t{t2}\t{t3}\t{not_comm}")
    c += 1

    current_year = value[0]["timestamp"]  # verify year
    year_at = None
    if current_year < bins_y_s[0][0] or current_year > bins_y_s[2][1]:
        continue
    elif current_year <= bins_y_s[0][1]:
        current_year = bins_y_s[0][1]
        year_at = 0
    elif current_year <= bins_y_s[1][1]:
        current_year = bins_y_s[1][1]
        year_at = 1
    elif current_year <= bins_y_s[2][1]:
        current_year = bins_y_s[2][1]
        year_at = 2

    cat = value[0]["category"]  # verify community
    if cat == "Alt-right" or cat == "Alt-lite" or cat == "Intellectual Dark Web":
        cat = comm_transl[cat]
    else:
        cat = "control"

    t = []  # add ids
    for comm in value:
        if comm["timestamp"] < current_year:
            t.append(comm["id"])
        else:
            not_comm += 1

    engagement = len(t)  # verify engagement
    if engagement <= bins_eng_y[0][1]:
        comment[cat][bins_t_s[year_at]][bins_eng_t[0]].extend(t)
        t0 += 1
    elif engagement <= bins_eng_y[1][1]:
        comment[cat][bins_t_s[year_at]][bins_eng_t[1]].extend(t)
        t1 += 1
    elif engagement <= bins_eng_y[2][1]:
        comment[cat][bins_t_s[year_at]][bins_eng_t[2]].extend(t)
        t2 += 1
    elif engagement <= bins_eng_y[3][1]:
        comment[cat][bins_t_s[year_at]][bins_eng_t[3]].extend(t)
        t3 += 1

# Saves each community at each comment
for cat in communities:
    for year in bins_t_s:
        for eng in bins_eng_t:
            to_save = tuple(comment[cat][year][eng])
            with open(f"./data/engagement_{cat}_{year}_{eng}.pickle", "wb") as fp:
                pickle.dump(to_save, fp, protocol=4)

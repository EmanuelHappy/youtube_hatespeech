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

    cat = value[0]["category"]  # verify community
    if cat == "Alt-right" or cat == "Alt-lite" or cat == "Intellectual Dark Web":
        cat = comm_transl[cat]
    else:
        cat = "control"

    t16 = []
    t17 = []
    t18 = []
    for comm in value:  # add values by year
        current_year = comm["timestamp"]
        if current_year < bins_y_s[0][0] or current_year > bins_y_s[2][1]:
            not_comm += 1
            continue
        elif current_year < bins_y_s[0][1]:
            t16.append(comm['id'])
        elif current_year < bins_y_s[1][1]:
            t17.append(comm['id'])
        elif current_year < bins_y_s[2][1]:
            t18.append(comm['id'])

    all_t = [t16, t17, t18]  # for all years
    for year_at, t in zip(bins_t_s, all_t):
        engagement = len(t)  # verify engagement
        if engagement == 0:
            continue
        elif engagement <= bins_eng_y[0][1]:
            comment[cat][year_at][bins_eng_t[0]].extend(t)
            t0 += 1
        elif engagement <= bins_eng_y[1][1]:
            comment[cat][year_at][bins_eng_t[1]].extend(t)
            t1 += 1
        elif engagement <= bins_eng_y[2][1]:
            comment[cat][year_at][bins_eng_t[2]].extend(t)
            t2 += 1
        elif engagement <= bins_eng_y[3][1]:
            comment[cat][year_at][bins_eng_t[3]].extend(t)
            t3 += 1

# Saves each community at each comment
for cat in communities:
    for year in bins_t_s:
        for eng in bins_eng_t:
            to_save = tuple(comment[cat][year][eng])
            with open(f"./data/engagement_{cat}_{year}_{eng}_all.pickle", "wb") as fp:
                pickle.dump(to_save, fp, protocol=4)

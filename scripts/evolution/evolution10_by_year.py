import pickle

bins_t_s = ["2016", "2017", "2018"]
bins_y_s = [
    (1462017600000, 1493553600000),  # Apr 30,16 - Apr 30,17
    (1493553600000, 1525089600000),  # Apr 30,17 - Apr 30,18
    (1525089600000, 1556625600000)  # Apr 30,18 - Apr 30,19
]
communities = ["Alt-right", "IDW", "Alt-lite", "control"]
communities_real = ["Alt-right", "Intellectual Dark Web", "Alt-lite", "control"]
comm_transl = dict(zip(communities_real, communities))
comment = {}
for cat in communities:
    comment[cat] = {}
    for year in bins_t_s:
        comment[cat][year] = {}
        for i in range(2, 11, 2):
            comment[cat][year][i] = []
c = 0
with open("authors_10.pickle", "rb") as fp:
    authors = pickle.load(fp)

for value in authors:
    if c % 100000 == 0:
        print("it = ", c)
    d = {"Alt-right": [], "Alt-lite": [], "IDW": [], "control": []}
    diff_comm = set()
    c += 1

    for comm in value:
        cat = comm["category"]
        if cat == "Alt-right" or cat == "Alt-lite" or cat == "Intellectual Dark Web":
            d[comm_transl[cat]].append((comm["timestamp"], comm["id"]))
            diff_comm.add(comm_transl[cat])
        else:
            d["control"].append((comm["timestamp"], comm["id"]))
            diff_comm.add("control")

    for cat in diff_comm:
        year = "year"
        if d[cat][0][0] < bins_y_s[0][0]:
            break
        elif d[cat][0][0] < bins_y_s[0][1]:
            year = bins_t_s[0]
        elif d[cat][0][0] < bins_y_s[1][1]:
            year = bins_t_s[1]
        elif d[cat][0][0] < bins_y_s[2][1]:
            year = bins_t_s[2]
        if year != "year":
            for i in range(2, 11, 2):
                comment[cat][year][i].append(d[cat][i-2][1])
                comment[cat][year][i].append(d[cat][i-1][1])

# Saves each community at each comment
for cat in communities:
    for year in bins_t_s:
        for i in range(2, 11, 2):
            to_save = tuple(comment[cat][year][i])
            with open(f"./data/evolution10_{cat}_{year}_{i}.pickle", "wb") as fp:
                pickle.dump(to_save, fp, protocol=4)

import pickle

t0 = t1 = t2 = t3 = 0
bins_y_s = [(1, 1), (2, 3), (4, 9), (10, float('inf'))]
bins_t_s = ["1", "2_3", "4_9", "10"]
communities = ["Alt-right", "IDW", "Alt-lite", "control"]
communities_real = ["Alt-right", "Intellectual Dark Web", "Alt-lite", "control"]
comm_transl = dict(zip(communities_real, communities))
comment = {}
for cat in communities:
    comment[cat] = {}
    for eng in bins_t_s:
        comment[cat][eng] = []
c = 0
with open("authors_engagement.pickle", "rb") as fp:
    authors = pickle.load(fp)

for value in authors:
    if c % 100000 == 0:
        print(f"it\t{bins_t_s[0]}\t{bins_t_s[1]}\t{bins_t_s[2]}\t{bins_t_s[3]}")
        print(f"{c}\t{t0}\t{t1}\t{t2}\t{t3}")
    t = []
    cat = None
    diff_comm = set()
    c += 1

    for comm in value:
        cat = comm["category"]
        if cat == "Alt-right" or cat == "Alt-lite" or cat == "Intellectual Dark Web":
            t.append(comm["id"])
            cat = comm_transl[cat]
        else:
            t.append(comm["id"])
            cat = "control"

    if len(t) <= bins_y_s[0][1]:
        comment[cat][bins_t_s[0]].extend(t)
        t0 += 1
    elif len(t) <= bins_y_s[1][1]:
        comment[cat][bins_t_s[1]].extend(t)
        t1 += 1
    elif len(t) <= bins_y_s[2][1]:
        comment[cat][bins_t_s[2]].extend(t)
        t2 += 1
    elif len(t) <= bins_y_s[3][1]:
        comment[cat][bins_t_s[3]].extend(t)
        t3 += 1

# Saves each community at each comment
for cat in communities:
    for eng in bins_t_s:
        to_save = tuple(comment[cat][eng])
        with open(f"./data/engagement_{cat}_{eng}.pickle", "wb") as fp:
            pickle.dump(to_save, fp, protocol=4)

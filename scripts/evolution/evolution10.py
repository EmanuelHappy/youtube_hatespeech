import pickle

communities = ["Alt-right", "IDW", "Alt-lite", "control"]
communities_real = ["Alt-right", "Intellectual Dark Web", "Alt-lite", "control"]
comm_transl = dict(zip(communities_real, communities))
comment = {}
for cat in communities:
    comment[cat] = {}
    for i in range(1, 11):
        comment[cat][i] = []
c = 0
not_comm = 0
with open("authors_10.pickle", "rb") as fp:
    authors = pickle.load(fp)

for value in authors:
    if c % 100000 == 0:
        print("it = ", c, "not = ", not_comm)
    d = {"Alt-right": [], "Alt-lite": [], "IDW": [], "control": []}
    diff_comm = set()
    c += 1

    for comm in value:
        cat = comm["category"]
        if cat == "Alt-right" or cat == "Alt-lite" or cat == "Intellectual Dark Web":
            d[comm_transl[cat]].append(comm["id"])
            diff_comm.add(comm_transl[cat])
        else:
            d["control"].append(comm["id"])
            diff_comm.add("control")

    if len(diff_comm) > 1:  # just authors that comment in a single community
        not_comm += 1
        continue

    for cat in diff_comm:
        for i in range(1, 11):
            comment[cat][i].append(d[cat][i-1])

# Saves each community at each comment
for cat in communities:
    for i in range(1, 11):
        to_save = tuple(comment[cat][i])
        with open(f"./data/evolution10_{cat}_{i}.pickle", "wb") as fp:
            pickle.dump(to_save, fp, protocol=4)

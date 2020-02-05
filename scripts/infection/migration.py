import pickle

bins_t_s = ["2016", "2017", "2018"]

bins_y_s = [
    (1462017600000, 1493553600000),  # Apr 30,16 - Apr 30,17
    (1493553600000, 1525089600000),  # Apr 30,17 - Apr 30,18
    (1525089600000, 1556625600000)  # Apr 30,18 - Apr 30,19
]

communities = ["Alt-lite_IDW", "Alt-lite", "IDW", "control"]

light = {}
mild = {}
severe = {}
for community in communities:
    light[community] = {}
    mild[community] = {}
    severe[community] = {}
    for y in bins_t_s:
        light[community][y] = []
        mild[community][y] = []
        severe[community][y] = []


def add_year(year):
    values = []
    for v in d.values():
        values.extend(v)

    if len(d["Alt-right"]) <= 2:  # light
        if len(d["Alt-lite"]) > 0 and len(d["Intellectual Dark Web"]) > 0 and len(d["control"]) > 0:
            return
        elif len(d["Alt-lite"]) > 0 and len(d["Intellectual Dark Web"]) > 0:
            light["Alt-lite_IDW"][year].extend(values)
        elif len(d["Alt-lite"]) > 0:
            light["Alt-lite"][year].extend(values)
        elif len(d["Intellectual Dark Web"]) > 0:
            light["IDW"][year].extend(values)
        elif len(d["control"]) > 0:
            light["control"][year].extend(values)

    elif len(d["Alt-right"]) <= 5:  # mild
        if len(d["Alt-lite"]) > 0 and len(d["Intellectual Dark Web"]) > 0 and len(d["control"]) > 0:
            return
        elif len(d["Alt-lite"]) > 0 and len(d["Intellectual Dark Web"]) > 0:
            mild["Alt-lite_IDW"][year].extend(values)
        elif len(d["Alt-lite"]) > 0:
            mild["Alt-lite"][year].extend(values)
        elif len(d["Intellectual Dark Web"]) > 0:
            mild["IDW"][year].extend(values)
        elif len(d["control"]) > 0:
            mild["control"][year].extend(values)

    else:  # severe
        if len(d["Alt-lite"]) > 0 and len(d["Intellectual Dark Web"]) > 0 and len(d["control"]) > 0:
            return
        elif len(d["Alt-lite"]) > 0 and len(d["Intellectual Dark Web"]) > 0:
            severe["Alt-lite_IDW"][year].extend(values)
        elif len(d["Alt-lite"]) > 0:
            severe["Alt-lite"][year].extend(values)
        elif len(d["Intellectual Dark Web"]) > 0:
            severe["IDW"][year].extend(values)
        elif len(d["control"]) > 0:
            severe["control"][year].extend(values)


c = 0
not_comm = 0
with open("authors_split_new2.pickle", "rb") as fp:
    authors = pickle.load(fp)

for value in authors:
    d = {"Alt-right": [], "Alt-lite": [], "Intellectual Dark Web": [], "control": []}
    s_not = s_16 = s_17 = s_18 = False

    for comm in value:
        if comm['timestamp'] < bins_y_s[0][0]:
            continue
        cat = comm["category"]

        if cat == "Alt-right" or cat == "Alt-lite" or cat == "Intellectual Dark Web":
            d[cat].append((comm["timestamp"], comm["id"]))
        else:
            d["control"].append((comm["timestamp"], comm["id"]))

    if len(d["Alt-right"]) == 0:
        not_comm += 1
        continue
    else:
        for t in d["Alt-right"]:
            if t[0] < bins_y_s[0][0]:
                s_not = True
                break
            elif t[0] <= bins_y_s[0][1]:
                s_16 = True
            elif t[0] <= bins_y_s[1][1]:
                s_17 = True
            else:
                s_18 = True

        if s_not:
            continue
        if s_16:
            add_year("2016")
        elif s_17:
            add_year("2017")
        else:
            add_year("2018")

    if c == 0:
        print(d)
    if c % 100000 == 0:
        print("loop", c, len(light[community][y]), len(mild[community][y]), len(severe[community][y]))
    c += 1

print("Not commented in Alt-right = ", not_comm)
print("Saving")

for community in communities:
    for y in bins_t_s:
        print(community, y, len(light[community][y]), len(mild[community][y]), len(severe[community][y]))
        light_item = list(light[community][y])
        mild_item = list(mild[community][y])
        severe_item = list(severe[community][y])
        with open(f"light_{community}_{y}.pickle", "wb") as f1:
            pickle.dump(light_item, f1, protocol=4)
        with open(f"mild_{community}_{y}.pickle", "wb") as f2:
            pickle.dump(mild_item, f2, protocol=4)
        with open(f"severe_{community}_{y}.pickle", "wb") as f3:
            pickle.dump(severe_item, f3, protocol=4)


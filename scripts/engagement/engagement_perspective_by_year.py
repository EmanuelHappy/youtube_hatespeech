import pickle
import numpy as np
import pandas as pd


def bootstrap(data, n=1000, func=np.mean):
    simulations = list()
    sample_size = len(data)
    for _ in range(n):
        itersample = np.random.choice(data, size=sample_size, replace=True)
        simulations.append(func(itersample))
    simulations.sort()

    def ci(p):
        u_pval = (1+p)/2.
        l_pval = (1-u_pval)
        l_indx = int(np.floor(n*l_pval))
        u_indx = int(np.floor(n*u_pval))
        return simulations[l_indx], simulations[u_indx]
    return ci


names_control = ["right-center", "center", "left", "left-center", "right"]
filenames = ["0_5000000", "0_10000000", "0_15000000", "0_20000001", "2_2390000", "2.1_640000", "2.2_285042",
             "2.3_887730", "2.4_6000000", "3_7900000", "3.1_2180000", "4.1_4581097", "4.2_320000", "4.3_1050000",
             "4_2200000", "5.1_2300000", "5.2_6139999", "6.1_2858690", "6.2_6109999", "7.1_3859623"]
names = ["Alt-right", "IDW", "Alt-lite", "control"]
bins_t_s = ["2016", "2017", "2018"]
bins_eng_s = ["1", "2_3", "4_9", "10"]
attributes = ['TOXICITY', 'SEVERE_TOXICITY', 'IDENTITY_ATTACK']
dst_path = "./../../data/sentiment/dataframes/perspective_df/engagement/"
middle_path = "./../../data/sentiment/"

# Values to change
with open("./../../data/sentiment/ids/removed_ids/change_ids.pickle", "rb") as fp:
    changed = pickle.load(fp)
print("changed")
with open("./../../data/sentiment/ids/removed_ids/remove_ids.pickle", "rb") as fp:
    removed = pickle.load(fp)
print("removed")
to_change = dict()
for eng in bins_eng_s:
    to_change[eng] = []
t_remove = 0

ks = {}
for file in filenames:
    print(file)
    with open(f"{middle_path}values/perspective_val/perspective_{file}_val", "rb") as fp:
        perspective = pickle.load(fp)
    with open(f"{middle_path}ids/perspective_id/perspective_{file}_id", "rb") as fp:
        ide = pickle.load(fp)

    print(len(ide), len(perspective))
    for i in range(len(perspective)):
        ks[ide[i]] = perspective[i]

for year in bins_t_s:
    for name in names:
        x = []
        y = []
        dyd = []
        dyu = []
        for eng in bins_eng_s:
            x.append(eng)
            values = []

            with open(f"./data/engagement_{name}_{year}_{eng}_all.pickle", "rb") as fp:
                engagement_id = pickle.load(fp)

            print(name, year, "eng:", eng, "number of comments:", len(engagement_id))
            if name == "Alt-lite":
                engagement_id = list(engagement_id)
                engagement_id.extend(to_change[eng])
                print("new number =", len(engagement_id))

            for ide in engagement_id:
                if ide in ks and len(ks[ide]) > 0:
                    if name != "Alt-lite" and ide in changed:
                        to_change[eng].append(ide)
                    elif ide not in removed:
                        values.append(ks[ide][1])
                    else:
                        t_remove += 1

            values = np.array(values)
            print(f"Shape of values = {values.shape}, Changed = {len(to_change[eng])}, Removed = {t_remove}")
            t_remove = 0

            y.append(np.mean(values, axis=0))
            boot = bootstrap(values)
            c = boot(.95)
            dyd.append(c[0])
            dyu.append(c[1])

        y = np.array(y)
        print("Y shape =", y.shape)

        d = dict()
        d[attributes[1]] = y
        d[f"{attributes[1]}_dyu"] = dyu
        d[f"{attributes[1]}_dyd"] = dyd
        d["engage"] = x

        df = pd.DataFrame(d)
        df.to_csv(f"{dst_path}{name}_{year}_perspective_engagement_all.csv")

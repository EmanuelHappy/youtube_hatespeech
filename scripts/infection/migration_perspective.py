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
        u_pval = (1 + p) / 2.
        l_pval = (1 - u_pval)
        l_indx = int(np.floor(n * l_pval))
        u_indx = int(np.floor(n * u_pval))
        return simulations[l_indx], simulations[u_indx]

    return ci


names_control = ["right-center", "center", "left", "left-center", "right"]
filenames = ["0_5000000", "0_10000000", "0_15000000", "0_20000001", "2_2390000", "2.1_640000", "2.2_285042",
             "2.3_887730", "2.4_6000000", "3_7900000", "3.1_2180000", "4.1_4581097", "4.2_320000", "4.3_1050000",
             "4_2200000", "5.1_2300000", "5.2_6139999", "6.1_2858690", "6.2_6109999", "7.1_3859623"]
names = ["Alt-lite_IDW", "IDW", "Alt-lite", "control"]
bins_t_s = ["2017", "2018"]
attributes = ['SEVERE_TOXICITY']
dst_path = "./../../data/sentiment/dataframes/perspective_df/migration/"
middle_path = "./../../data/sentiment/"

# Values to change
with open("./../../data/sentiment/ids/removed_ids/change_ids.pickle", "rb") as fp:
    changed = pickle.load(fp)
print("changed")
with open("./../../data/sentiment/ids/removed_ids/remove_ids.pickle", "rb") as fp:
    removed = pickle.load(fp)
print("removed")
to_change = dict()
for start in bins_t_s:
    to_change[start] = {}
    for cat in ["light", "mild", "severe"]:
        to_change[start][cat] = {}
        for year in range(int(start) - 1, int(start) + 1):
            to_change[start][cat][year] = []
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

for name in names:
    for start in bins_t_s:
        for cat in ["light", "mild", "severe"]:
            x = []
            y = []
            dyd = []
            dyu = []

            for year in range(int(start) - 1, int(start) + 1):
                end = str(year)
                x.append(end)

                values = []
                with open(f"./values_per_year/{cat}_{name}_{start}_{end}.pickle", "rb") as fp:
                    migration_id = pickle.load(fp)
                print(name, start, end, cat, len(migration_id))

                if name == "Alt-lite":
                    migration_id = list(migration_id)
                    migration_id.extend(to_change[start][cat][year])
                    print("new number =", len(migration_id))

                for ide in migration_id:
                    if ide in ks and len(ks[ide]) > 0:
                        if name == "IDW" and ide in changed:
                            to_change[start][cat][year].append(ide)
                        elif ide not in removed:
                            values.append(ks[ide][1])
                        else:
                            t_remove += 1

                values = np.array(values)
                print(f"Shape = {values.shape}, Changed = {len(to_change[start][cat][year])}, Removed = {t_remove}")
                t_remove = 0
                y.append(np.mean(values))

                dyd_year = []
                dyu_year = []

                boot = bootstrap(values)
                c = boot(.95)
                dyd_year.append(c[0])
                dyu_year.append(c[1])

                dyu.append(dyu_year)
                dyd.append(dyd_year)

            y = np.array(y)
            print(y.shape)

            d = dict()
            for i in range(len(attributes)):
                d[attributes[i]] = []
                d[f"{attributes[i]}_dyu"] = []
                d[f"{attributes[i]}_dyd"] = []
            d["year"] = x

            print("saving")
            for i in range(len(y)):
                for j in range(len(attributes)):
                    d[attributes[j]].append(y[i])
                    d[f"{attributes[j]}_dyu"].append(dyu[i][j])
                    d[f"{attributes[j]}_dyd"].append(dyd[i][j])

            df = pd.DataFrame(d)
            df.to_csv(f"{dst_path}{name}{start}{cat}_perspective_migration_new.csv")

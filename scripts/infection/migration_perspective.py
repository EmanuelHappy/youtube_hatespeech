import pickle
import numpy as np
import pandas as pd

def bootstrap(data, n=1000, func=np.mean):
    """
    Generate `n` bootstrap samples, evaluating `func`
    at each resampling. `bootstrap` returns a function,
    which can be called to obtain confidence intervals
    of interest.
    """
    simulations = list()
    sample_size = len(data)
    xbar_init = np.mean(data)
    for c in range(n):
        itersample = np.random.choice(data, size=sample_size, replace=True)
        simulations.append(func(itersample))
    simulations.sort()

    def ci(p):
        """
        Return 2-sided symmetric confidence interval specified
        by p.
        """
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
names = ["Alt-lite_IDW", "IDW", "Alt-lite", "control"]
bins_t_s = ["2016", "2017", "2018"]
attributes = ['TOXICITY', 'SEVERE_TOXICITY', 'IDENTITY_ATTACK']
dst_path = "./../../data/sentiment/dataframes/perspective_df/migration/"
middle_path = "./../../data/sentiment/"

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

            for year in range(int(start)-1, 2019):
                end = str(year)
                x.append(end)

                values = []
                with open(f"./values_per_year/{cat}_{name}_{start}_{end}.pickle", "rb") as fp:
                    migration_id = pickle.load(fp)
                print(name, start, end, cat, len(migration_id))

                for ide in migration_id:
                    if ide in ks and len(ks[ide]) > 0:
                        values.append([ks[ide][0], ks[ide][1], ks[ide][2]])

                values = np.array(values)
                print(values.shape)
                y.append(np.mean(values, axis=0))
                
                dyd_year = []
                dyu_year = []
                c = 0
                for j in range(3):
                    boot = bootstrap(values[:, j])
                    c = boot(.95)
                    dyd_year.append(c[0])
                    dyu_year.append(c[1])

                dyu.append(dyu_year)
                dyd.append(dyd_year)
            
            y = np.array(y)
            print(y.shape)
            
            d = {}
            for i in range(len(attributes)):
                d[attributes[i]] = []
                d[f"{attributes[i]}_dyu"] = []
                d[f"{attributes[i]}_dyd"] = []
            d["year"] = x

            print("saving")
            for i in range(len(y)):
                for j in range(len(attributes)):
                    d[attributes[j]].append(y[i, j])
                    d[f"{attributes[j]}_dyu"].append(dyu[i][j])
                    d[f"{attributes[j]}_dyd"].append(dyd[i][j])

            df = pd.DataFrame(d)
            df.to_csv(f"{dst_path}{name}{start}{cat}_perspective_migration.csv")

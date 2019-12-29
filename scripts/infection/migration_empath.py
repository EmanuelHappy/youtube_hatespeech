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
        u_pval = (1 + p) / 2.
        l_pval = (1 - u_pval)
        l_indx = int(np.floor(n * l_pval))
        u_indx = int(np.floor(n * u_pval))
        return simulations[l_indx], simulations[u_indx]

    return ci


names_control = ["right-center", "center", "left", "left-center", "right"]
filenames = ["1_4600000", "2_4600000", "3_2400002", "4_3000002", "5_1000001", "6_10000000", "6_20000000",
                 "6_30000000", "6_40000000", "6_50000000", "6_53900001"]
names = ["Alt-lite_IDW", "IDW", "Alt-lite", "control"]
bins_t_s = ["2016", "2017", "2018"]
attributes = ['size', 'sadness', 'independence', 'positive_emotion', 'family', 'negative_emotion', 'government',
                'love', 'ridicule', 'masculine', 'feminine', 'violence', 'suffering', 'dispute', 'anger', 'envy',
                'work', 'politics', 'terrorism', 'shame', 'confusion', 'hate']
dst_path = "./../../data/sentiment/dataframes/empath_df/migration/"
middle_path = "./../../data/sentiment/"

ks = {}
for file in filenames:
    print(file)
    with open(f"{middle_path}values/empath_val/empath_{file}_val", "rb") as fp:
        perspective = pickle.load(fp)
    with open(f"{middle_path}ids/empath_id/empath_{file}_id", "rb") as fp:
        ide = pickle.load(fp)

    for i in range(len(perspective)):
        ks[ide[i]] = perspective[i]

for name in names:
    for start in bins_t_s:
        for cat in ["light", "mild", "severe"]:
            x = []
            y = []
            dyd = []
            dyu = []

            for year in range(int(start) - 1, 2019):
                end = str(year)
                x.append(end)

                values = []
                with open(f"./values_per_year/{cat}_{name}_{start}_{end}.pickle", "rb") as fp:
                    migration_id = pickle.load(fp)
                print(name, start, end, cat, len(migration_id))


                for ide in migration_id:
                    if ide in ks:
                        values.append(ks[ide])

                values = np.array(values)
                y.append(np.mean(values, axis=0))

                dyd_year = []
                dyu_year = []
                c = 0
                for j in range(len(attributes)):
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
            df.to_csv(f"{dst_path}{name}{start}{cat}_empath_migration.csv")

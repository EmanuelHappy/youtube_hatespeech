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


names = ["Alt-lite_IDW", "IDW", "Alt-lite", "control"]
bins_t_s = ["2016", "2017", "2018"]
attributes = ['TOXICITY', 'IDENTITY_ATTACK', 'THREAT']
dst_path = "./../../data/sentiment/dataframes/text_blob_df/migration/"
middle_path = "./../../data/sentiment/"

with open(f"{middle_path}values/textblob_pol_val/all_polarity.pickle", "rb") as fp:
    polarity = pickle.load(fp)
print("polarity", len(polarity))
with open(f"{middle_path}ids/textblob_id/all_keys.pickle", "rb") as fp:
    ide = pickle.load(fp)
print("ide", len(ide))
ks = dict(zip(ide, polarity))

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
                print(name, start, end, cat)

                values = []
                with open(f"./values_per_year/{cat}_{name}_{start}_{end}.pickle", "rb") as fp:
                    migration_id = pickle.load(fp)

                for ide in migration_id:
                    if ide in ks:
                        values.append(ks[ide])

                values = np.array(values)
                y.append(np.mean(values))

                boot = bootstrap(values)
                c = boot(.95)
                dyd.append(c[0])
                dyu.append(c[1])

            d = {"polarity": y, "polarity_dyu": dyu, "polarity_dyd": dyd, "year": x}

            print("saving", y, dyu, dyd, x)

            df = pd.DataFrame(d)
            df.to_csv(f"{dst_path}{name}{start}{cat}_perspective_migration.csv")

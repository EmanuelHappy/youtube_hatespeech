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
filenames = ["1_4600000", "2_4600000", "3_2400002", "4_3000002", "5_1000001", "6_10000000", "6_20000000",
                 "6_30000000", "6_40000000", "6_50000000", "6_53900001"]
emotion_list = ['size', 'sadness', 'independence', 'positive_emotion', 'family',
                'negative_emotion', 'government', 'love', 'ridicule',
                'masculine', 'feminine', 'violence', 'suffering',
                'dispute', 'anger', 'envy', 'work', 'politics',
                'terrorism', 'shame', 'confusion', 'hate']
dst_path = "./../../data/sentiment/dataframes/empath_blob_df/migration/"
middle_path = "./../../data/sentiment/"


with open(f"{middle_path}values/textblob_pol_val/all_polarity.pickle", "rb") as fp:
    polarity = pickle.load(fp)
print("polarity", len(polarity))
with open(f"{middle_path}ids/textblob_id/all_keys.pickle", "rb") as fp:
    ide = pickle.load(fp)
print("ide", len(ide))
ks_pol = dict(zip(ide, polarity))


ks_emp = {}
for file in filenames:
    print(file)
    with open(f"{middle_path}values/empath_val/empath_{file}_val", "rb") as fp:
        perspective = pickle.load(fp)
    with open(f"{middle_path}ids/empath_id/empath_{file}_id", "rb") as fp:
        ide = pickle.load(fp)

    for i in range(len(perspective)):
        ks_emp[ide[i]] = perspective[i]


for name in names:
    for start in bins_t_s:
        for cat in ["light", "mild", "severe"]:
            d = {}
            x = []

            for emotion in emotion_list:
                d[emotion] = []
                d[f"{emotion}_dyu"] = []
                d[f"{emotion}_dyd"] = []

            for year in range(int(start) - 1, 2019):
                end = str(year)
                x.append(end)

                values = {}
                for emotion in emotion_list:
                    values[emotion] = []

                with open(f"./values_per_year/{cat}_{name}_{start}_{end}.pickle", "rb") as fp:
                    migration_id = pickle.load(fp)

                print(name, start, end, cat, len(migration_id))

                for ide in migration_id:
                    if ide in ks_emp and ide in ks_pol:
                        for emotion in emotion_list:
                            if ks_emp[ide][emotion_list.index(emotion)] > 0:
                                values[emotion].append(ks_pol[ide])

                for emotion in emotion_list:
                    d[emotion].append(np.mean(np.array(values[emotion])))
                    boot = bootstrap(values[emotion])
                    c = boot(.95)
                    d[f"{emotion}_dyd"].append(c[0])
                    d[f"{emotion}_dyu"].append(c[1])

            d["year"] = x
            print("saving", d["sadness"], d["sadness_dyd"], d["sadness_dyu"], x)

            df = pd.DataFrame(d)
            df.to_csv(f"{dst_path}{name}{start}{cat}_empath_blob_migration.csv")

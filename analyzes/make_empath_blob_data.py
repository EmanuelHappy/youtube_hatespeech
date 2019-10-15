import pandas as pd
import pickle
import numpy as np
from .bootstrap import bootstrap

names_control = ["right-center", "center", "left", "left-center", "right1", "right2"]
names = ["Alt-right", "IDW", "Alt-lite", "control"]
names_list_list = [["Alt-right"], ["IDW"], ["Alt-lite"], names_control]
emotion_list = ['size', 'sadness', 'independence', 'positive_emotion', 'family',
                'negative_emotion', 'government', 'love', 'ridicule',
                'masculine', 'feminine', 'violence', 'suffering',
                'dispute', 'anger', 'envy', 'work', 'politics',
                'terrorism', 'shame', 'confusion', 'hate']


def get_ids():
    for names_list in names_list_list:
        d_empath = {}
        for emotion in emotion_list:
            d_empath[emotion] = {}
            for year in range(2006, 2020):
                d_empath[emotion][year] = []

        for name in names_list:
            with open(f"{name}.pickle", "rb") as fp:
                ks = pickle.load(fp)

            filenames = ["1_4600000", "2_4600000", "3_2400002", "4_3000002", "5_1000001", "6_10000000", "6_20000000",
                         "6_30000000", "6_40000000", "6_50000000", "6_53900001"]
            for fname in filenames:
                with open(f"empath_{fname}_val", "rb") as fp:
                    empath = pickle.load(fp)
                print("perspective")
                with open(f"empath_{fname}_id", "rb") as fp:
                    ide = pickle.load(fp)
                print("id")

                for i in range(len(empath)):
                    if i % 1000000 == 0:
                        print(i)
                    key = ide[i]
                    if key in ks:
                        for j in range(1, len(emotion_list)):
                            if empath[i][j] > 0:
                                d_empath[emotion_list[j]][ks[key]].append(key)

                print(fname, "sadness", len(d_empath["sadness"][2018]))
                print(fname, "positive", len(d_empath["positive_emotion"][2018]))

        for emotion in emotion_list:
            for year in range(2007, 2020):
                with open(f"./empath/{names[names_list_list.index(names_list)]}_empath_{emotion}_{year}", "wb") as fp:
                    pickle.dump(d_empath[emotion][year], fp, protocol=4)


def make_df():
    ide = []
    pol = []

    filenames = ["0", "1_10000000", "2_10000000", "3_10000000", "4_10000000", "5_10000000", "6_10000000", "7_4989623"]

    for fname in filenames:

        with open(f"blob_{fname}_pol", "rb") as fp:
            pol1 = pickle.load(fp)
        print("pol")
        with open(f"blob_{fname}_id", "rb") as fp:
            ide1 = pickle.load(fp)

        ide.extend(ide1)
        pol.extend(pol1)
        print(len(pol), len(ide))

    d_pol = dict(zip(ide, pol))
    print("d_pol", len(d_pol))

    for name in names:
        print(name)
        d = {}
        for emotion in emotion_list[1:]:
            d[emotion] = []
            d[f"{emotion}_dyu"] = []
            d[f"{emotion}_dyd"] = []
            d[f"{emotion}_std"] = []
            print(emotion)
            y = []

            for i in range(2007, 2020):
                y1 = []
                with open(f"./empath_blob/{name}_empath_{emotion}_{i}", "rb") as f:
                    keys = pickle.load(f)
                for key in keys:
                    if key in d_pol:
                        y1.append(d_pol[key])
                y.append(np.array(y1))

            print(len(y), y[0])
            y_mean = []
            y_std = []
            dyu = []
            dyd = []

            for i in y:
                y_mean.append(np.mean(i))
                y_std.append(np.std(i))
                boot = bootstrap(i)
                c = boot(.95)
                print(c)
                dyd.append(c[0])
                dyu.append(c[1])

            d[emotion] = y_mean
            d[f"{emotion}_dyu"] = dyu
            d[f"{emotion}_dyd"] = dyd
            d[f"{emotion}_std"] = y_std

        d["year"] = [i for i in range(2007, 2020)]

        df = pd.DataFrame(d)
        df.to_csv(f"./empath_blob/{name}_pol_empath_prop_boots.csv")


if __name__ == "__main__":
    get_ids()
    make_df()

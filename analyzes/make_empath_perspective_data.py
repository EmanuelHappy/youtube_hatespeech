import pandas as pd
import pickle
import numpy as np
from analyzes.utilities.bootstrap import bootstrap

names_control = ["right-center", "center", "left", "left-center", "right1", "right2"]
names_list = ["control"]
emotion_list = ['size', 'sadness', 'independence', 'positive_emotion', 'family',
                'negative_emotion', 'government', 'love', 'ridicule',
                'masculine', 'feminine', 'violence', 'suffering',
                'dispute', 'anger', 'envy', 'work', 'politics',
                'terrorism', 'shame', 'confusion', 'hate']
attributes = ['TOXICITY', 'SEVERE_TOXICITY', 'IDENTITY_ATTACK', 'INSULT',
              'PROFANITY', 'THREAT', 'SEXUALLY_EXPLICIT', 'FLIRTATION']


def make_df():
    filenames = ["0_5000000", "0_10000000", "0_15000000", "0_20000001", "2?2_285042", "2?3_887730", "2?4_6000000",
                 "2?_640000", "2_2390000", "3.1_2180000", "3_7900000", "4.1_4581097", "4.2_320000", "4.3_1050000",
                 "4_2200000", "5.1_2300000", "5.2_6139999", "6.1_2858690", "6.2_6109999", "7.1_3859623"]
    ide = []
    pol = []

    for fname in filenames:
        print(fname)
        p2 = []
        id2 = []
        with open(f"./perspective/perspective_{fname}_val", "rb") as fp:
            persp1 = pickle.load(fp)
        with open(f"./perspective/perspective_{fname}_id", "rb") as fp:
            ide1 = pickle.load(fp)
        ide1 = np.array(ide1)
        for i in range(len(persp1)):
            if len(persp1[i]) == 0:
                continue
            p2.append(np.array([*persp1[i]]))
            id2.append(ide1[i])

        ide.extend(id2)
        pol.extend(p2)
        print(f"len pers = {len(pol)}, len ide = {len(ide)}")

    print(f"type persp[0] = {type(pol[0])}, shape = {pol[0].shape}")
    d_persp = dict(zip(ide, pol))
    print("d_persp", len(d_persp))

    for name in names_list:
        print(name)
        for attri in range(len(attributes)):
            d = {}
            for emotion in emotion_list[1:]:
                d[emotion] = []
                d[f"{emotion}_dyu"] = []
                d[f"{emotion}_dyd"] = []
                d[f"{emotion}_std"] = []
                print(name, attributes[attri], emotion)
                y = []
                for i in range(2010, 2020):
                    y1 = []

                    with open(f"./empath_blob/{name}_empath_{emotion}_{i}", "rb") as f:
                        keys = pickle.load(f)

                    for key in keys:
                        if key in d_persp:
                            y1.append(d_persp[key][attri])
                    y.append(np.array(y1))
                y_mean = []
                y_std = []
                dyu = []
                dyd = []

                count = 2010
                for i in y:
                    y_mean.append(np.mean(i))
                    y_std.append(np.std(i))
                    boot = bootstrap(i)
                    c = boot(.95)
                    if count >= 2017:
                        print(count, c)
                    count += 1
                    dyd.append(c[0])
                    dyu.append(c[1])

                d[emotion] = y_mean
                d[f"{emotion}_dyu"] = dyu
                d[f"{emotion}_dyd"] = dyd
                d[f"{emotion}_std"] = y_std

            df = pd.DataFrame(d)
            df.to_csv(f"./empath_perspective/{name}_{attributes[attri]}_empath.csv")


if __name__ == "__main__":
    make_df()

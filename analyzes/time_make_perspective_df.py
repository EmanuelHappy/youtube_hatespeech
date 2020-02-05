import pickle
import numpy as np
import pandas as pd
from utilities.bootstrap import bootstrap

names_control = ["right-center", "center", "left", "left-center", "right"]
names = ["Alt-right", "IDW", "Alt-lite", "control"]
names_list_list = [["Alt-right"], ["IDW"], ["Alt-lite"], names_control]
bins_t_s = ["2016", "2017", "2018"]

attributes = ['TOXICITY', 'SEVERE_TOXICITY', 'IDENTITY_ATTACK', 'INSULT', 'PROFANITY', 'THREAT', 'SEXUALLY_EXPLICIT',
              'FLIRTATION']
src_path = "./../data/sentiment/values_per_year/perspective/"
dst_path = "./../data/sentiment/dataframes/perspective_df/"

for names_list in names_list_list:
    print(names_list)
    y = []
    x = bins_t_s
    dyu = []
    dyd = []

    for year in bins_t_s:
        y2 = np.array([[]])
        print(year)

        for name in names_list:
            with open(f"{src_path}{name}_perspective_{year} ", "rb") as fp:
                y1 = pickle.load(fp)
                y3 = []
            for i in y1:
                if len(i) == 0:
                    continue
                y3.append(np.array([*i]))

            if y2.size == 0:
                y2 = np.array(y3)
            else:
                y2 = np.concatenate((y2, np.array(y3)))

        print(y2.shape)
        y.append(y2.mean(axis=0))
        dyu_year = []
        dyd_year = []
        print(y2[:, 0].shape)

        for i in range(8):
            if i not in [0, 1, 2]:
                dyd_year.append(y[-1][i])
                dyu_year.append(y[-1][i])
                continue

            boot = bootstrap(y2[:, i])
            c = boot(.95)
            print(c)
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

    for j in range(len(y)):
        for i in range(len(attributes)):
            d[attributes[i]].append(y[j, i])
            d[f"{attributes[i]}_dyu"].append(dyu[j][i])
            d[f"{attributes[i]}_dyd"].append(dyd[j][i])

    df = pd.DataFrame(d)
    df.to_csv(f"{dst_path}{names[names_list_list.index(names_list)]}_perspective.csv")

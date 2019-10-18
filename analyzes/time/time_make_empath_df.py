import pickle
import numpy as np
import pandas as pd
from bootstrap import bootstrap

names_control = ["right-center", "center", "left", "left-center", "right"]
names = ["Alt-right", "IDW", "Alt-lite", "control"]
names_list_list = [["Alt-right"], ["IDW"], ["Alt-lite"], names_control]
emotion_list = ['size', 'sadness', 'independence', 'positive_emotion', 'family', 'negative_emotion', 'government',
                'love', 'ridicule', 'masculine', 'feminine', 'violence', 'suffering', 'dispute', 'anger', 'envy',
                'work', 'politics', 'terrorism', 'shame', 'confusion', 'hate']
bins_t_s = ["2006-2012", "2013-2015", "2016", "2017", "2018"]

src_path = "./../data/sentiment/values_per_year/empath/time/"
dst_path = "./../data/sentiment/dataframes/empath_df/time/"

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
            try:
                with open(f"{src_path}{name}_empath_{year}", "rb") as fp:
                    y1 = pickle.load(fp)
                    if y2.size == 0:
                        y2 = np.array(y1)
                    else:
                        y2 = np.concatenate((y2, np.array(y1)))
            except:
                continue

        print(y2.shape)
        y.append(y2.mean(axis=0))

        dyu_year = []
        dyd_year = []
        print(y2[:, 0].shape)
        for i in range(22):
            if year == "2018" or year == "2017":
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

    for i in range(len(emotion_list)):
        d[emotion_list[i]] = []
        d[f"{emotion_list[i]}_dyu"] = []
        d[f"{emotion_list[i]}_dyd"] = []
    d["year"] = x

    for j in range(len(y)):
        for i in range(len(emotion_list)):
            d[emotion_list[i]].append(y[j, i])
            d[f"{emotion_list[i]}_dyu"].append(dyu[j][i])
            d[f"{emotion_list[i]}_dyd"].append(dyd[j][i])

    df = pd.DataFrame(d)
    df.to_csv(f"{dst_path}{names[names_list_list.index(names_list)]}_empath.csv")

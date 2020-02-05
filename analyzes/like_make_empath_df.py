import pickle
import numpy as np
import pandas as pd
from utilities.bootstrap import bootstrap

names_control = ["right-center", "center", "left", "left-center", "right"]
names = ["Alt-right", "IDW", "Alt-lite", "control"]
names_list_list = [["Alt-right"], ["IDW"], ["Alt-lite"], names_control]
emotion_list = ['size', 'sadness', 'independence', 'positive_emotion', 'family', 'negative_emotion', 'government',
                'love', 'ridicule', 'masculine', 'feminine', 'violence', 'suffering', 'dispute', 'anger', 'envy',
                'work', 'politics', 'terrorism', 'shame', 'confusion', 'hate']
new_emotion_list = ['love', 'ridicule', 'masculine', 'feminine', 'violence', 'anger', 'politics', 'terrorism', 'hate']
bins_like_name = ["0", "1", "2-5", "6-100", "100"]
bins_t_s = ["2016", "2017", "2018"]

src_path = "./../data/sentiment/values_per_year/empath/like/"
dst_path = "./../data/sentiment/dataframes/empath_df/like/"

for like_name in bins_like_name:
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
                    with open(f"{src_path}{name}{like_name}_empath_{year}", "rb") as fp:
                        y1 = pickle.load(fp)
                        if y2.size == 0:
                            y2 = np.array(y1)
                        else:
                            y2 = np.concatenate((y2, np.array(y1)))
                except:
                    print(name, year, like_name, "NOT OPENED")
                    continue

            print(y2.shape)
            y.append(y2.mean(axis=0))

            dyu_year = []
            dyd_year = []
            print(y2[:, 0].shape)
            for i in range(22):
                if emotion_list[i] not in new_emotion_list:
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
        df.to_csv(f"{dst_path}{names[names_list_list.index(names_list)]}{like_name}_empath.csv")

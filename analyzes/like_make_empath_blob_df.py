import pandas as pd
import pickle
import numpy as np
from bootstrap import bootstrap

names_control = ["right-center", "center", "left", "left-center", "right"]
names = ["Alt-right", "IDW", "Alt-lite", "control"]
names_list_list = [["Alt-right"], ["IDW"], ["Alt-lite"], names_control]
emotion_list = ['size', 'sadness', 'independence', 'positive_emotion', 'family',
                'negative_emotion', 'government', 'love', 'ridicule',
                'masculine', 'feminine', 'violence', 'suffering',
                'dispute', 'anger', 'envy', 'work', 'politics',
                'terrorism', 'shame', 'confusion', 'hate']
bins_t_s = ["2016", "2017", "2018"]
bins_like_name = ["0", "1", "2-5", "6-100", "100"]

middle_path = "./../data/sentiment/"
community_path = middle_path + "community_id/like/"
df_path = middle_path + "dataframes/empath_blob_df/like/"
values_path = middle_path + "values_per_year/empath_blob/like/"


def get_ids():
    for like_name in bins_like_name:
        print(like_name)
        for names_list in names_list_list:
            d_empath = {}
            for emotion in emotion_list:
                d_empath[emotion] = {}
                for year in bins_t_s:
                    d_empath[emotion][year] = []

            for name in names_list:
                if name not in ["Alt-right", "IDW", "Alt-lite"]:
                    return 0
                with open(f"{community_path}{name}{like_name}.pickle", "rb") as fp:
                    ks = pickle.load(fp)

                filenames = ["1_4600000", "2_4600000", "3_2400002", "4_3000002", "5_1000001", "6_10000000", "6_20000000",
                             "6_30000000", "6_40000000", "6_50000000", "6_53900001"]
                for fname in filenames:
                    if name == "Alt-right" and fname not in ["6_20000000", "6_30000000", "6_40000000"]:
                        continue
                    if name == "IDW" and fname not in ["6_10000000", "6_20000000", "6_30000000", "6_40000000"]:
                        continue
                    if name == "Alt-lite" and fname in ["1_4600000", "2_4600000", "3_2400002", "4_3000002", "5_1000001"]:
                        continue
                    if name in names_control and fname in ["6_40000000", "6_50000000", "6_53900001"]:
                        continue
                        
                    with open(f"{middle_path}values/empath_val/empath_{fname}_val", "rb") as fp:
                        empath = pickle.load(fp)
                    with open(f"{middle_path}ids/empath_id/empath_{fname}_id", "rb") as fp:
                        ide = pickle.load(fp)
                    print(f"empath and id from {name} loaded")

                    for i in range(len(empath)):
                        if i % 1000000 == 0:
                            print(i)
                        key = ide[i]
                        if key in ks and ks[key] in bins_t_s:
                            for j in range(1, len(emotion_list)):
                                if empath[i][j] > 0:
                                    d_empath[emotion_list[j]][ks[key]].append(key)

                    print(fname, "sadness", len(d_empath["sadness"]["2018"]))
                    print(fname, "positive", len(d_empath["positive_emotion"]["2018"]))

            for emotion in emotion_list:
                for year in bins_t_s:
                    with open(f"{values_path}{names[names_list_list.index(names_list)]}{like_name}_empath_{emotion}_{year}", "wb") as fp:
                        pickle.dump(d_empath[emotion][year], fp, protocol=4)


def make_df():
    ide = []
    pol = []

    filenames = ["0", "1_10000000", "2_10000000", "3_10000000", "4_10000000", "5_10000000", "6_10000000", "7_4989623"]

    for fname in filenames:

        with open(f"{middle_path}values/textblob_pol_val/blob_{fname}_pol", "rb") as fp:
            pol1 = pickle.load(fp)
        print("pol")
        with open(f"{middle_path}ids/textblob_id/blob_{fname}_id_list", "rb") as fp:
            ide1 = pickle.load(fp)

        ide.extend(ide1)
        pol.extend(pol1)
        print(len(pol), len(ide))

    d_pol = dict(zip(ide, pol))
    print("d_pol", len(d_pol))

    for like_name in bins_like_name:
        for name in names:
            print(name, like_name)
            d = {}
            for emotion in emotion_list[1:]:
                d[emotion] = []
                d[f"{emotion}_dyu"] = []
                d[f"{emotion}_dyd"] = []
                d[f"{emotion}_std"] = []
                print(emotion)
                y = []

                for i in bins_t_s:
                    y1 = []
                    with open(f"{values_path}{name}{like_name}_empath_{emotion}_{i}", "rb") as f:
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
            d["year"] = bins_t_s

            df = pd.DataFrame(d)
            df.to_csv(f"{df_path}{name}{like_name}_pol_empath_like.csv")


if __name__ == "__main__":
    get_ids()
    make_df()

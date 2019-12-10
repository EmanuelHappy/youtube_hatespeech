import pickle
import numpy as np
import pandas as pd
from bootstrap import bootstrap

names_control = ["right-center", "center", "left", "left-center", "right"]
names_list = ["Alt-right", "IDW", "Alt-lite", "control"]
names_list_list = [["Alt-right"], ["IDW"], ["Alt-lite"], names_control]
attributes = ['TOXICITY', 'SEVERE_TOXICITY', 'IDENTITY_ATTACK', 'INSULT', 'PROFANITY', 'THREAT', 'SEXUALLY_EXPLICIT',
              'FLIRTATION']
emotion_list = ['size', 'sadness', 'independence', 'positive_emotion', 'family',
                'negative_emotion', 'government', 'love', 'ridicule',
                'masculine', 'feminine', 'violence', 'suffering',
                'dispute', 'anger', 'envy', 'work', 'politics',
                'terrorism', 'shame', 'confusion', 'hate']

bins_t_s = ["2006-2012", "2013-2015", "2016", "2017", "2018"]

middle_path = "./../data/sentiment/"
community_path = middle_path + "community_id/"
id_path = middle_path + "ids/perspective_id/"
val_path = middle_path + "values/perspective_val/"
dst_path = middle_path + "values_per_year/perspective_attr/"
df_path = middle_path + "dataframes/empath_perspective/"


def get_ids():
    c = 0
    for names in [names_control]:
        d_persp = {}
        for attr in attributes:
            d_persp[attr] = {}
            for year in bins_t_s:
                d_persp[attr][year] = []
        for name in names:
            print(name)
            with open(f"{community_path}{name}.pickle", "rb") as fp:
                ks = pickle.load(fp)

            filenames = ["0_5000000", "0_10000000", "0_15000000", "0_20000001", "0_20369999", "1_3626600", "2_2390000",
                         "2.1_640000", "2.2_285042", "2.3_887730", "2.4_6000000", "3_7900000", "3.1_2180000",
                         "4.1_4581097", "4.2_320000", "4.3_1050000", "4_2200000", "5.1_2300000", "5.2_6139999",
                         "6.1_2858690", "6.2_6109999", "7.1_3859623"]

            for fname in filenames:
                with open(f"{val_path}perspective_{fname}_val", "rb") as fp:
                    perspective = pickle.load(fp)
                print("perspective")
                with open(f"{id_path}perspective_{fname}_id", "rb") as fp:
                    ide = pickle.load(fp)
                print("id")

                p2 = []
                id2 = []
                ide = np.array(ide)
                for i in range(len(perspective)):
                    if len(perspective[i]) == 0:
                        continue
                    p2.append(np.array([*perspective[i]]))
                    id2.append(ide[i])
                perspective = np.array(p2)
                ide = np.array(id2)
                print("perspective shape ", perspective.shape, "ide shape ", ide.shape)
                a = perspective > 0.5
                for i in range(8):
                    for key in ide[a[:, i]]:
                        if key in ks:
                            d_persp[attributes[i]][ks[key]].append(key)

                print(fname, "TOXICITY", len(d_persp["TOXICITY"]["2018"]))
                print(fname, "IDENTITY_ATTACK", len(d_persp["IDENTITY_ATTACK"]["2018"]))

        for attr in attributes:
            for year in bins_t_s:
                with open(f"{dst_path}control_{attr}_{year}", "wb") as fp:
                    pickle.dump(d_persp[attr][year], fp, protocol=4)
        c += 1


def make_df():
    ide = []
    emp = []
    filenames = ["1_4600000", "2_4600000", "3_2400002", "4_3000002", "5_1000001", "6_10000000", "6_20000000",
                     "6_30000000", "6_40000000", "6_50000000", "6_53900001"]

    for fname in filenames:
        with open(f"{middle_path}values/empath_val/empath_{fname}_val", "rb") as fp:
            emp1 = pickle.load(fp)
        with open(f"{middle_path}ids/empath_id/empath_{fname}_id", "rb") as fp:
            ide1 = pickle.load(fp)

        ide.extend(ide1)
        emp.extend(emp1)
        print(fname, len(emp), len(ide))

    d_emp = dict(zip(ide, emp))
    print("d_emp", len(d_emp))

    #for name in names_list:
    #    print(name)
    name = "control"
    for attr in attributes:
        print(attr)
        d = {"year": bins_t_s}

        for emotion in emotion_list[1:]:
            d[emotion] = []
            d[f"{emotion}_dyu"] = []
            d[f"{emotion}_dyd"] = []

        for year in bins_t_s:
            id_persp = np.array([[]])
            
            print(name, attr, year)
            with open(f"{dst_path}{name}_{attr}_{year}", "rb") as fp:
                id_persp = pickle.load(fp)
            y_emp = []

            for ide in id_persp:
                if ide in d_emp:
                    y_emp.append(d_emp[ide])
            print("y_emp created")
            y_emp = np.array(y_emp)
            for i in range(1, len(emotion_list)):
                y_at = y_emp[:, i]
                emotion = emotion_list[i]
                d[emotion].append(np.mean(y_at))

                if year == "2017" or year == "2018":
                    d[f"{emotion}_dyd"].append(d[emotion][-1])
                    d[f"{emotion}_dyu"].append(d[emotion][-1])
                    continue

                boot = bootstrap(y_at)
                c = boot(.95)

                d[f"{emotion}_dyd"].append(c[0])
                d[f"{emotion}_dyu"].append(c[1])

        df = pd.DataFrame(d)
        df.to_csv(f"{df_path}control_{attr}_empath.csv")


if __name__ == "__main__":
    #get_ids()
    make_df()

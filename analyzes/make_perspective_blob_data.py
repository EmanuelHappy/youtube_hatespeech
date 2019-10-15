import pickle
import numpy as np

names_control = ["right-center", "center", "left", "left-center", "right1", "right2"]
names_list = ["Alt-right", "IDW", "Alt-lite", "control"]
names_list_list = [["Alt-right"], ["IDW"], ["Alt-lite"], names_control]
attributes = ['TOXICITY', 'SEVERE_TOXICITY', 'IDENTITY_ATTACK', 'INSULT', 'PROFANITY', 'THREAT', 'SEXUALLY_EXPLICIT',
              'FLIRTATION']


def get_ids():
    c = 0
    for names in names_list_list:
        d_persp = {}
        for attr in attributes:
            d_persp[attr] = {}
            for year in range(2006, 2020):
                d_persp[attr][year] = []
        for name in names:
            print(name)
            with open(f"{name}.pickle", "rb") as fp:
                ks = pickle.load(fp)

            filenames = ["0_5000000", "0_10000000", "0_15000000", "0_20000001", "2?2_285042", "2?3_887730",
                         "2?4_6000000",
                         "2?_640000", "2_2390000", "3.1_2180000", "3_7900000", "4.1_4581097", "4.2_320000",
                         "4.3_1050000",
                         "4_2200000", "5.1_2300000", "5.2_6139999", "6.1_2858690", "6.2_6109999", "7.1_3859623"]

            for fname in filenames:
                with open(f"./perspective/perspective_{fname}_val", "rb") as fp:
                    perspective = pickle.load(fp)
                print("perspective")
                with open(f"./perspective/perspective_{fname}_id", "rb") as fp:
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

                print(fname, "TOXICITY", len(d_persp["TOXICITY"][2018]))
                print(fname, "IDENTITY_ATTACK", len(d_persp["IDENTITY_ATTACK"][2018]))

        for attr in attributes:
            for year in range(2010, 2020):
                with open(f"./perspective_blob/{names_list[c]}_{attr}_{year}", "wb") as fp:
                    pickle.dump(d_persp[attr][year], fp, protocol=4)
        c += 1


if __name__ == "__main__":
    get_ids()

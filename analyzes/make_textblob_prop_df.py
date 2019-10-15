import pickle
import numpy as np
import pandas as pd

names_control = ["right-center", "center", "left", "left-center", "right"]
names = ["Alt-right", "IDW", "Alt-lite", "control"]
names_list_list = [["Alt-right"], ["IDW"], ["Alt-lite"], names_control]

src_path = "./../data/sentiment/values_per_year/textblob/"
dst_path = "./../data/sentiment/dataframes/text_blob_proportion_df/"


def make_df(blob, dif):
    for names_list in names_list_list:
        pos = []
        neu = []
        neg = []
        print(names_list, "Polarity")
        x = []
        for year in range(2007, 2020):
            y2 = np.array([])
            print(year)

            for name in names_list:
                try:
                    with open(f"{src_path}{name}_{blob}_{year}", "rb") as fp:
                        y1 = pickle.load(fp)
                        y2 = np.concatenate((y2, np.array(y1)), axis=None)
                except:
                    print(name, year)
                    continue

            pos.append(np.sum(y2 > dif) / len(y2))
            neg.append(np.sum(y2 < -dif) / len(y2))
            neu.append(1 - pos[-1] - neg[-1])
        pos = np.array(pos)
        neg = np.array(neg)
        neu = np.array(neu)

        df = pd.DataFrame({"x": x, "pos": pos, "neg": neg, "neu": neu})
        df.to_csv(f"{dst_path}{names[names_list_list.index(names_list)]}_{blob}_prop.csv")


if __name__ == "__main__":
    make_df(blob="pol", dif=0.1)
    make_df(blob="subj", dif=0.5)

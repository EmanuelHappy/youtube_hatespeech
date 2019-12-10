import pickle
import numpy as np
import pandas as pd
from bootstrap import bootstrap

names_control = ["right-center", "center", "left", "left-center", "right"]
names = ["Alt-right", "IDW", "Alt-lite", "control"]
names_list_list = [["Alt-right"], ["IDW"], ["Alt-lite"], names_control]

cat = ["pol"]
bins_t_s = ["2016", "2017", "2018"]

src_path = "./../data/sentiment/values_per_year/textblob/"
dst_path = "./../data/sentiment/dataframes/text_blob_df/"

for names_list in names_list_list:
    print(names_list)
    for blob in cat:
        y = []
        x = bins_t_s

        for year in bins_t_s:
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

            y.append(y2)

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

        df = pd.DataFrame({"x": x, "y": y_mean, "dyd": dyd, "dyu": dyu, "std": y_std})
        df.to_csv(f"{dst_path}{names[names_list_list.index(names_list)]}_{blob}.csv")

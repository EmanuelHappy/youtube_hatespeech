import pickle
import numpy as np
import pandas as pd
from bootstrap import bootstrap

names_control = ["right-center", "center", "left", "left-center", "right"]
names = ["Alt-right", "IDW", "Alt-lite", "control"]
names_list_list = [["Alt-right"], ["IDW"], ["Alt-lite"], names_control]
bins_like_name = ["0", "1", "2-5", "6-100", "100"]

cat = ["pol"]
bins_t_s = ["2016", "2017", "2018"]

src_path = "./../data/sentiment/values_per_year/textblob/like/"
dst_path = "./../data/sentiment/dataframes/text_blob_df/like/"

for like_name in bins_like_name:
    for names_list in names_list_list:
        if names_list in [["Alt-right"], ["IDW"]] and like_name == "0": continue
        print(names_list, like_name)
        for blob in cat:
            y = []
            x = bins_t_s

            for year in bins_t_s:
                y2 = np.array([])
                print(year)

                for name in names_list:
                    print(name)
                    try:
                        with open(f"{src_path}{name}{like_name}_{blob}_{year}", "rb") as fp:
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
            df.to_csv(f"{dst_path}{names[names_list_list.index(names_list)]}{like_name}_{blob}.csv")

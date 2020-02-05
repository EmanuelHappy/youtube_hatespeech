import pickle
import numpy as np
import argparse

parser = argparse.ArgumentParser(description="""This script creates a new sqlite database,
                                                based on textblob scores of each youtube comment.""")

parser.add_argument("--src", dest="src", type=str, default="./../../data/sentiment/",
                    help="Sqlite DataBase source of the comments.")

parser.add_argument("--dst", dest="dst", type=str, default="./../../data/sentiment/values_per_year/textblob/like/",
                    help="Sqlite DataBase to store the textblob values.")

parser.add_argument("--name", dest="name", type=str, default="IDW",
                    help="Name of the community to create textblob files")

args = parser.parse_args()

bins_t_s = ["2006-2012", "2013-2015", "2016", "2017", "2018"]
names_list = ["right-center0", "Alt-right0", "center0", "left0", "left-center0", "IDW0", "Alt-lite0",
              "right-center1", "Alt-right1", "center1", "right1", "left1", "left-center1", "IDW1", "Alt-lite1",
              "right-center2-5", "Alt-right2-5", "center2-5", "right2-5", "left2-5", "left-center2-5", "IDW2-5",
              "Alt-lite2-5",
              "right-center6-100", "Alt-right6-100", "center6-100", "right6-100", "left6-100", "left-center6-100",
              "IDW6-100", "Alt-lite6-100",
              "right-center100", "Alt-right100", "center100", "right100", "left100", "left-center100", "IDW100",
              "Alt-lite100"]
names_list = ['right0']
middle_path = "./../../data/sentiment/"
community_path = "./../../data/sentiment/community_id/like/"


def make_values_by_year():
    # Values to change
    with open("./../../data/sentiment/ids/removed_ids/change_ids.pickle", "rb") as fp:
        changed = pickle.load(fp)
    print("changed")
    with open("./../../data/sentiment/ids/removed_ids/remove_ids.pickle", "rb") as fp:
        removed = pickle.load(fp)
    print("removed")
    ks_change = dict()
    t_remove = 0

    # filenames = ["0", "1_10000000", "2_10000000", "3_10000000", "4_10000000", "5_10000000", "6_10000000", "7_4989623"]
    with open(f"{args.src}values/textblob_pol_val/all_polarity.pickle", "rb") as fp:
        pol = pickle.load(fp)
    with open(f"{args.src}ids/textblob_id/all_keys.pickle", "rb") as fp:
        ide = pickle.load(fp)
    print(len(pol), len(ide))
    d1 = dict(zip(ide, pol))
    del ide
    del pol
    ide = pol = []

    for name in names_list:
        with open(f"{community_path}{name}.pickle", "rb") as fp:
            ks = pickle.load(fp)
        id_likes = list(ks.keys())

        # update new key
        print(len(ks))
        ks.update(ks_change)
        print(len(ks))
        id_likes.extend(list(ks_change.keys()))
        if len(ks_change) > 0: flag = False
        else: flag = True
        ks_change = {}

        d_pol = {}
        for year in bins_t_s:
            d_pol[year] = []

        for i in range(len(id_likes)):
            if i % 1000000 == 0:
                print(i)
            key = id_likes[i]
            if key in d1:
                if key not in removed and (not flag or key not in changed):
                    d_pol[ks[key]].append(d1[key])
                elif key in changed:
                    ks_change[key] = ks[key]
                elif flag and key in removed:
                    t_remove += 1
        print(name, 'len 2018', len(d_pol['2018']), 'change', len(ks_change), 'remove', t_remove)
        t_remove = 0

        for i in bins_t_s:
            print(i)
            with open(f"{args.dst}{name}_pol_{i}", "wb") as f:
                pickle.dump(tuple(np.array(d_pol[i])), f, protocol=4)


if __name__ == "__main__":
    make_values_by_year()

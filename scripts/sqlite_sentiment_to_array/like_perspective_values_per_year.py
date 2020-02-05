import pickle
import numpy as np
import argparse
from sqlitedict import SqliteDict
from time import time

parser = argparse.ArgumentParser(description="""This script creates a new sqlite database,
                                                based on perspective scores of each youtube comment.""")

parser.add_argument("--src", dest="src", type=str, default="./../../data/sqlite/perspective_sqlite/",
                    help="Sqlite DataBase source of the comments.")

parser.add_argument("--dst", dest="dst", type=str, default="./../../data/sentiment/values_per_year/perspective/like/",
                    help="Sqlite DataBase to store the perspective values.")

parser.add_argument("--name", dest="name", type=str, default="IDW",
                    help="Name of the community to create perspective files")

args = parser.parse_args()

bins_t_s = ["2006-2012", "2013-2015", "2016", "2017", "2018"]
names_list = ["IDW0", "Alt-lite0",
              "right-center1", "Alt-right1", "center1", "right1", "left1", "left-center1", "IDW1", "Alt-lite1",
              "right-center2-5", "Alt-right2-5", "center2-5", "right2-5", "left2-5", "left-center2-5", "IDW2-5",
              "Alt-lite2-5",
              "right-center6-100", "Alt-right6-100", "center6-100", "right6-100", "left6-100", "left-center6-100",
              "IDW6-100", "Alt-lite6-100",
              "right-center100", "Alt-right100", "center100", "right100", "left100", "left-center100", "IDW100",
              "Alt-lite100"]
middle_path = "./../../data/sentiment/"
community_path = "./../../data/sentiment/community_id/like/"


def sqlite_to_array(num):

    p2 = SqliteDict(f"{args.src}perspective_value{num}.sqlite", tablename="value", flag="r")

    c = 0
    t_ini = time()
    ids = []
    perspective = []

    for key, value in p2.items():
        if c % 100000 == 0:
            print("iteration number ", c, "at", round((time()-t_ini)/60, 2), "minutes")
        c += 1

        if c % 5000000 == 0:
            save_arrays(num, perspective, ids, c)
            ids = []
            perspective = []

        ids.append(key)
        perspective.append(tuple(value.values()))
    c += 1
    save_arrays(num, perspective, ids, c)


def save_arrays(num, perspective, ids, c):
    print(":D")
    with open(f"{middle_path}values/perspective_val/perspective_{num}_{c}_val", "wb") as f:
        pickle.dump(np.array(perspective), f, protocol=4)
    print("Val")
    with open(f"{middle_path}ids/perspective_id/perspective_{num}_{c}_id", "wb") as f:
        pickle.dump(tuple(np.array(ids)), f, protocol=4)
    print("ID")


def make_values_by_year():
    with open("./../../data/sentiment/ids/removed_ids/change_ids.pickle", "rb") as fp:
        changed = pickle.load(fp)
    print("changed")
    with open("./../../data/sentiment/ids/removed_ids/remove_ids.pickle", "rb") as fp:
        removed = pickle.load(fp)
    print("removed")
    ks_change = dict()
    t_remove = 0

    ide = np.array([[]])
    perspective = np.array([[]])
    filenames = ["0_5000000", "0_10000000", "0_15000000", "0_20000001", "2_2390000", "2.1_640000", "2.2_285042",
                 "2.3_887730", "2.4_6000000", "3_7900000", "3.1_2180000", "4.1_4581097", "4.2_320000", "4.3_1050000",
                 "4_2200000", "5.1_2300000", "5.2_6139999", "6.1_2858690", "6.2_6109999", "7.1_3859623"]

    for fname in filenames:
        with open(f"{middle_path}values/perspective_val/perspective_{fname}_val", "rb") as fp:
            perspective1 = pickle.load(fp)
            perspective2 = []
            for i in perspective1:
                if len(i) != 0:
                    perspective2.append([*i])
            perspective1 = np.array(perspective2)
        with open(f"{middle_path}ids/perspective_id/perspective_{fname}_id", "rb") as fp:
            ide1 = pickle.load(fp)
            ide1 = np.array(ide1)
        if fname == filenames[0]:
            ide = ide1
            perspective = perspective1
        else:
            perspective = np.concatenate([perspective, perspective1])
            ide = np.concatenate([ide, ide1])
        print(fname, len(ide))
    d = dict(zip(ide, perspective))

    for name in names_list:
        with open(f"{community_path}{name}.pickle", "rb") as fp:
            ks = pickle.load(fp)
        id_likes = list(ks.keys())

        # update new key
        ks.update(ks_change)
        id_likes.extend(list(ks_change.keys()))
        if len(ks_change) > 0: flag = False
        else: flag = True
        ks_change = {}

        d_persp = {}
        for year in bins_t_s:
            d_persp[year] = []

        for i in range(len(id_likes)):
            if i % 1000000 == 0:
                print(i)
            key = id_likes[i]
            if key in d:
                if key not in removed and (not flag or key not in changed):
                    d_persp[ks[key]].append(d[key])
                elif flag and key in changed:
                    ks_change[key] = ks[key]
                elif key in removed:
                    t_remove += 1
        print(name, 'len 2018', len(d_persp['2018']), 'change', len(ks_change), 'remove', t_remove)

        for i in bins_t_s:
            print(i)
            with open(f"{args.dst}{name}_perspective_{i} ", "wb") as f:
                pickle.dump(tuple(np.array(d_persp[i])), f, protocol=4)


if __name__ == "__main__":
    #pers_files = [0, 1, 2, 2.0, 2.1, 2.2, 2.3, 2.4, 3.1, 3, 4, 4.1, 4.2, 4.3, 5.1, 5.2, 6.1, 6.2, 7.1]
    #for number_file in pers_files:
    #    sqlite_to_array(number_file)

    #for comm in names_list:
    make_values_by_year()

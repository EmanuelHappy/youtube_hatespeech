import pickle
from sqlitedict import SqliteDict
import numpy as np
from time import time
import argparse

parser = argparse.ArgumentParser(description="""This script creates a new sqlite database,
                                                based on empath scores of each youtube comment.""")

parser.add_argument("--src", dest="src", type=str, default="./../../data/sqlite/empath_sqlite/",
                    help="Sqlite DataBase source of the comments.")

parser.add_argument("--dst", dest="dst", type=str, default="./../../data/sentiment/values_per_year/empath/like/",
                    help="Sqlite DataBase to store the empath values.")

parser.add_argument("--name", dest="name", type=str, default="IDW",
                    help="Name of the community to create empath files")

args = parser.parse_args()

bins_t_s = ["2006-2012", "2013-2015", "2016", "2017", "2018"]
bins_like_name = ["0", "1", "2-5", "6-100", "100"]
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
    emp_sql = SqliteDict(f"{args.src}empath_value{num}.sqlite", tablename="value", flag="r")
    t_ini = time()
    ids = []
    emp_values = []
    c = 0

    for key, value in emp_sql.items():
        if c % 1000000 == 0:
            print("iteration number ", c, "at", round((time() - t_ini) / 60, 2), "minutes")
        c += 1

        ids.append(key)
        emp_values.append(tuple(value.values()))

        if c % 10000000 == 0:
            save_arrays(num, emp_values, ids, c)
            ids = []
            emp_values = []

    save_arrays(num, emp_values, ids, c)


def save_arrays(num, emp_values, emp_ids, count):
    print(":D")
    with open(f"{middle_path}values/empath_val/empath_{num}_{count}_val", "wb") as f:
        pickle.dump(np.array(emp_values), f, protocol=4)
    print("Val")
    with open(f"{middle_path}ids/empath_id/empath_{num}_{count}_id", "wb") as f:
        pickle.dump(tuple(np.array(emp_ids)), f, protocol=4)
    print("ID")


def make_values_by_year():
    print("start")
    # Values to change
    with open("./../../data/sentiment/ids/removed_ids/change_ids.pickle", "rb") as fp:
        changed = pickle.load(fp)
    print("changed")
    with open("./../../data/sentiment/ids/removed_ids/remove_ids.pickle", "rb") as fp:
        removed = pickle.load(fp)
    print("removed")
    ks_change = dict()
    t_remove = 0

    ide = np.array([[]])
    empath = np.array([[]])
    filenames = ["1_4600000", "2_4600000", "3_2400002", "4_3000002", "5_1000001", "6_10000000", "6_20000000",
                 "6_30000000", "6_40000000", "6_50000000", "6_53900001"]

    for fname in filenames:
        with open(f"{middle_path}values/empath_val/empath_{fname}_val", "rb") as fp:
            empath1 = pickle.load(fp)
        with open(f"{middle_path}ids/empath_id/empath_{fname}_id", "rb") as fp:
            ide1 = pickle.load(fp)
        if fname == filenames[0]:
            ide = ide1
            empath = empath1
        else:
            empath = np.concatenate([empath, empath1])
            ide = np.concatenate([ide, ide1])
        print(fname, len(ide))
    d = dict(zip(ide, empath))
    del ide1
    del ide
    del empath1
    del empath
    ide1 = ide = empath1 = empath = []
    for name in names_list:
        with open(f"{community_path}{name}.pickle", "rb") as fp:
            ks = pickle.load(fp)
        id_likes = list(ks.keys())

        # update new key
        ks.update(ks_change)
        id_likes.extend(list(ks_change.keys()))
        if len(ks_change) > 0:
            flag = False
        else:
            flag = True
        ks_change = dict()

        d_emp = {}
        for year in bins_t_s:
            d_emp[year] = []

        for i in range(len(id_likes)):
            if i % 1000000 == 0:
                print(i)
            key = id_likes[i]
            if key in d:
                if key not in removed and (not flag or key not in changed):
                    d_emp[ks[key]].append(d[key])
                elif flag and key in changed:
                    ks_change[key] = ks[key]
                elif key in removed:
                    t_remove += 1
        print(name, 'len 2018', len(d_emp['2018']), 'change', len(ks_change), 'remove', t_remove)
        t_remove = 0

        for i in bins_t_s:
            print(i)
            with open(f"{args.dst}{name}_empath_{i}", "wb") as f:
                pickle.dump(tuple(np.array(d_emp[i])), f, protocol=4)


if __name__ == "__main__":

    make_values_by_year()

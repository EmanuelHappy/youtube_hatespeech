import pickle
from sqlitedict import SqliteDict
import numpy as np
from time import time
import argparse

parser = argparse.ArgumentParser(description="""This script creates a new sqlite database,
                                                based on empath scores of each youtube comment.""")

parser.add_argument("--src", dest="src", type=str, default="./../../../data/sqlite/empath_sqlite/",
                    help="Sqlite DataBase source of the comments.")

parser.add_argument("--dst", dest="dst", type=str, default="./../../../data/sentiment/values_per_year/empath/",
                    help="Sqlite DataBase to store the empath values.")

parser.add_argument("--name", dest="name", type=str, default="IDW",
                    help="Name of the community to create empath files")

args = parser.parse_args()

bins_t_s = ["2006-2012", "2013-2015", "2016", "2017", "2018"]
names_list = ["right-center", "Alt-right", "center", "right", "left", "left-center", "IDW", "Alt-lite"]
middle_path = "./../../../data/sentiment/"
community_path = "./../../../data/sentiment/community_id/"


def sqlite_to_array(num):
    emp_sql = SqliteDict(f"{args.src}empath_value{num}.sqlite", tablename="value", flag="r")
    t_ini = time()
    ids = []
    emp_values = []
    c = 0

    for key, value in emp_sql.items():
        if c % 1000000 == 0:
            print("iteration number ", c, "at", round((time()-t_ini)/60, 2), "minutes")
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

# Values to change
with open("./../../../data/sentiment/ids/removed_ids/change_ids.pickle", "rb") as fp:
    changed = pickle.load(fp)
print("changed")
with open("./../../../data/sentiment/ids/removed_ids/remove_ids.pickle", "rb") as fp:
    removed = pickle.load(fp)
print("removed")
to_change_id = []
to_change_emp = []


def make_values_by_year(name):
    with open(f"{community_path}{name}.pickle", "rb") as fp:
        ks = pickle.load(fp)

    d_emp = {}
    for year in bins_t_s:
        d_emp[year] = []

    filenames = ["1_4600000", "2_4600000", "3_2400002", "4_3000002", "5_1000001", "6_10000000", "6_20000000",
                 "6_30000000", "6_40000000", "6_50000000", "6_53900001"]

    for fname in filenames:
        with open(f"{middle_path}values/empath_val/empath_{fname}_val", "rb") as fp:
            empath = pickle.load(fp)
        with open(f"{middle_path}ids/empath_id/empath_{fname}_id", "rb") as fp:
            ide = pickle.load(fp)
        print("empath", fname)

        if name == "Alt-lite":
            empath = list(empath)
            empath.extend(to_change_emp)
            ide = list(ide)
            ide.extend(to_change_id)
        t_remove = 0

        for i in range(len(empath)):
            if i % 1000000 == 0:
                print(i)
            key = ide[i]
            if key in ks:
                if name != "Alt-lite" and key in changed:
                    to_change_id.append(key)
                    to_change_emp.append(empath[i])
                elif key not in removed:
                    d_emp[ks[key]].append(empath[i])
                else:
                    t_remove += 1

        print(fname, "len", len(d_emp['2018']), "removed = ", t_remove, "changed = ", len(to_change_id))

    for i in bins_t_s:
        print(i)
        with open(f"{args.dst}{name}_empath_{i}", "wb") as f:
            pickle.dump(tuple(np.array(d_emp[i])), f, protocol=4)


if __name__ == "__main__":
    #for number_file in range(1, 7):
    #    sqlite_to_array(number_file)

    for comm in names_list:
        make_values_by_year(comm)

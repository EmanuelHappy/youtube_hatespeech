import pickle
from sqlitedict import SqliteDict
import numpy as np
from time import time
import argparse

parser = argparse.ArgumentParser(description="""This script creates a new sqlite database,
                                                based on empath scores of each youtube comment.""")

parser.add_argument("--src", dest="src", type=str, default="/../../../scratch/manoelribeiro/helpers/text_dict.sqlite",
                    help="Source folder of the comments.")

parser.add_argument("--dst", dest="dst", type=str, default="./../sentiment/empath/sqlite/empath_value.sqlite",
                    help="Where to save the output files.")

parser.add_argument("--name", dest="name", type=str, default="IDW",
                    help="Name of the community to create empath files")

args = parser.parse_args()


def sqlite_to_array(num):
    emp_sql = SqliteDict(f"empath_value{num}.sqlite", tablename="value", flag="r")
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
            save_arrays(emp_values, ids, c)
            ids = []
            emp_values = []

    save_arrays(emp_values, ids, c)


def save_arrays(emp_values, emp_ids, count):
    print(":D")
    with open(f"empath_6_{count}_val", "wb") as f:
        pickle.dump(np.array(emp_values), f, protocol=4)
    print("Val")
    with open(f"empath_6_{count}_id", "wb") as f:
        pickle.dump(tuple(np.array(emp_ids)), f, protocol=4)
    print("ID")


def make_values_by_year(name):
    with open(f"{name}.pickle", "rb") as fp:
        ks = pickle.load(fp)

    d_emp = {}
    for year in range(2006, 2020):
        d_emp[year] = []

    filenames = ["1_4600000", "2_4600000", "3_2400002", "4_3000002", "5_1000001", "6_10000000", "6_20000000",
                 "6_30000000", "6_40000000", "6_50000000", "6_53900001"]

    for fname in filenames:
        with open(f"empath_{fname}_val", "rb") as fp:
            empath = pickle.load(fp)
        print("perspective")
        with open(f"empath_{fname}_id", "rb") as fp:
            ide = pickle.load(fp)
        print("id")

        for i in range(len(empath)):
            if i % 1000000 == 0:
                print(i)
            key = ide[i]
            if key in ks:
                d_emp[ks[key]].append(empath[i])

        print(fname, len(d_emp[2018]))

    for i in range(2007, 2020):
        print(i)
        with open(f"{name}_empath_{i}", "wb") as f:
            pickle.dump(tuple(np.array(d_emp[i])), f, protocol=4)


if __name__ == "__main__":
    for number_file in range(1, 7):
        sqlite_to_array(number_file)

    make_values_by_year(args.name)

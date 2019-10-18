import pickle
import numpy as np
import argparse

parser = argparse.ArgumentParser(description="""This script creates a new sqlite database,
                                                based on textblob scores of each youtube comment.""")

parser.add_argument("--src", dest="src", type=str, default="./../../data/sentiment/",
                    help="Sqlite DataBase source of the comments.")

parser.add_argument("--dst", dest="dst", type=str, default="./../../data/sentiment/values_per_year/textblob/time/",
                    help="Sqlite DataBase to store the textblob values.")

parser.add_argument("--name", dest="name", type=str, default="IDW",
                    help="Name of the community to create textblob files")

args = parser.parse_args()

bins_t_s = ["2006-2012", "2013-2015", "2016", "2017", "2018"]
names_list = ["right-center", "Alt-right", "center", "right", "left", "left-center", "IDW", "Alt-lite"]
middle_path = "./../../data/sentiment/"
community_path = "./../../data/sentiment/community_id/time/"


def make_values_by_year(name):
    with open(f"{community_path}{name}.pickle", "rb") as fp:
        ks = pickle.load(fp)

    d_pol = {}
    d_subj = {}
    for year in bins_t_s:
        d_pol[year] = []
        d_subj[year] = []

    filenames = ["0", "1_10000000", "2_10000000", "3_10000000", "4_10000000", "5_10000000", "6_10000000", "7_4989623"]

    for fname in filenames:
        with open(f"{args.src}values/textblob_subj_val/blob_{fname}_subj", "rb") as fp:
            subj = pickle.load(fp)
        print("subj")
        with open(f"{args.src}values/textblob_pol_val/blob_{fname}_pol", "rb") as fp:
            pol = pickle.load(fp)
        print("pol")
        with open(f"{args.src}ids/textblob_id/blob_{fname}_id_list", "rb") as fp:
            ide = pickle.load(fp)
        print("id")

        for i in range(len(pol)):
            if i % 1000000 == 0:
                print(i)
            key = ide[i]
            if key in ks:
                d_pol[ks[key]].append(pol[i])
                d_subj[ks[key]].append(subj[i])

        print(fname, len(d_pol['2018']))

    for i in bins_t_s:
        print(i)
        with open(f"{args.dst}{name}_pol_{i}", "wb") as f:
            pickle.dump(tuple(np.array(d_pol[i])), f, protocol=4)
        with open(f"{args.dst}{name}_subj_{i}", "wb") as f:
            pickle.dump(tuple(np.array(d_subj[i])), f, protocol=4)


if __name__ == "__main__":
    for comm in names_list:
        make_values_by_year(comm)

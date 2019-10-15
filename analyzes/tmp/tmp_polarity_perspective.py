"""
ide = []
pol = []
d_emp={2006:[], 2007:[], 2008:[], 2009:[], 2010:[], 2011:[], 2012:[], 2013:[], 2014:[], 2015:[], 2016:[], 2017:[], 2018:[], 2019:[]}
filenames = ["3.1_2180000", "3_7900000", "4.1_4581097", "4.2_320000", "4.3_1050000", "4_2200000", "5.1_2300000", "5.2_6139999", "6.1_2858690", "6.2_6109999", "7.1_3859623"]
for fname in filenames:

    if fname!="n":
        with open(f"blobm_{fname}_pol", "rb") as fp:
            pol1 = pickle.load(fp)
        print("pol")
        with open(f"blobm_{fname}_id_list", "rb") as fp:
            ide1 = pickle.load(fp)
    else:
        with open(f"blob_{fname}_pol", "rb") as fp:
            pol1 = pickle.load(fp)
        print("pol")
        with open(f"blob_{fname}_id", "rb") as fp:
            ide1 = pickle.load(fp)
    ide.extend(ide1)
    pol.extend(pol1)
    print(len(pol), len(ide))
d_pol = dict(zip(ide, pol))
print("d_pol", len(d_pol))


for name in names_list:
    print(name)

    with open(f"blob_n_id", "rb") as f:
        ide = pickle.load(f)
    print("id")
    with open(f"blob_n_pol", "rb") as f:
        pol = pickle.load(f)
    print("pol")
    with open(f"blob_n_sub", "rb") as f:
        sub = pickle.load(f)
    print("sub")

    d_subj = dict(zip(ide, sub))
    print("d_sub")
    y_emotion = []
    dif=0.1
    d = {}
    for emotion in attributes:
        d[emotion] = []
        d[f"{emotion}_dyu"] = []
        d[f"{emotion}_dyd"] = []
        d[f"{emotion}_std"] = []
        print(emotion)
        y_mean = []
        pos = []
        neu = []
        neg = []
        y=[]
        for i in range(2007, 2020):
            y1 = []
            with open(f"./perspective_blob/{name}_perspective_{emotion}_{i}", "rb") as f:
                keys = pickle.load(f)
            for key in keys:
                if key in d_pol:
                    y1.append(d_pol[key])
            y.append(np.array(y1))
        print(len(y), y[0])
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
        d[emotion] = y_mean
        d[f"{emotion}_dyu"] = dyu
        d[f"{emotion}_dyd"] = dyd
        d[f"{emotion}_std"] = y_std

    d["year"] = [i for i in range(2007, 2020)]

    df = pd.DataFrame(d)
    #df = pd.DataFrame({"x":x, "y":y_mean, "std":y_std})
    df.to_csv(f"./perspective_blob/{name}_pol_perspective_prop_boots.csv")

            #pos.append(np.sum(np.array(y)>dif)/len(np.array(y)))
            #neg.append(np.sum(np.array(y)<-dif)/len(np.array(y)))
            #neu.append(1-pos[-1]-neg[-1])
        #y_emotion.append((np.array(neg), np.array(neu), np.array(pos)))
        #print(len(y_emotion), len(pos), len(y))
    #with open(f"./empath_blob/{name}_pol_empath_prop", "wb") as f:
    #    pickle.dump(y_emotion, f)"""

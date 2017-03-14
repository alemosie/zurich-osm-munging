import matplotlib.pyplot as plt
import numpy as np

def make_pie(sizes, text,colors,labels):
    # http://stackoverflow.com/questions/36296101/donut-chart-python

    col = [[i/255. for i in c] for c in colors]

    fig, ax = plt.subplots()
    ax.axis('equal')
    width = 0.35
    kwargs = dict(colors=col, startangle=180, autopct='%1.1f%%')
    outside, _, _ = ax.pie(sizes, radius=1, pctdistance=1-width/2,
                           labels=labels,**kwargs)
    plt.setp( outside, width=width, edgecolor='white')

    kwargs = dict(size=14, fontweight='bold', va='center')
    ax.text(0, 0, text, ha='center', **kwargs)
    plt.show()


if __name__ == "__main__":

    # mongo results set
    top_5 = [{ "_id" : { "user" : "mdk", "uid" : "178186" }, "count" : 566235 },
    { "_id" : { "user" : "SimonPoole", "uid" : "92387" }, "count" : 334879 },
    { "_id" : { "user" : "Sarob", "uid" : "1218134" }, "count" : 146217 },
    { "_id" : { "user" : "hecktor", "uid" : "465052" }, "count" : 117316 },
    { "_id" : { "user" : "feuerstein", "uid" : "194843" }, "count" : 102162 }]

    total = 3146959

    counts = {}
    for user in top_5:
        username = user["_id"]["user"]
        counts[username] = user["count"]
        total -= user["count"]

    counts["other"] = total

    c1 = (170, 57, 57)
    c2 = (170, 108, 57)
    c3 = (136, 45, 96)
    c4 = (45, 136, 45)
    c5 = (34, 102, 102)
    c6 = (46, 65, 114)


    make_pie(counts.values(), "Records by user",[c1,c2,c3,c4,c5,c6],counts.keys())

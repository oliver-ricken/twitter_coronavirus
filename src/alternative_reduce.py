#!/usr/bin/env python3

import matplotlib
import numpy as np
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# command line args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_paths',nargs='+',required=True)
parser.add_argument('--keys',nargs='+',required=True)
parser.add_argument('--percent',action='store_true')
args = parser.parse_args()

# imports
import os
import json
from collections import Counter,defaultdict

for key in args.keys:
    # load input paths
    sorted(args.input_paths)
    yaxis = []
    total_count = defaultdict(lambda: Counter())
    for path in args.input_paths:
        with open(path) as pf:
            val = json.load(pf)
            num_sum = 0
            try:
                for element in val[key]:
                    num_sum += val[key][element]
            except:
                pass
            yaxis.append(num_sum)
    plt.plot(np.arange(366), yaxis, label = key)
plt.xlabel("Date in 2020")
plt.ylabel("Number of Tweets")
plt.title("Tweets with Given Hashtags per Day in 2020")
plt.xticks([0, 60, 121, 182, 244, 305], ["Jan", "Mar", "May", "Jul", "Sept", "Nov"])
plt.legend()
plt.tight_layout()
plt.savefig("lineplot_by_hashtag_v2.png")

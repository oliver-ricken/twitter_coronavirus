#!/usr/bin/env python3

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np

# command line args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_path',required=True)
parser.add_argument('--key',required=True)
parser.add_argument('--percent',action='store_true')
args = parser.parse_args()

# imports
import os
import json
from collections import Counter,defaultdict

# open the input path
with open(args.input_path) as f:
    counts = json.load(f)

# normalize the counts by the total values
if args.percent:
    for k in counts[args.key]:
        counts[args.key][k] /= counts['_all'][k]

counter = 0
key_list = []
val_list = []

items = sorted(counts[args.key].items(), key=lambda item: (item[1],item[0]), reverse=True)

for k,v in items:
    if counter <= 9:
        key_list += [k]
        val_list += [int(v)]
    counter += 1

key_list_flip = list(reversed(key_list))
val_list_flip = list(reversed(val_list))

n = len(key_list)
indices = np.arange(n)
plot1 = plt.bar(indices, val_list_flip)
plt.xticks(indices, key_list_flip)

if "country" in str(args.input_path):
    xaxis = "Country"
else:
    xaxis = "Language"

plt.ylabel('Number of Tweets')
plt.xlabel(xaxis)

if "#코로나바이러스" in str(args.key):
    pass
else:
    plt.title('Top 10 ' + args.key + ' Tweets by ' + xaxis)

# Save the graph as a PNG file
plt.tight_layout()
plt.savefig(f"./{args.input_path}_korean_graph.png")

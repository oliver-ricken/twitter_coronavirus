#!/usr/bin/env python3

# command line args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_path',required=True)
parser.add_argument('--output_folder',default='outputs')
args = parser.parse_args()

# imports
import os
import zipfile
import datetime 
import json
from collections import Counter,defaultdict

# load keywords
hashtags = [
    '#코로나바이러스',  # korean
    '#コロナウイルス',  # japanese
    '#冠状病毒',        # chinese
    '#covid2019',
    '#covid-2019',
    '#covid19',
    '#covid-19',
    '#coronavirus',
    '#corona',
    '#virus',
    '#flu',
    '#sick',
    '#cough',
    '#sneeze',
    '#hospital',
    '#nurse',
    '#doctor',
    ]

# initialize counters
counter_lang = defaultdict(lambda: Counter())
counter_country = defaultdict(lambda: Counter())

# open the zipfile
with zipfile.ZipFile(args.input_path) as archive:

    # loop over every file within the zip file
    for i,filename in enumerate(archive.namelist()):
        print(datetime.datetime.now(),args.input_path,filename)

        # open the inner file
        with archive.open(filename) as f:

            # loop over each line in the inner file
            for line in f:

                # load the tweet as a python dictionary
                tweet = json.loads(line)

                # convert text to lower case
                text = tweet['text'].lower()

                # set lang var
                lang = tweet['lang']
                # check for country code
                if tweet['place']:
                    if tweet['place']['country_code']:
                        country = tweet['place']['country_code']
                    else:
                        country = None
                else:
                    country = None
                # search hashtags
                for hashtag in hashtags:
                    if hashtag in text:
                        counter_lang[hashtag][lang] += 1
                        if country is not None:
                            counter_country[hashtag][country] += 1
                    counter_lang['_all'][lang] += 1
                    if country is not None:
                        counter_country['_all'][country] += 1

# open the outputfile
try:
    os.makedirs(args.output_folder)
except FileExistsError:
    pass
output_path_base = os.path.join(args.output_folder,os.path.basename(args.input_path))

output_path_lang = output_path_base+'.lang'
output_path_country = output_path_base+'.country'

print('saving', output_path_lang)
with open(output_path_lang, 'w') as f_lang:
    f_lang.write(json.dumps(counter_lang))

print('saving', output_path_country)
with open(output_path_country, 'w') as f_country:
    f_country.write(json.dumps(counter_country))

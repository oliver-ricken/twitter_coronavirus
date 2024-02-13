# Tracking the Coronavirus on Twitter in 2020

In this project, I scanned through all geotagged tweets sent in 2020 to monitor for the spread of the coronavirus on social media. This project allowed me to:

- work with large scale datasets (~3.3 terabytes)
- work with multilingual text
- utilize the MapReduce divide-and-conquer paradigm to create parallel code
- better understand global perceptions of the coronavirus in the early stages on the pandemic

## Background

Of the approximately 500 million tweets sent everyday, only 2% are *geotagged*. Geotagged tweets contain location information about where the tweets were sent from.
The dataset I used for this project contains all geotagged tweets sent in the year 2020 -- about 1.1 billion tweets in total.

The tweets for each day in 2020 are stored in zip files with the following name format: `geoTwitterYY-MM-DD.zip`. Inside each of these zip files are 24 text files, one for each hour of the day, that contain a single tweet per line in JSON format.

## Project Motivation

Let's say we wanted to simply count the number of tweets sent on a particular day. We could use the following command:

```
unzip -p '/data/Twitter dataset/geoTwitter20-01-01.zip' | wc -l
```

However, the file is so large that looping over it and counting the number of lines takes a very long time -- about 80 seconds on average for me. So, how long would it take for us to loop over the entire dataset?

```
$ echo "print(1887*80/60/60)" | python3
41.93333333333333
```

Based on this, we can predict that it will take about 42 hours just to loop over the entire dataset! Because looping has a runtime of $O(n)$, an algorithm with $O(n^2)$ runtime would take about 73 days to complete. Therefore, it's very important that any algorithms we perform on this dataset have runtime $O(n)$. 73 days is just way too long to sit around waiting for code to finish!

However, we can't let this runtime issue prevent us from digging into this dataset and searching for insights about the spread of coronavirus in 2020. Usually, datasets that contain key insights are quite large. So, we need better ways of dealing with large scale data... introducing: MapReduce.

## MapReduce

MapReduce is a widely used 3-step procedure for large scale parallel processing. The general flow of the MapReduce procedure is as follows:

1. **Partition**: we partition the data into subsets.
2. **Map**: we apply a mapping to the subsets that performs some determined operation.
3. **Reduce**: we merge the outputs generated by the mappings, allowing us to have a single output file by which we can perform analysis on. 

The following image helps to visualize the MapReduce process:

<img src=mapreduce.png width=100% />

The main benefit of MapReduce is that we can run the computationally expensive mapping tasks in parallel, significantly reducing runtime. 

Now that we've introduced the MapReduce model, let's cover each of the steps in a bit more detail. Note that the partition step was completed in the creation of the dataset, as the tweets are already split into one file per day.

## Method

**Task 1: Map**

The `map.py` file processes the zip files for each day and tracks the usage of the loaded hashtags on both a language and country level. The hashtags we track are contained within the `# load keywords` section of the file, and displayed below:

```
hashtags = [
    '#코로나바이러스',   # Korean for Coronavirus
    '#コロナウイルス',   # Japanese for Coronavirus
    '#冠状病毒',         # Chinese for Coronavirus
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
```

Running `map.py` will output two files, one that ends in `.lang` for the language dictionary, and one that ends in `.country` for the country dictionary. Essentially, each file either contains the number of tweets sent from each country (in the `.country` file), or the number of tweets written in each language (in the `.lang` file). The keys of the dictionary in each file are simply the hashtags that we want to track, and the value of those keys are the number of sent tweets that contain their respective hashtag.

## Programming Tasks

Complete the following tasks:

**Task 0: Create the mapper**

Modify the `map.py` file so that it tracks the usage of the hashtags on both a language and country level.
This will require creating a variable `counter_country` similar to the variable `counter_lang`, 
and modifying this variable in the `#search hashtags` section of the code appropriately.
The output of running `map.py` should be two files now, one that ends in `.lang` for the language dictionary (same as before),
and one that ends in `.country` for the country dictionary.

> **HINT:**
> Most tweets contain a `place` key,
> which contains a dictionary with the `country_code` key.
> This is how you should lookup the country that a tweet was sent from.
> Some tweets, however, do not have a `country_code` key.
> This can happen, for example, if the tweet was sent from international waters or the [international space station](https://web.archive.org/web/20220124224726/https://unistellaroptics.com/10-years-ago-today-the-first-tweet-was-sent-directly-from-space/).
> Your code will have to be generic enough to handle edge cases similar to this without failing.

**Task 1: Run the mapper**

> **HINT:**
> You should thoroughly test your `map.py` file on a single day's worth of tweets and verify that you are getting reasonable results before moving on to this step.

Create a shell script called `run_maps.sh`.
This file will loop over each file in the dataset and run the `map.py` command on that file.
Each call to `map.py` can take up to a day to finish, so you should use the `nohup` command to ensure the program continues to run after you disconnect and the `&` operator to ensure that all `map.py` commands run in parallel.

> **HINT:**
> Use the glob `*` to select only the tweets from 2020 and not all tweets.

**Task 2: Reduce**

> **HINT:**
> You should manually inspect the output of your mapper code to ensure that it is reasonable and that you did not run into any error messages.
> If you have errors above that you don't deal with,
> then everything else below will be incorrect.

After your modified `map.py` has run on all the files,
you should have a large number of files in your `outputs` folder.
Use the `reduce.py` file to combine all of the `.lang` files into a single file,
and all of the `.country` files into a different file.

**Task 3: Visualize**

Recall that you can visualize your output files with the command
```
$ ./src/visualize.py --input_path=PATH --key=HASHTAG
```
Currently, this prints the top keys to stdout.

Modify the `visualize.py` file so that it generates a bar graph of the results and stores the bar graph as a png file.
The horizontal axis of the graph should be the keys of the input file,
and the vertical axis of the graph should be the values of the input file.
The final results should be sorted from low to high, and you only need to include the top 10 keys.

> **HINT:**
> We are not covering how to create images from python code in this class.
> I recommend you use the matplotlib library,
> and you can find some samples to base your code off of [in the documentation here](https://matplotlib.org/3.1.1/tutorials/introductory/sample_plots.html).

Then, run the `visualize.py` file with the `--input_path` equal to both the country and lang files created in the reduce phase, and the `--key` set to `#coronavirus` and `#코로나바이러스`.
This should generate four plots in total.

**Task 4: Alternative Reduce**

Create a new file `alternative_reduce.py`.
This file should take as input on the command line a list of hashtags,
and output a line plot where:
1. There is one line per input hashtag.
1. The x-axis is the day of the year.
1. The y-axis is the number of tweets that use that hashtag during the year.

Your `alternative_reduce.py` file have to follow a similar structure to a combined version of the `reduce.py` and `visualize.py` files.
First, you will scan through all of the data in the `outputs` folder created by the mapping step.
In this scan, you will construct a dataset that contains the information that you need to plot.
Then, after you have extracted this information,
you should call the appropriate matplotlib functions to plot the data.

> **HINT:**
> The specifications for this program and plot are intentionally underspecified
> (similar to how many real-world problems are underspecified).
> Feel free to ask clarifying questions.

**Task 5: Uploading**

Commit all of your code and images output files to your github repo and push the results to github.
You must:
1. Delete the current contents of the `README.md` file
1. Insert into the `README.md` file a brief explanation of your project, including the 4 generated png files.
    This explanation should be suitable for a future employer to look at while they are interviewing you to get a rough idea of what you accomplished.
    (And you should tell them about this in your interviews!)

## Submission

Upload a link to you github repository on sakai.
I will look at your code and visualization to determine your grade.

**Grading:**

The assignment is worth 32 points:

1. 8 points for getting the map/reduce to work
1. 8 points for your repo/readme file
1. 8 points for Task 3 plots
1. 8 points for Task 4 plots

The most common ways to miss points are:
1. having incorrect data plotted (because the map program didn't finish running on all of the inputs)
1. having illegible plots that are not "reasonably" formatted

Notice that we are not using CI to grade this assignment.
There's two reasons:

1. You can get slightly different numbers depending on some of the design choices you make in your code.
    For example, should the term `corona` count tweets that contain `coronavirus` as well as tweets that contain just `corona`?
    These are relatively insignificant decisions.
    I'm more concerned with your ability to write a shell script and use `nohup`, `&`, and other process control tools effectively.

1. The dataset is too large to upload to github actions.
    In general, writing test cases for large data analysis tasks is tricky and rarely done.
    Writing correct code without test cases is hard,
    and so many (most?) analysis of large datasets contain lots of bugs.

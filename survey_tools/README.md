These python routines are for working with the survey data that Randall Munroe compiled in his [2010 colour survey](http://blog.xkcd.com/2010/05/03/color-survey-results/). The raw data is available as a sqlite dump [here](http://xkcd.com/color/colorsurvey.tar.gz) (83.6MiB .tar.gz).

When you untar the data you get two files, mainsurvey_sqldump.txt and satfaces_sqldump.txt. We're only interested in the first of the two. Recreate the sqlite database as follows:

```
$ tar zxvf colorsurvey.tar.gz
$ sqlite3 colorsurvey.db
sqlite> .read mainsurvey_sqldump.txt
```

This takes a few minutes to import on my Macbook. Once done, you can use the sqlite commands `.tables` and `.schema` to interrogate the structure of the database to get an idea of how the data is laid-out:

```
sqlite> .tables
answers  names    users
sqlite> .schema answers
CREATE TABLE answers
                 (id INTEGER PRIMARY KEY, user_id, datestamp, r, g, b, colorname);
CREATE INDEX bval ON answers (b);
CREATE INDEX colorname ON answers (colorname);
CREATE INDEX gval ON answers (g);
CREATE INDEX rval ON answers (r);
CREATE INDEX whichuser ON answers (user_id);
```

I'm only interested in the `answers` table. The `names` table contains some aggregate stats and `users` contains anonymized information about the survey participants, neither of which I need for this.

```
$ python db_colorfill.py
```

For better colour-matching, I decided to convert all the colours into the [CIE-L*a*b*](http://en.wikipedia.org/wiki/Lab_color_space#CIELAB) space, which is purportedly the best space for representing the human perception of colour. In theory, the closer-together two points are in this space, the closer together they appear to a human observer as well. The resulting new table is called `conv_ans`.

I also take the opportunity here to fix some of the issues with the colour names, stripping leading and trailing whitespace, removing double-spaces, quotes, and certain other punctuation.

```
$ python db_averages.py
```

Create a table of average colours in Lab space, along with their variances (the square of the standard deviation). The resulting table is called `averages`.

I take a further opportunity to prune spam out of the database in two ways. First, any colour with only a single result is suspect and I cull it. This removes a few legitimate colour names which is unfortunate, but mainly it removes some of the really silly answers where users decided to start running conversations instead of answering with colour names.

An extra pruning step removes all of the colours where the variance is too big. This is done as follows: from the 50 most popular colours, choose the one with the biggest variance (blue, as it happens). Delete all colours with a bigger variance. This eliminates most of the spam answers such as "I don't know" and certain epithets that are repeated many times (there are over 3800 instances of the N-word in the answers, for example).

```
$ python db_2_json.py > colours.js
```

Finally, take the top 1000 colours and output them to a JavaScript file as an array. RGB values are converted back to integers, Lab and variance are trimmed to 3 decimal places. This produces a JS file approximately 60KiB in size, which gzips-down to approximately 26KiB. Acceptable. I could shrink the file further by removing the RGB values and calculating them on the fly, but I don't think it really matters.

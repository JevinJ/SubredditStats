# SubredditStats
Reddit bot for anonymously monitoring the frequency of topics/words in a single or multiple subreddits using PRAW library. Topics/mentions are filtered with a blacklist as well as length and punctuation, and saved to a CSV file. 

### Prerequisites
* PRAW Libraries
* Python3+
* Program that can read CSV, eg. LibreCalc

### Setup
Install PRAW via pip3.
```
pip3 install praw
```

To upgrade PRAW.
```
pip3 install --upgrade praw
```

Set up the praw.ini file in SubredditStats/app.
1. [Check out the PRAW.ini docs](http://praw.readthedocs.io/en/latest/getting_started/configuration/prawini.html)
2. Create a script app in reddit under the bot account: reddit->preferences->apps->create an app->script->name(your_bot_name)->redirect uri(http://127.0.0.1).
3. Take note of the string under "personal use script", and "secret" string, do NOT share these.
4. The "personal use script" id generated from reddit is the "client_id", in your praw.ini file.
5. "secret" is the "client_secret" as noted in the "Defining Additional Sites" section in the PRAW docs in step 1.
6. Save this as praw.ini in SubredditStats/app.

Create 'word_filter.txt' and 'user_filter.txt' in the program directory. If you do not create these files, a blank file will be created for you after first run.
1. word_filter.txt contains words that you do not want to be included in the final CSV file(conjunctives, certain nouns, short words, etc). Only include words in lowercase, without punctuation.
2. user_filter.txt contains usernames whose comments you don't want to include, eg(AutoModerator). Only include names in lowercase.

### Running
In SubredditStats/app run main.py
```
python main.py [bot site/name] [subreddits to target] --interval[a number, the time in days to generate a CSV](optional, default is 1)
```

##### Example: 
```
python main.py bot1 pcgaming+gaming --interval 3
```
###### Will collect comments/submissions from pcgaming & gaming. After 3 days, a CSV will be ready and you can read the results.

##### Another Example:
```
python main.py bot1 learnpython
```
###### Will collect from learnpython. A CSV will be ready after the default 1 day.

## Built With
* [PRAW](http://praw.readthedocs.io/en/latest/index.html)

## Authors
* **Jevin Jones** - *Creator* - [JevinJ](https://github.com/JevinJ)

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

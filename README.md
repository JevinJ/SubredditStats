# Subreddit-Stats

Reddit bot for anonymously monitoring the frequency of topics in specific subreddits via CSV file using praw library. Topics/mentions are filtered with a blacklist as well as length and punctuation. 

### Prerequisites

Praw Libraries
Praw.ini
Python 3+
Program That Can Read CSV, eg. LibreCalc

### Installing

Install Praw Via Pip3
```
pip3 install praw
```

To Upgrade Praw
```
pip3 install --upgrade praw
```

Set Up Praw INI File
```
http://praw.readthedocs.io/en/latest/getting_started/configuration/prawini.html

Create a script app in reddit under the bot account:
 Reddit->Preferences->Apps->Create an app->Script->Name(Your Name)->Redirect uri(http://127.0.0.1)
 Take note of the string under "personal use script", and "secret" string, do NOT share these.
"personal use script" id goes under "client_id" and "secret" under "client_secret" as noted in the "Defining Additional Sites" section of the above link

Save this as .ini in the same directory of the program
```

Create 'filter.txt' and 'userfilter.txt' in the program directory.
```
filter.txt contains words that you do not want to be included in the final CSV file(conjunctives, certain nouns, short words, etc). Only include words in lowercase.
userfilter.txt contains usernames whose comments you don't want to include, eg(automoderator). Only include names in lowercase.
If you do not create these files, a blank file will be created for you.
```

Update Lines In SrStats.py As Commented To Suit Your Needs

Run SrStats.py
```
CMD: python SrStats.py
Terminal: python3 SrStats.py
```
Generate CSV when ready
```
CMD: python GenerateCSV.py
Terminal: python3 GenerateCSV.py
```

###NOTE
```
Data loss is unlikely to occur but I recommend daily backups of the generated commentdata.pickle file.
```

## Built With

* [Praw](http://praw.readthedocs.io/en/latest/index.html)


## Authors

* **Jevin Jones** - *Creator* - [JevinJ](https://github.com/JevinJ)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

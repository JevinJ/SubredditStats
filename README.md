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

Create "blacklist.txt" and "commentspolled.txt" in program directory
```
blacklist.txt contains words that you do not want to be included in the final CSV file(conjunctives, certain nouns, short words, etc)
commentspolled.txt contains comment ids that have been read so we do not include the text more than once
```

Update SrStats.py to suit your needs

###NOTE
```
I highly reccomend timing how long the program takes to complete. If the program is interrupted manually or via Internet loss or 
 Reddit maintainance, there is a small chance of data loss. Recccomend daily backups of CSV file.
```

## Built With

* [Praw](http://praw.readthedocs.io/en/latest/index.html)


## Authors

* **Jevin Jones** - *Creator* - [JevinJ](https://github.com/JevinJ)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

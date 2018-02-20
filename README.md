# Subreddit-Stats
Reddit bot for anonymously monitoring the frequency of topics in a single or multiple subreddits using PRAW library. Topics/mentions are filtered with a blacklist as well as length and punctuation, and saved to a CSV file. 

### Prerequisites
PRAW Libraries
PRAW.ini
Python3+
Program that can read CSV, eg. LibreCalc

### Setup
Install PRAW via pip3.
```
pip3 install praw
```

To upgrade PRAW.
```
pip3 install --upgrade praw
```

Set up praw.ini file.
1. http://praw.readthedocs.io/en/latest/getting_started/configuration/prawini.html
2. Create a script app in reddit under the bot account: Reddit->Preferences->Apps->Create an app->Script->Name(YourName)->Redirect uri(http://127.0.0.1).
3. Take note of the string under "personal use script", and "secret" string, do NOT share these.
4. "personal use script" id goes under "client_id".
5. "secret" under "client_secret" as noted in the "Defining Additional Sites" section in the link in step 1.
6. Save this as .ini in the same directory of the program.

Create 'filter.txt' and 'userfilter.txt' in the program directory. If you do not create these files, a blank file will be created for you.
1. filter.txt contains words that you do not want to be included in the final CSV file(conjunctives, certain nouns, short words, etc). Only include words in lowercase.
2. userfilter.txt contains usernames whose comments you don't want to include, eg(automoderator). Only include names in lowercase.

Update commented lines in SrStats.py to suit your needs.

### Running
Run SrStats.py
```
CMD: python SrStats.py
Terminal: python3 SrStats.py
```
Generate CSV when ready
```
Close SrStats if it is running.
CMD: python GenerateCSV.py
Terminal: python3 GenerateCSV.py
```

## Built With
* [PRAW](http://praw.readthedocs.io/en/latest/index.html)


## Authors
* **Jevin Jones** - *Creator* - [JevinJ](https://github.com/JevinJ)

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

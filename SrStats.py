from collections import defaultdict
import os.path
import pickle
import praw
import string


#Text filters: Punctuation, undesired words from filter.txt(blacklist), non alpha words,
# and <= 1 char and >= char words
def filter_comment(text):
    text = text.split()
    text = [word.lower() for word in text if word.lower() not in blacklist and
            word.isalpha() and (len(word) > 1 and len(word) < 15)]
    text = [''.join(ch for ch in word if ch not in string.punctuation) for word in text]
    return text

def save_data(comment_data):
    with open('commentdata.pickle', 'wb') as f:
        pickle.dump(comment_data, f, protocol=pickle.HIGHEST_PROTOCOL)

def load_data():
    if not os.path.isfile('commentdata.pickle'):
        return defaultdict(int)
    with open('commentdata.pickle', 'rb') as f:
        return pickle.load(f)

def save_comments_polled(c_polled):
    with open('commentspolled.pickle', 'wb') as f:
        pickle.dump(c_polled, f, protocol=pickle.HIGHEST_PROTOCOL)

def load_comments_polled():
    if not os.path.isfile('commentspolled.pickle'):
        return set()
    with open('commentspolled.pickle', 'rb') as f:
        return pickle.load(f)

if not os.path.isfile('filter.txt'):
    open('filter.txt', 'w')
with open('filter.txt', 'r', encoding='utf-8') as f:
    blacklist = f.read()
    blacklist = blacklist.split('\n')
    blacklist = list(filter(None, blacklist))

if not os.path.isfile('userfilter.txt'):
    open('userfilter.txt', 'w')
with open('userfilter.txt', 'r', encoding='utf-8') as f:
    user_filter = f.read()
    user_filter = user_filter.split('\n')
    user_filter = list(filter(None, user_filter))

# Bot title from praw.ini goes here, eg('bot1')
reddit = praw.Reddit('')

# Put subreddit title here as it apprears in url, multiple subs can be read
# by appending '+' between titles, eg('sub1+sub2')								    
subreddit = reddit.subreddit('')

comment_data = load_data()
comments_polled = load_comments_polled()
for thread in subreddit.hot(limit=50):
    print('Working in submission: ' + str(thread.title))
    # Can limit how many deep you go with 'More Comments' sections or limit how
    # many comments you'll get from each section, default is sufficient. 2 seconds per request.
    thread.comments.replace_more(limit=0, threshold=4)
    comments = thread.comments.list()
    for comment in comments:
        if (str(comment.author).lower() in user_filter) or (str(comment.id) in comments_polled):
            continue
        text = filter_comment(comment.body)
        comments_polled.add(str(comment.id))
        for word in text:
            if comment_data.get(word, False):
                comment_data[word] += 1
            else:
                comment_data[word] = 1
    save_comments_polled(comments_polled)
    save_data(comment_data)

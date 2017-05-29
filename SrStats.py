import praw
import string

reddit = praw.Reddit("bot3")
subreddit = reddit.subreddit("politics")													#Put subreddit title here as it apprears in url, multiple subs can be read
																					# by appending '+' between titles, eg "sub1+sub2"
with open('blacklist.txt', 'r') as blacklist_raw:
	blacklist = blacklist_raw.read()
	blacklist = blacklist.split('\n')
	blacklist = list(filter(None, blacklist))
	
with open('commentspolled.txt', 'r') as polled_raw:
	polled = polled_raw.read()
	polled = polled.split('\n')
	polled = list(filter(None, polled))
	
with open('topics.csv', 'r') as topics_raw:
	topics = topics_raw.read()
	topics = topics.split('\n')
	topics = list(filter(None, topics))

def filterBody(text):
	text = text.split(' ')															#Text filters: Punctuation, undesired words from filter.txt(blacklist),		
	text = [word.lower() for word in text]											# non alpha words, and <= 1 char and >= char words
	text = [''.join(ch for ch in word if ch not in string.punctuation) for word in text]																							 																		
	text = [word for word in text if word not in blacklist and \
	+ word.isalpha() and len(word) > 1 and len(word) < 15]
	return(text)
	
for submission in subreddit.hot(limit=25):
	print("In submission: " + str(submission.title))
	submission.comments.replace_more(limit=0, threshold= 4)							#Can limit how many "More Comments" you request or threshold based on how 
	comments = submission.comments.list()											# many comments you'll get. 2 seconds per request.
	for comment in comments:
		if str(comment.author) != "AutoModerator" and str(comment.id) not in polled:			
			text = filterBody(comment.body)
			polled.append(str(comment.id))
			with open("commentspolled.txt", "w") as f:							
				for comment_id in polled:
					f.write(comment_id + "\n")
				for word in text:
					for num, line in enumerate(topics):				
						if word in line:
							spl = line.split(',')
							num_times = int(spl[1]) + 1
							topics[num] = word + ',' + str(num_times)
							with open('topics.csv', 'w', encoding="utf-8") as f:
								for x in topics:
									f.write(x + '\n')
							break
					if not any(word in line for line in topics):					#Adding words to file if not in
						topics.append(word + ',1')
						with open('topics.csv', 'w', encoding="utf-8") as f:
							for x in topics:
								f.write(x + '\n')				
import praw
import string


#Bot title from praw.ini goes here, eg. "Bot1"
reddit = praw.Reddit('')

#Put subreddit title here as it apprears in url, multiple subs can be read
# by appending '+' between titles, eg "sub1+sub2"								    
subreddit = reddit.subreddit('')
							
with open('filter.txt', 'r', encoding='utf-8') as f:
	blacklist = f.read()
	blacklist = blacklist.split('\n')
	blacklist = list(filter(None, blacklist))
	
with open('commentspolled.txt', 'r', encoding='utf-8') as f:
	c_polled = f.read()
	c_polled = c_polled.split('\n')
	c_polled = list(filter(None, c_polled))
	
with open('topics.csv', 'r', encoding='utf-8') as f:
	topics = f.read()
	topics = topics.split('\n')
	topics = list(filter(None, topics))
	
#Text filters: Punctuation, undesired words from filter.txt(blacklist), non alpha words,
# and <= 1 char and >= char words	
def filterBody(text):
	text = text.split(' ')										        
	text = [word.lower() for word in text]								
	text = [''.join(ch for ch in word if ch not in string.punctuation) for word in text]																							 																		
	text = [word for word in text if word not in blacklist and \
	+ word.isalpha() and len(word) > 1 and len(word) < 15]
	return(text)
	
for submission in subreddit.hot(limit=25):
	print("In submission: " + str(submission.title))
	#Can limit how many "More Comments" you request or threshold based on how 
	# many comments you'll get. 2 seconds per request.
	submission.comments.replace_more(limit=0, threshold= 4)						
	comments = submission.comments.list()								        
	for comment in comments:
		if str(comment.author) != "AutoModerator" and str(comment.id) not in c_polled:			
			text = filterBody(comment.body)
			c_polled.append(str(comment.id))
			with open("commentspolled.txt", "w") as f:							
				for comment_id in c_polled:
					f.write(comment_id + "\n")
				for word in text:
					for num, line in enumerate(topics):				
						if word in line:
							spl = line.split(',')
							num_times = int(spl[1]) + 1
							topics[num] = word + ',' + str(num_times)
							with open('topics.csv', 'w', encoding='utf-8') as f:
								for x in topics:
									f.write(x + '\n')
							break
					#Adding words to file if not in
					if not any(word in line for line in topics):			      
						topics.append(word + ',1')
						with open('topics.csv', 'w', encoding="utf-8") as f:
							for x in topics:
								f.write(x + '\n')				

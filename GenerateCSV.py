from collections import defaultdict
import os.path
import pickle


def load_data():
    if not os.path.isfile('commentdata.pickle'):
        return defaultdict(int)
    with open('commentdata.pickle', 'rb') as f:
        return pickle.load(f)
		

comment_data = load_data()
if not os.path.isfile('topicsCSV.csv'):
	open('topicsCSV.csv', 'w')
with open('topicsCSV.csv', 'w') as f:
	for word in comment_data:
		f.write(word + ',' + str(comment_data[word]) + '\n')


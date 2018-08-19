from string import punctuation
import praw
from Main import io


class SubredditStats:
    def __init__(self):
        self.reddit = praw.Reddit('bot1')
        self.target = self.reddit.subreddit('politics')
        self.comment_data = io.load_pickle('commentdata.pickle')
        self.user_filter = io.load_file_as_set('user_filter.txt')
        self.word_filter = io.load_file_as_set('word_filter.txt')
        self.main()

    def parse_text(self, text, min_length=1, max_length=16):
        '''
        Text filtering, filters punctuation, undesired words, and very short/long words, etc.
        :return: A list of words that have been filtered
        '''
        result = []
        punct_table = str.maketrans(dict.fromkeys(punctuation))
        for word in text.lower().split():
            if (len(word) > min_length and len(word) < max_length):
                if word.isalpha() and word not in self.word_filter:
                    result.append(''.join(word.translate(punct_table)))
        return result

    def main(self):
        for thread in self.target.hot(limit=500):
            print(f'Working in submission: {str(thread.title)}')
            thread.comments.replace_more(limit=0, threshold=4)
            comments = thread.comments.list()
            for comment in comments:
                if str(comment.author).lower() in self.user_filter:
                    continue
                text = self.parse_text(comment.body)
                for word in text:
                    self.comment_data[word] += 1
            io.save_pickle('commentdata.pickle', self.comment_data)

if __name__ == '__main__':
    SubredditStats()




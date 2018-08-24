from collections import defaultdict
from datetime import datetime
import praw
from unidecode import unidecode
import fileio as fio
import constants


class SubredditStats:
    def __init__(self, bot_name, target, csv_period=1):
        '''
        :param bot_name: The name/site of the bot as defined in praw.ini
        :param target: Target subreddit(s), eg: 'pcgaming' or 'pcgaming+gaming'
        :param csv_period: Time period in days to generate a full CSV file of results.
        '''
        self.reddit = praw.Reddit(bot_name)
        self.target = self.reddit.subreddit(target)
        self.csv_period = csv_period
        self.word_frequency = defaultdict(int)
        self.user_filter = set(filter(None, fio.load_file('', 'user_filter.txt')))
        self.word_filter = set(filter(None, fio.load_file('', 'word_filter.txt')))
        self.last_csv_generation = datetime.now()
        self.last_dataset_save = datetime.now()
        self.main()

    def filter_text(self, text, min_length=1, max_length=16):
        '''
        Text filtering, filters punctuation, converts non-ascii, undesired, very short/long words, or
        anything in word_filter.txt
        :param text: The full text body of a comment or submission title.
        :param min_length: The minimum length of a single word in text, anything less is filtered out.
        :param max_length: The maximum length of a single word in text, anything more is filtered out.
        :return: A list of words that have been filtered.
        '''
        result = []
        for word in unidecode(text.lower()).split(' '):
            if len(word) > min_length and len(word) < max_length:
                if word.isalpha() and word not in self.word_filter:
                    result.append(''.join(word.translate(constants.PUNCTUATION_TRANS)))
        return result

    def update_dataset(self, text):
        '''
        Increment the values in the word frequency dict for each word in text.
        :param text: A list of words that have been filtered/parsed and are ready to be included into word_frequency.
        '''
        text = self.filter_text(text)
        for word in text:
            self.word_frequency[word] += 1

    def main(self):
        while True:
            for comment in self.target.stream.comments(pause_after=-1):
                if comment is None:
                    break
                if str(comment.author).lower() not in self.user_filter:
                    self.update_dataset(comment.body)

            for submission in self.target.stream.submissions(pause_after=-1):
                if submission is None:
                    break
                if str(submission.author).lower() not in self.user_filter:
                    self.update_dataset(submission.title)

            #If an hour has passed since start-up/last save, save the word frequencies into a file and wipe it.
            if (datetime.now() - self.last_dataset_save).seconds >= 3600:
                pickle_filename = f'{self.last_dataset_save.strftime(constants.TIMESTAMP_FORMAT)}.pickle'
                fio.save_pickle(self.word_frequency, 'output', pickle_filename)
                self.word_frequency = defaultdict(int)
                self.last_dataset_save = datetime.now()

            #If self.csv_period days have passed since start-up/last save, generate a csv and wipe saved pickle files.
            if (datetime.now() - self.last_csv_generation).seconds // 86400 >= self.csv_period:
                csv_filename = f'{self.last_csv_generation.strftime(constants.TIMESTAMP_FORMAT)}.csv'
                fio.generate_csv('output', 'output/completedcsv', csv_filename)
                self.last_csv_generation = datetime.now()


if __name__ == '__main__':
    SubredditStats('bot1', 'all')




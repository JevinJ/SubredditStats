import argparse
from collections import defaultdict
from datetime import datetime
import praw
from unidecode import unidecode
import fileio as fio
import constants


class SubredditStats:
    def __init__(self, **kwargs):
        '''
        :param bot_name: The name/site of the bot as defined in praw.ini
        :param target: Target subreddit(s), eg: 'pcgaming' or 'pcgaming+gaming'
        :param csv_period: Time period in days to generate a full CSV file of results.
        '''
        print(f'Running with commands --name({kwargs["bot_name"]}), --target({kwargs["target"]}),'
              f' and generating a new csv every {kwargs["csv_period"]} day(s)')
        self.reddit = praw.Reddit(kwargs['bot_name'])
        self.target = self.reddit.subreddit(kwargs['target'])
        self.csv_period = kwargs['csv_period']
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

            time_now = datetime.now()
            #If an hour has passed since start-up/last save, save the word frequencies into a file and wipe it.
            if (time_now - self.last_dataset_save).seconds // 3600 >= 1:
                pickle_filename = f'{self.last_dataset_save.strftime(constants.FILE_TIMESTAMP_FORMAT)}.pickle'
                fio.save_pickle(self.word_frequency, 'output', pickle_filename)
                self.word_frequency = defaultdict(int)
                self.last_dataset_save = datetime.now()
                print(f'{time_now.strftime(constants.CONSOLE_TIMESTAMP_FORMAT)}' + \
                      f' Saved {pickle_filename} to /output/')

            #If self.csv_period days have passed since start-up/last save, generate a csv and wipe saved pickle files.
            if (time_now - self.last_csv_generation).seconds // 86400 >= self.csv_period:
                csv_filename = f'{self.last_csv_generation.strftime(constants.FILE_TIMESTAMP_FORMAT)}.csv'
                fio.generate_csv('output', 'output/completedcsv', csv_filename)
                self.last_csv_generation = datetime.now()
                print(f'{time_now.strftime(constants.CONSOLE_TIMESTAMP_FORMAT)}' + \
                      f' Generated {csv_filename} to /output/completedcsv')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', type=str, metavar='BOT_NAME', dest='bot_name', required=True,
                        help='The name/site of the bot as defined in praw.ini')
    parser.add_argument('--target', type=str, metavar='SUB_NAME', required=True,
                        help='Subreddit(s) to target, "+" to use multiple subs, eg: pcgaming or pcgaming+gaming')
    parser.add_argument('--interval', type=lambda i: abs(int(i)), metavar='CSV_PERIOD', dest='csv_period', default=1,
                        help='Time interval in days to compile a csv containing word frequencies for that period')
    SubredditStats(**vars(parser.parse_args()))

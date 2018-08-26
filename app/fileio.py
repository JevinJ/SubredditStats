from collections import Counter
from datetime import datetime
import gzip
import os
from pathlib import Path
import pickle
import constants


def create_directory_path(relative_folderpath):
    '''Create a folder for every directory in relative_folderpath
    :param relative_folderpath: str, a new path relative to main
    '''
    return Path.cwd().joinpath(relative_folderpath).mkdir(parents=True, exist_ok=True)

def get_abs_path(relative_path, filename=''):
    '''Returns an absolute pathlib Path from relative_path and filename'''
    return Path.cwd().joinpath(relative_path, filename).resolve()

def save_pickle(pickle_data, to_relative_path, filename):
    abs_path = get_abs_path(to_relative_path, filename)
    with gzip.open(abs_path, 'wb') as f:
        pickle.dump(pickle_data, f, protocol=pickle.HIGHEST_PROTOCOL)
    print(f'{datetime.now().strftime(constants.CONSOLE_TIMESTAMP_FORMAT)}' + \
          f' Saved {filename} to {to_relative_path}')

def load_pickle(from_relative_path, filename):
    abs_path = get_abs_path(from_relative_path, filename)
    with gzip.open(abs_path, 'rb') as f:
        return pickle.load(f)

def load_file(from_relative_path, filename):
    '''
    :return: A list of lines of the filename located at the absolute path of from_relative_path.
    '''
    abs_path = get_abs_path(from_relative_path, filename)
    while True:
        try:
            with open(abs_path, 'r', encoding='utf-8') as f:
                return f.read().split('\n')
        except FileNotFoundError:
            with open(abs_path, 'w'):
                pass

def generate_csv(from_relative_path, to_relative_path, filename):
    '''
    Generate a CSV file from datasets in from_relative_path, and outputs it into to_relative_path.
    :param from_relative_path: Path containing .pickle datasets, relative to main.py
    :param to_relative_path: Path to output CSV file to, relative to main.py.
    :param filename: Name of CSV file to output, including .csv suffix.
    '''
    abs_from = get_abs_path(from_relative_path)
    abs_to = get_abs_path(to_relative_path, filename)
    word_frequencies = Counter()
    for file in abs_from.glob('*.pickle'):
        word_frequencies.update(load_pickle(from_relative_path, file))
        os.remove(file)
    with open(abs_to, 'w', encoding='utf-8') as f:
        for word in word_frequencies:
            f.write(f'{word},{word_frequencies[word]}\n')
    print(f'{datetime.now().strftime(constants.CONSOLE_TIMESTAMP_FORMAT)}' + \
          f' Generated {filename} to {to_relative_path}')

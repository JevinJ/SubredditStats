from collections import Counter
import gzip
import os
import os.path as path
import pickle


def save_pickle(pickle_data, to_relative_path, filename):
    abs_path = path.abspath(path.join(to_relative_path, filename))
    with gzip.open(abs_path, 'wb') as f:
        pickle.dump(pickle_data, f, protocol=pickle.HIGHEST_PROTOCOL)

def load_pickle(from_relative_path, filename):
    abs_path = path.abspath(path.join(from_relative_path, filename))
    with gzip.open(abs_path, 'rb') as f:
        return pickle.load(f)

def load_file(from_relative_path, filename):
    '''
    :return: A list of lines of the filename located at the absolute path of from_relative_path.
    '''
    abs_path = path.abspath(path.join(from_relative_path, filename))
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
    abs_from = path.abspath(from_relative_path)
    abs_to = path.abspath(path.join(to_relative_path, filename))
    word_frequencies = Counter()
    pickle_files = [f for f in os.listdir(abs_from) if f.endswith('.pickle')]
    for name in pickle_files:
        file_dict = load_pickle(from_relative_path, name)
        word_frequencies.update(file_dict)
        os.remove(path.join(abs_from, name))
    with open(abs_to, 'w', encoding='utf-8') as f:
        for word in word_frequencies:
            f.write(f'{word},{word_frequencies[word]}\n')

from collections import defaultdict
import pickle


def save_pickle(filename, pickle_data):
    with open(filename, 'wb') as f:
        pickle.dump(pickle_data, f, protocol=pickle.HIGHEST_PROTOCOL)

def load_pickle(filename):
    try:
        with open(filename, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('')
        return defaultdict(int)

def load_file_as_set(filename):
    while True:
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                file = f.read().split('\n')
                return set(filter(None, file))
        except FileNotFoundError:
            with open(filename, 'w'):
                pass
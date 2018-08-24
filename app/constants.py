from string import punctuation


PUNCTUATION_TRANS = str.maketrans(dict.fromkeys(punctuation))
TIMESTAMP_FORMAT = '%Y%b%d_%H.%M.%S'
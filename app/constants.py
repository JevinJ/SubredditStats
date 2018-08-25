from string import punctuation


PUNCTUATION_TRANS = str.maketrans(dict.fromkeys(punctuation))
FILE_TIMESTAMP_FORMAT = '%Y%b%d_%H.%M.%S'
CONSOLE_TIMESTAMP_FORMAT = '%I:%M %p:'
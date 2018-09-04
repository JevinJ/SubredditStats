from string import punctuation


PUNCTUATION_TRANS = str.maketrans(dict.fromkeys(punctuation))
FILE_TIMESTAMP_FORMAT = '%Y%b%d-%H_%M_%S'
CONSOLE_TIMESTAMP_FORMAT = '%I:%M %p:'

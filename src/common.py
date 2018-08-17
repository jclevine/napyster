from pathlib import Path
import string
import re


CLEAR_PUNCTUATION_TABLE = str.maketrans('', '', string.punctuation)
STOP_WORDS = {'remastered'}


def mockable_input(text):  # pragma: no cover
    return input(text)


def get_line_from_filepath(filepath):
    if Path(filepath).is_file():
        with open(filepath) as f:
            return f.readline().rstrip('\n')
    else:
        return None


def write_line_to_filepath(filepath, line):  # pragma: no cover
    with open(filepath, 'w') as f:
        f.write(line)


def get_lines_as_list(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read().splitlines()


def cleanse_music_text(s):
    words = str(s).strip().lower()
    words.replace('’', '\'')
    words = list(re.split(r'\s', words))
    words = [word for word in words if word not in STOP_WORDS]
    words = words[1:] if words[0] == 'the' else words
    return ' '.join(words)

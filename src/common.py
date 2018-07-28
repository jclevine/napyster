from pathlib import Path


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

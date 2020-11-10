import re
from functools import partial
from pathlib import Path


def is_match_pattern(t: str, *, pattern: str) -> bool:
    p = re.compile(pattern)
    if p.match(t):
        return True
    else:
        return False


def is_remove(t: str) -> bool:
    checkers = (
        lambda x: x == '',
        partial(is_match_pattern, pattern='^\d+$'), # is int
        partial(is_match_pattern, pattern='^[\d,:]+ --> [\d,:]+$'), # is srt timestamp
    )

    return any([checker(t) for checker in checkers])


def is_paragraph_splitter(t: str) -> bool:
    return is_match_pattern(t, pattern='^[+]+[\s\w]+[+]+$')\
        or is_match_pattern(t, pattern='^[*]+[\s\w]+[+]+$')\
        or is_match_pattern(t, pattern='^[*]+[\s\w]+[*]+$')


def main(inf, outf):
    ret = []

    with Path(inf).open('r') as f_:
        for line in f_:
            ln = line.strip()

            if is_remove(ln):
                ...
            elif is_paragraph_splitter(ln):
                ret.append(f'\n\n{ln}\n\n')
            else:
                if ln.endswith('.') or ln.endswith(','):
                    ret.append(f'{ln} ')
                else:
                    ret.append(f'{ln}. ')


    with Path(outf).open('w') as f_:
        f_.write(''.join(ret))


if __name__ == '__main__':
    main('t.txt', 'o.txt')

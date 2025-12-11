from utils import *

def load_high_score():
    try:
        if os.path.exists(SCORE_FILE):
            with open(SCORE_FILE, 'r') as f:
                return int(f.read().strip())
    except (ValueError, IOError):
        pass
    return 0


def save_high_score(score):
    try:
        with open(SCORE_FILE, 'w') as f:
            f.write(str(score))
    except IOError:
        pass
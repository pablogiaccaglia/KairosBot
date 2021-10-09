from pathlib import Path

from validator_collection import checkers

from GUI import gui


def relative_to_assets(path: str) -> Path:
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path("./assets")
    return ASSETS_PATH / Path(path)


def delete_text_on_callback(event):  # note that you must include the event as an arg, even if you don't use it.
    event.widget.delete(0, "end")
    return None


def validateUserInput(userId, password):
    return validatePassword(password) and validateID(userId)


def validateID(userId):
    try:
        return \
            not checkers.is_none(userId) \
            and checkers.is_string(userId) \
            and checkers.has_length(userId, minimum=7, maximum=7) \
            and checkers.is_integer(int(userId), minimum=5000000, maximum=8000000)
    except:
        return False


def validatePassword(password):
    try:
        return \
            not checkers.is_none(password) \
            and checkers.is_string(password) \
            and checkers.has_length(password, minimum=1, maximum=200)
    except:
        return False

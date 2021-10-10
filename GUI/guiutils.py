from pathlib import Path
from tkinter import Button

from validator_collection import checkers

## RELATIVE_PATHS
bookButtonRelPath = "button_book.png"
loginButtonRelPath = "button_login.png"
changeDateButtonRelPath = "button_change_date.png"
closeAppButtonRelPath = "button_close.png"
retryButtonRelPath = "button_retry.png"
loginBackgroundRelPath = "login_bg.png"
passwordEntryRelPath = "password_entry.png"
usernameEntryRelPath = "username_entry.png"


def relativeToAssets(path: str) -> Path:
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path("./assets")
    return ASSETS_PATH / Path(path)


def deleteTextOnCallback(event):  # note that you must include the event as an arg, even if you don't use it.
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


def addButtonToWindow(xPos, yPos, width, height, callback, buttonImage, cursor="hand"):
    button = Button(
        image=buttonImage,
        borderwidth=0,
        highlightthickness=0,
        command=callback,
        relief="flat",
        cursor=cursor
    )

    button.place(
        x=xPos,
        y=yPos,
        width=width,
        height=height
    )

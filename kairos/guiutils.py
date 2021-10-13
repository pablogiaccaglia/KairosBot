from enum import Enum
from tkinter import Button
from validator_collection import checkers


class View(Enum):
    LOGIN_VIEW = "loginView"
    CALENDAR_VIEW = "calendarView"
    BOOKING_VIEW = "bookingView"
    BOOKING_FAILED_VIEW = "bookingFailedView"
    BOOKING_OK_VIEW = "bookingOkView"


## RELATIVE_PATHS
bookButtonRelPath = "button_book.png"
loginButtonRelPath = "button_login.png"
changeDateButtonRelPath = "button_change_date.png"
closeAppButtonRelPath = "button_close.png"
retryButtonRelPath = "button_retry.png"
loginBackgroundRelPath = "login_bg.png"
passwordEntryRelPath = "password_entry.png"
usernameEntryRelPath = "username_entry.png"

## SIZE CONSTANTS
loginWindowWidth = "464"
loginWindowHeight = "853"
wideWindowWidth = "864"
wideWindowHeight = "628"
regularWindowWidth = "474"
regularWindowHeight = "628"


def getWindowSizeAsString(width, height) -> str:
    return str(width) + "x" + str(height)


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

    return button

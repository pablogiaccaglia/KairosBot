import threading
from tkinter import Tk, Canvas, Entry, PhotoImage, StringVar, END, ttk, Label, CENTER, Widget
from abc import ABC, abstractmethod
from tkcalendar import Calendar
from kairos import guiutils
from kairos.bot.KairosBot import KairosBot
from kairos.utils import relativeToAbsPath
from kairos.guiutils import View
from PIL import Image, ImageTk
from functools import partial
from datetime import date, timedelta


class GUI:

    def __init__(self):
        self.window = Tk()
        self.window.resizable(False, False)
        self.date = None
        self.canvas = None
        self.isBookingOk = False
        self.kairosBot = None
        self.views = {
            View.LOGIN_VIEW: LoginView(self),
            View.CALENDAR_VIEW: CalendarView(self),
            View.BOOKING_VIEW: BookingView(self),
            View.BOOKING_FAILED_VIEW: BookingFailedView(self),
            View.BOOKING_OK_VIEW: BookingOkView(self)
        }
        self.userId = None
        self.password = None
        self.currentView = None

    def runView(self, view: View):
        self.currentView.destroyWidgets()
        self.__buildCommonGUIStructure()
        self.currentView = self.views[view]
        self.currentView.run()

    def start(self):
        ico = Image.open(relativeToAbsPath('deadline.png'))
        photo = ImageTk.PhotoImage(ico)
        self.window.wm_iconphoto(False, photo)

        self.window.title("KairosBot")
        self.window.configure(bg="#FFFFFF")
        self.canvas = Canvas(
            self.window,
            bg="#FFFFFF",
            height=853,
            width=464,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )

        self.canvas.place(x=0, y=0)
        self.currentView = self.views[View.LOGIN_VIEW]
        self.runView(View.LOGIN_VIEW)

    def __buildCommonGUIStructure(self):
        self.window.geometry(guiutils.getWindowSizeAsString(guiutils.regularWindowWidth, guiutils.regularWindowHeight))
        self.window.configure(bg="#FFFFFF")

        self.canvas.create_text(
            32.0,
            152.0,
            anchor="nw",
            text="Prenotazione lezioni dell???intera giornata",
            fill="#000000",
            font=("Roboto", 13 * -1)
        )

        self.canvas.place(x=0, y=0)

        self.canvas.create_rectangle(
            0.0,
            0.0,
            864.0,
            628.0,
            fill="#FFFFFF",
            outline="")

        self.canvas.create_text(
            32.0,
            32.0,
            anchor="nw",
            text="KairosBot",
            fill="#000000",
            font=("Montserrat Bold", 32 * -1)
        )

        self.canvas.create_rectangle(
            0.0,
            132.0,
            864.0,
            192.0,
            fill="#FAFAFA",
            outline="")


class AbstractView(ABC):

    def __init__(self, name: str, gui: 'GUI'):
        self.name = name
        self.gui = gui
        self.canvasItems = []
        self.texts = []
        self.buttons = []
        self.labelWidgets = []
        self.widgets = [self.texts, self.buttons, self.labelWidgets]

    def addWidget(self, widget: Widget):
        self.widgets.append(widget)

    def addCanvasElement(self, elem):
        self.canvasItems.append(elem)

    def addButtonElement(self, elem: Widget):
        self.buttons.append(elem)

    def addLabelWidget(self, elem: Widget):
        self.labelWidgets.append(elem)

    def destroyWidgets(self):
        for widgetsList in self.widgets:
            for widget in widgetsList:
                widget.destroy()

    def destroyCanvasItems(self):
        for elem in self.canvasItems:
            self.gui.canvas.delete(elem)

    @abstractmethod
    def run(self):
        pass


class LoginView(AbstractView):

    def __init__(self, gui: 'GUI'):
        super().__init__("loginView", gui)
        self.inputEntries = []
        self.widgets.append(self.inputEntries)
        self.passwordEntry = None
        self.idEntry = None

    def addInputEntry(self, widget: Widget):
        self.inputEntries.append(widget)

    def __setDefaultInput(self):
        self.idEntry.delete(0, END)
        self.passwordEntry.delete(0, END)
        self.idEntry.insert(END, 'Student ID')
        self.passwordEntry.insert(END, 'password')

    def setUserData(self, userId, password):
        self.gui.userId = userId
        self.gui.password = password

    def __performInputAction(self, userIdSVar, passwordSVar):
        userId = userIdSVar.get()
        password = passwordSVar.get()
        if guiutils.validateUserInput(userId, password):
            self.setUserData(userId, password)
            self.gui.runView(View.CALENDAR_VIEW)
        else:
            self.__setDefaultInput()
            self.gui.window.update()

    def run(self):
        self.gui.window.geometry(guiutils.getWindowSizeAsString(guiutils.loginWindowWidth, guiutils.loginWindowHeight))
        image_image_1 = PhotoImage(
            file=relativeToAbsPath(guiutils.loginBackgroundRelPath))

        smaller_image = image_image_1.subsample(5, 5)

        imgElem1 = self.gui.canvas.create_image(
            220.0,
            430.0,
            image=smaller_image
        )

        self.addCanvasElement(imgElem1)

        textElem1 = self.gui.canvas.create_text(
            220.5,
            411.0,
            anchor="nw",
            text="Ciao!",
            fill="#FFFFFF",
            font=("SFProDisplay Semibold", 20 * -1)
        )

        self.addCanvasElement(textElem1)

        textElem2 = self.gui.canvas.create_text(
            85.0,
            441.0,
            anchor="nw",
            text="Accedi per prenotare",
            fill="#FFFFFF",
            font=("SFProDisplay Heavy", 34 * -1)
        )

        self.addCanvasElement(textElem2)

        id_entry_image = PhotoImage(
            file=relativeToAbsPath(guiutils.usernameEntryRelPath))

        imgElem2 = self.gui.canvas.create_image(
            235.0,
            556.0,
            image=id_entry_image
        )

        self.addCanvasElement(imgElem2)

        IDEntryStringVar = StringVar()

        self.idEntry = Entry(
            bd=0,
            bg="#FFFFFF",
            highlightthickness=0,
            textvariable=IDEntryStringVar
        )

        self.idEntry.place(
            x=100.0,
            y=519.0,
            width=268.0,
            height=72.0
        )

        self.idEntry.bind("<Button-1>", guiutils.deleteTextOnCallback)

        self.addInputEntry(self.idEntry)

        password_entry_image = PhotoImage(
            file=relativeToAbsPath(guiutils.passwordEntryRelPath))

        imgElem3 = self.gui.canvas.create_image(
            235.0,
            643.0,
            image=password_entry_image
        )

        self.addCanvasElement(imgElem3)

        passwordEntryStringVar = StringVar()

        self.passwordEntry = Entry(
            bd=0,
            bg="#FFFFFF",
            highlightthickness=0,
            textvariable=passwordEntryStringVar,
            show="*",
        )
        self.passwordEntry.place(
            x=100.0,
            y=607.0,
            width=270.0,
            height=70.0
        )
        self.passwordEntry.bind("<Button-1>", guiutils.deleteTextOnCallback)

        self.addInputEntry(self.passwordEntry)

        loginButtonImage = PhotoImage(
            file=relativeToAbsPath(guiutils.loginButtonRelPath))

        loginButton = guiutils.addButtonToWindow(
            xPos=180.0,
            yPos=704.0,
            width=95.0,
            height=41.0,
            callback=partial(self.__performInputAction, IDEntryStringVar, passwordEntryStringVar),
            buttonImage=loginButtonImage)

        self.addButtonElement(loginButton)
        self.__setDefaultInput()
        self.gui.window.mainloop()


class CalendarView(AbstractView):

    def __init__(self, gui: 'GUI'):
        super().__init__("calendarView", gui)
        self.cal = None

    def destroyWidgets(self):
        self.cal.destroy()
        super().destroyWidgets()

    def __buildCalendar(self, mindate, maxdate):
        if self.cal is not None:
            self.cal.destroy()
        self.cal = Calendar(self.gui.window, font="Arial 14", selectmode='day', locale='ita',
                            mindate=mindate, maxdate=maxdate, disabledforeground='red', foreground='black',
                            weekendbackground='white', disableddaybackground='gray',
                            firstweekday="monday", cursor="hand")

        self.cal.grid(padx=110, pady=270)

        for i in range(6):
            self.cal._week_nbs[i].destroy()  # evil trick going on here :) pls dont roast my code

        s = ttk.Style(self.gui.window)
        s.theme_use('classic')

    def __prepareBookingAction(self):
        self.gui.date = self.cal.selection_get()
        self.gui.runView(View.BOOKING_VIEW),

    def run(self):
        bookButtonImage = PhotoImage(
            file=relativeToAbsPath(guiutils.bookButtonRelPath))

        bookButton = guiutils.addButtonToWindow(
            xPos=47.0,
            yPos=522.0,
            width=380.0,
            height=44.0,
            callback=self.__prepareBookingAction,
            buttonImage=bookButtonImage)

        self.addButtonElement(bookButton)

        textElem1 = self.gui.canvas.create_text(
            32.0,
            86.0,
            anchor="nw",
            text="Prenotazione",
            fill="#111111",
            font=("Roboto", 16 * -1)
        )

        self.addCanvasElement(textElem1)

        textElem2 = self.gui.canvas.create_text(
            148.0,
            145.0,
            anchor="nw",
            text="Seleziona la data",
            fill="#000000",
            font=("Montserrat Bold", 20 * -1)
        )

        self.addCanvasElement(textElem2)

        today = date.today()

        mindate = today
        maxdate = today + timedelta(days=10)

        self.__buildCalendar(mindate, maxdate)
        self.gui.window.mainloop()


class BookingFailedView(AbstractView):
    def __init__(self, gui: 'GUI'):
        super().__init__("bookingFailedView", gui)

    def run(self):
        textElem1 = self.gui.canvas.create_text(
            107.0,
            150.0,
            anchor="nw",
            text="Prenotazione non andata a buon fine  ",
            fill="#111111",
            font=("Roboto", 16 * -1)
        )

        self.addCanvasElement(textElem1)

        retryButtonImage = PhotoImage(
            file=relativeToAbsPath(guiutils.retryButtonRelPath))

        retryButton = guiutils.addButtonToWindow(
            xPos=119.0,
            yPos=430.0,
            width=236.0,
            height=44.0,
            callback=partial(self.gui.runView, View.BOOKING_VIEW),
            buttonImage=retryButtonImage)

        self.addButtonElement(retryButton)

        changeDateButtonImage = PhotoImage(
            file=relativeToAbsPath(guiutils.changeDateButtonRelPath))

        changeDateButton = guiutils.addButtonToWindow(
            xPos=119.0,
            yPos=372.0,
            width=236.0,
            height=44.0,
            callback=partial(self.gui.runView, View.CALENDAR_VIEW),
            buttonImage=changeDateButtonImage
        )

        self.addButtonElement(changeDateButton)

        textElem2 = self.gui.canvas.create_text(
            32.0,
            86.0,
            anchor="nw",
            text="Prenotazione",
            fill="#111111",
            font=("Roboto", 16 * -1)
        )

        self.addCanvasElement(textElem2)

        closeAppButtonImage = PhotoImage(
            file=relativeToAbsPath(guiutils.closeAppButtonRelPath))

        closeAppButton = guiutils.addButtonToWindow(
            xPos=119.0,
            yPos=314.0,
            width=236.0,
            height=44.0,
            callback=self.gui.window.destroy,
            buttonImage=closeAppButtonImage
        )

        self.addButtonElement(closeAppButton)

        self.gui.window.mainloop()


class BookingView(AbstractView):

    def __init__(self, gui: 'GUI'):
        super().__init__("bookingView", gui)
        self.POLLING_DELAY = 50  # ms
        self.lock = threading.Lock()  # Lock for shared resources.
        self.finished = False
        self.ind = -1
        self.currentLoadingBarXPos = None

    def __destroyLoadingBar(self):
        for widget in self.labelWidgets:
            widget.destroy()

    def __fun(self, j):
        self.__drawBlackBlock(j)
        self.gui.window.update_idletasks()

    def __drawBlackBlock(self, index):
        widget = Label(self.gui.window, bg="#1F2732", width=1, height=1)
        widget.place(x=70 + index - 1 * 22, y=350)
        self.currentLoadingBarXPos = 70 + index - 1 * 22
        self.addLabelWidget(widget)

    def __check_status(self):
        with self.lock:
            if not self.finished:
                self.ind = self.ind + 1
                if self.currentLoadingBarXPos == 400:
                    self.ind = -1
                    self.__destroyLoadingBar()

                self.gui.window.after(1, self.__fun(self.ind))
                self.gui.window.update_idletasks()
                self.gui.window.after(self.POLLING_DELAY, self.__check_status)  # Keep polling.

        if self.finished:
            self.ind = -1  # restore black block starting index
            if self.isBookingOk:
                self.gui.runView(View.BOOKING_OK_VIEW),
            else:
                self.gui.runView(View.BOOKING_FAILED_VIEW),

    def __book(self):
        try:
            self.gui.kairosBot = KairosBot(self.gui.userId, self.gui.password)
            self.gui.window.after(2000, self.gui.kairosBot.book(self.gui.date))
            self.isBookingOk = True
        except Exception as e:
            print(str(e))
            self.isBookingOk = False

        with self.lock:
            self.finished = True

    def __startLoadingBar(self):
        if self.lock.locked():
            self.lock.release()
            self.ind = -1

        with self.lock:
            self.finished = False
        t = threading.Thread(target=self.__book)
        t.daemon = True
        self.__check_status()  # Start polling.
        t.start()

    def run(self):

        textElem1 = self.gui.canvas.create_text(
            32.0,
            86.0,
            anchor="nw",
            text="Prenotazione in corso",
            fill="#111111",
            font=("Roboto", 16 * -1)
        )

        self.addCanvasElement(textElem1)

        textElem2 = self.gui.canvas.create_text(
            140.0,
            250.0,
            anchor="nw",
            text="Prenotazione in corso...",
            fill="#000000",
            font=("Montserrat Bold", 20 * -1)
        )

        self.addCanvasElement(textElem2)

        s = ttk.Style(self.gui.window)
        s.theme_use('classic')

        self.__startLoadingBar()
        self.gui.window.update()
        self.gui.window.mainloop()


class BookingOkView(AbstractView):
    def __init__(self, gui: 'GUI'):
        super().__init__("bookingOkView", gui)
        self.tree = None

    def destroyWidgets(self):
        self.tree.destroy()
        super().destroyWidgets()

    def __buildTreeView(self):
        # Add a self.treeview widget
        self.tree = ttk.Treeview(
            self.gui.window,
            column=("Corso", "Aula", "Orario", "Data"),
            show='headings',
            height=5)
        self.tree.column("# 1", anchor=CENTER)
        self.tree.heading("# 1", text="Corso")
        self.tree.column("# 2", anchor=CENTER)
        self.tree.heading("# 2", text="Aula")
        self.tree.column("# 3", anchor=CENTER)
        self.tree.heading("# 3", text="Orario")
        self.tree.column("# 4", anchor=CENTER)
        self.tree.heading("# 4", text="Data")

        # Insert the data in treeview widget
        for dictEntry in self.gui.kairosBot.bookingInfoDicts:
            self.__fillEntry(dictEntry)
        self.tree.grid(padx=30, pady=270)

        s = ttk.Style(self.gui.window)
        s.theme_use('aqua')

    def __fillEntry(self, entry):
        self.tree.insert(
            '',
            'end',
            text="1",
            values=(entry["courseName"], entry["lessonHall"], entry['lessonTime'], entry['lessonDate'])
        )

    def run(self):
        self.gui.window.geometry(guiutils.getWindowSizeAsString(guiutils.wideWindowWidth, guiutils.wideWindowHeight))
        self.gui.canvas.config(width=864, height=628)

        textElem1 = self.gui.canvas.create_text(
            342.0,
            160.0,
            anchor="nw",
            text="Prenotazione completata",
            fill="#111111",
            font=("Roboto", 16 * -1)
        )

        self.addCanvasElement(textElem1)

        changeDateButtonImage = PhotoImage(
            file=relativeToAbsPath(guiutils.changeDateButtonRelPath))

        changeDateButton = guiutils.addButtonToWindow(
            xPos=310.0,
            yPos=532.0,
            width=236.0,
            height=44.0,
            callback=partial(self.gui.runView, View.CALENDAR_VIEW),
            buttonImage=changeDateButtonImage)

        self.addButtonElement(changeDateButton)

        closeAppButtonImage = PhotoImage(
            file=relativeToAbsPath(guiutils.closeAppButtonRelPath))

        closeAppButton = guiutils.addButtonToWindow(
            xPos=310.0,
            yPos=474.0,
            width=236.0,
            height=44.0,
            callback=self.gui.window.destroy,
            buttonImage=closeAppButtonImage)

        self.addButtonElement(closeAppButton)

        textElem2 = self.gui.canvas.create_text(
            32.0,
            86.0,
            anchor="nw",
            text="Prenotazione",
            fill="#111111",
            font=("Roboto", 16 * -1)
        )

        self.addCanvasElement(textElem2)

        textElem3 = self.gui.canvas.create_text(
            28.0,
            228.0,
            anchor="nw",
            text="Lezioni prenotate",
            fill="#000000",
            font=("Roboto", 22 * -1)
        )

        self.addCanvasElement(textElem3)

        textElem4 = self.gui.canvas.create_text(
            28.0,
            206.0,
            anchor="nw",
            text="Posto a lezione",
            fill="#77767E",
            font=("Roboto", 13 * -1)
        )

        self.addCanvasElement(textElem4)

        self.__buildTreeView()
        self.gui.window.mainloop()


if __name__ == '__main__':
    guis = GUI()
    guis.start()

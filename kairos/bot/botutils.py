from datetime import datetime

monthsDict = {

    'gennaio': 'January',
    'febbraio': 'February',
    'marzo': 'March',
    'aprile': 'April',
    'maggio': 'May',
    'giugno': 'June',
    'luglio': 'July',
    'agosto': 'August',
    'settembre': 'September',
    'ottobre': 'October',
    'novembre': 'November',
    'dicembre': 'December',
    'gen': 'Jan',
    'feb': 'Feb',
    'mar': 'Mar',
    'apr': 'Apr',
    'mag': 'May',
    'giu': 'Jun',
    'lug': 'Jul',
    'ago': 'Aug',
    'set': 'Sep',
    'ott': 'Oct',
    'nov': 'Nov',
    'dic': 'Dec'

}

daysDict = {

    'domenica': 'sunday',
    'lunedì': 'monday',
    'martedì': 'tuesday',
    'mercoledì': 'wednesday',
    'giovedì': 'thursday',
    'venerdì': 'friday',
    'sabato': 'saturday',
    'dom': 'sun',
    'lun': 'mon',
    'mar': 'tue',
    'mer': 'wed',
    'gio': 'thu',
    'ven': 'fri',
    'sab': 'sat'

}


def getDateTimeObjectFromItalianText(italianDateText):
    englishDateString = translateItalianDateToEng(italianDateText)
    # remove day text, we don't need it
    cleanEnglishDateTime = englishDateString.split(' ')
    cleanEnglishDateTime[1] = cleanEnglishDateTime[1].zfill(2)
    cleanEnglishDateTime.pop(0)
    cleanEnglishDateTime = ' '.join(cleanEnglishDateTime)
    cleanEnglishDateTimeObject = datetime.strptime(cleanEnglishDateTime, '%d %B %Y')
    return cleanEnglishDateTimeObject


def translateItalianDateToEng(italianDateText):
    italianDateTextLCase = italianDateText.lower()
    wordsList = italianDateTextLCase.split(" ")

    for i in range(len(wordsList)):
        month = monthsDict.get(wordsList[i])
        if month is not None:
            wordsList[i] = month
            pass
        day = daysDict.get(wordsList[i])
        if day is not None:
            wordsList[i] = day

    dateString = ' '.join(wordsList)

    return dateString


""" super hardcoded crappy parsing function :( pls don't roast me

 following comments will illustrate a real parsing case.
 string to parse : 
     
     Hai prenotato la lezione:
     BILANCIO D ESERCIZIO (Cognomi M-Z)
     Martedì 19 Ottobre 2021, 08:20 - 09:40
     D6/0.18 [D6] 
     
"""


def parseBookingInfo(bookingInfo):
    infoDict = {
        "courseName": "courseName",
        "lessonHall": "lessonHall",
        "lessonDate": "lessonDate",
        "lessonTime": "lessonTime"
    }

    """ after first replacement we remove useless part. This is what remains :
        
        BILANCIO D ESERCIZIO (Cognomi M-Z)
        Martedì 19 Ottobre 2021, 08:20 - 09:40
        D6/0.18 [D6] 
        
    """

    bookingInfo = bookingInfo.replace("Hai prenotato la lezione:\n", "")

    # courseName = "BILANCIO D ESERCIZIO"
    infoDict['courseName'] = bookingInfo.split(' (')[0]

    """ Progressive bookingInfo reduction to obtain needed info :
    
        Martedì 19 Ottobre 2021, 08:20 - 09:40
        D6/0.18 [D6] 
        
    """
    bookingInfo = bookingInfo.split(')')[1]
    #                              date conversion from str to datetime <-(date string extracted)
    infoDict['lessonDate'] = getDateTimeObjectFromItalianText(bookingInfo.split(',')[0]).date()

    """ Progressive bookingInfo reduction to obtain needed info :

         08:20 - 09:40
        D6/0.18 [D6] 

    """
    bookingInfo = bookingInfo.split(',')[1]

    # remove leading space
    bookingInfo = bookingInfo[1:]

    # lessonTime is composed by the first 13 characters in bookingInfo string
    infoDict['lessonTime'] = bookingInfo[:13]

    """ Progressive bookingInfo reduction to obtain needed info :
    
        D6/0.18 [D6] 

    """
    bookingInfo = bookingInfo[14:]

    infoDict['lessonHall'] = bookingInfo

    return infoDict
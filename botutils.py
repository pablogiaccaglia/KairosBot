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


if __name__ == '__main__':

    str = "Venerdì 8 Ottobre 2021"
    getDateTimeObjectFromItalianText(str)

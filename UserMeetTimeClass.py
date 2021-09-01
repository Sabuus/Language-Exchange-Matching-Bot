import re
from datetime import datetime
from dateutil import tz

validLanguages = ["jp", "en"]

class UserMeetTime:
    def __init__(self, userInput):
        self.user = userInput.author.mention
        self.isValidInput = True
        self.languageSelected = ""
        self.startTime = datetime.now()
        self.endTime = datetime.now()
        self.timezone = ""


        content = re.split(' ', userInput.content)
        self.checkString(content)

    # Refactor this to be more manageable
    def checkString(self, inputStringArray):
        if inputStringArray[1] in validLanguages:
            self.languageSelected = inputStringArray[1]
        else:
            self.isValidInput = False

        try:
            print("input array 2" + inputStringArray[2])
            date = inputStringArray[2].replace('／', '/')

            baseTime = datetime.strptime(date, '%m/%d')

            baseTime = baseTime.replace(year=datetime.now().year)

            inputStringArray[3].replace('ー', '-')

            times = inputStringArray[3].split('-')

            self.startTime = self.generateTimeAttribute(times[0], baseTime)
            self.endTime = self.generateTimeAttribute(times[1], baseTime)

            # Need to fix this, timezones require a specific location for tz module
            self.timezone = inputStringArray[4]
            # self.timezone = tz.gettz(inputStringArray[4])
            # self.desiredTime.astimezone(self.timezone)
        except TypeError:
            self.isValidInput = False

    def generateTimeAttribute(self, timeStr, dateToReplaceWith):
        timeStr.replace('：', ':')

        tmpTime = datetime.strptime(timeStr, "%H:%M")

        return tmpTime.replace(year=dateToReplaceWith.year, month=dateToReplaceWith.month, day=dateToReplaceWith.day)

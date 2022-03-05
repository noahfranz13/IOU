from datetime import datetime

class Event:

    def __init__(self, userName, eventName, startTime, endTime, date):
        '''
        userName [str] : username used to login to the website
        eventName [str] : name of the event
        startTime [str] : str of the start time in 24h format like hh:mm
        endTime [str] : str of the end time in 24h format like hh:mm
        date [str] : date of the event in format mm/dd/yyyy
        '''

        self.userName = userName
        self.eventName = eventName

        m, d, y = int(date.split('/')[0]), int(date.split('/')[1]), int(date.split('/')[2])
        h0, m0, s0, ms0 = int(startTime.split(':')[0]), int(startTime.split(':')[1]), 0, 0
        hf, mf, sf, msf = int(endTime.split(':')[0]), int(endTime.split(':')[1]), 0, 0

        self.startTime = datetime(y, m, d, h0, m0, s0, ms0)
        self.endTime = datetime(y, m, d, hf, mf, sf, msf)

    def __str__(self):
        return f"username : {self.userName}\nEvent Name : {self.eventName}\nTime : {self.startTime} to {self.endTime}"

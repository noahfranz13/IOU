# imports
import os
import numpy as np
import pandas as pd
import pymysql

from Event import Event

class IO:

    def __init__(self, userName):
        self.userName = userName
        self.events = self.queryUser()

    def queryUser(self):
        '''
        Method to return a list of Event objects with the given userName
        '''

        # TODO : change this to query the mysql database for the given username
        # for now just read in a csv
        eventTable = pd.read_csv(os.path.join(os.getcwd(), 'EVENT_TABLE.csv'))
        eventTableByUser = eventTable[eventTable['UserName'] == self.userName]

        # throw error if the user does not have any events
        if (len(eventTableByUser) == 0):
            raise ValueError(f'{self.userName} has no events')

        eventList = []
        for ii, row in eventTableByUser.iterrows():
            event = Event(row['UserName'], row['Event'], row['StartTime'], row['EndTime'], row['StartDate'])
            eventList.append(event)
            print(event)

        return eventList

    def writeNewRow(self):
        pass

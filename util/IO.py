# imports
import os
import numpy as np
import pandas as pd
import pymysql
from pandas.plotting import table
import matplotlib.pyplot as plt

from util.Event import Event

class IO:

    def __init__(self, userName):
        self.userName = userName
        self.mysql = self.dbConnect()
        self.events = self.queryUser()

    def dbConnect(self):
        mysql = pymysql.connect(database ='IOU_DB',
                                host='localhost',
                                user='noahf',
                                password='1')
        return mysql

    def queryUser(self):
        '''
        Method to return a list of Event objects with the given userName
        '''

        # TODO : change this to query the mysql database for the given username
        # for now just read in a csv
        #eventTable = pd.read_csv(os.path.join(os.getcwd(), 'EVENT_TABLE.csv'))
        #eventTableByUser = eventTable[eventTable['UserName'] == self.userName]

        query = f'''
                SELECT *
                FROM EVENT_TABLE
                WHERE UserName='{self.userName}'
                '''

        eventTableByUser = pd.read_sql(query, self.mysql)

        # throw error if the user does not have any events
        if (len(eventTableByUser) == 0):
            raise ValueError(f'{self.userName} has no events')

        eventList = []
        for ii, row in eventTableByUser.iterrows():
            event = Event(row['UserName'], row['Event'], row['StartTime'], row['EndTime'], row['StartDate'])
            eventList.append(event)
            print(event)

        return eventList

    def writeNewEvent(self, table, event, start, end, startDate):

        sqlcmd = f"""
                INSERT INTO {table} VALUES {(self.userName, event, start, end, startDate)}
                """
        print(sqlcmd)
        cursor = self.mysql.cursor()
        cursor.execute(sqlcmd)
        self.mysql.commit()

    def removeEvent(self, event, date):
        sqlcmd = f"""
                DELETE FROM EVENT_TABLE
                WHERE UserName = '{self.userName}'
                AND Event = '{event}'
                AND StartDate = '{date}'
                """
        cursor = self.mysql.cursor()
        cursor.execute(sqlcmd)
        self.mysql.commit()

    def queryOweTable(self):

        query = f"""
                SELECT *
                FROM OWE_TABLE
                WHERE ower = '{self.userName}'
                """

        oweTable = pd.read_sql(query, self.mysql)
        print(oweTable)

        if len(oweTable) > 0:

            fig = plt.figure()

            ax = plt.subplot(111, frame_on=False) # no visible frame
            ax.xaxis.set_visible(False)  # hide the x axis
            ax.yaxis.set_visible(False)  # hide the y axis
            table(ax, oweTable)

            return fig
        else:
            return "You don't have any debt!!"

    def addRequest(self, startDate, start, end, eventName):

        sqlcmd = f"""
                INSERT INTO REQUESTS VALUES {(self.userName, startDate, start, end, eventName)}
                """
        print(sqlcmd)
        cursor = self.mysql.cursor()
        cursor.execute(sqlcmd)
        self.mysql.commit()

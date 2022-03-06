# imports
import os
import numpy as np
import pandas as pd
import pymysql
from pandas.plotting import table
import matplotlib.pyplot as plt
from datetime import datetime

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

    def queryRequestTable(self):

        query = f"""
                SELECT *
                FROM REQUESTS
                WHERE Requestor != '{self.userName}'
                """

        reqTable = pd.read_sql(query, self.mysql)
        print(reqTable)

        if len(reqTable) > 0:

            fig = plt.figure()

            ax = plt.subplot(111, frame_on=False) # no visible frame
            ax.xaxis.set_visible(False)  # hide the x axis
            ax.yaxis.set_visible(False)  # hide the y axis
            table(ax, reqTable)

            return fig
        else:
            return "There are no requests"

    def addRequest(self, startDate, start, end, eventName):

        sqlcmd = f"""
                INSERT INTO REQUESTS VALUES {(self.userName, startDate, start, end, eventName)}
                """
        print(self.userName, startDate, start, end, eventName)
        sqlCheck = f"""
                    SELECT *
                    FROM EVENT_TABLE
                    WHERE UserName='{self.userName}'
                    AND StartDate='{startDate}'
                    AND StartTime='{start}'
                    AND EndTime='{end}'
                    AND Event='{eventName}'
                    """

        cursor = self.mysql.cursor()
        print(pd.read_sql(sqlCheck, self.mysql))
        if len(pd.read_sql(sqlCheck, self.mysql)) == 0:
            raise ValueError('Please Enter Values for an existing event')

        cursor.execute(sqlcmd)
        self.mysql.commit()

    def fulfill(self, eventName, eventDate, otherFirst, otherLast):

        cursor = self.mysql.cursor()

        # get other User name
        getOtherUser = f"""
                        SELECT *
                        FROM USERNAME
                        WHERE FirstName='{otherFirst}'
                        AND LastName='{otherLast}'
                        """
        userInfo = pd.read_sql(getOtherUser, self.mysql)
        otherUser = userInfo['UserName'].tolist()[0]

        # first remove request from REQUEST table
        sqlcmd = f"""
                DELETE FROM REQUESTS
                WHERE Requestor = '{otherUser}'
                AND EventName = '{eventName}'
                AND StartDate = '{eventDate}'
                """

        cursor.execute(sqlcmd)
        #self.mysql.commit()

        # get event hours
        eventsQuery = f"""
                    SELECT *
                    FROM EVENT_TABLE
                    WHERE UserName='{otherUser}'
                    AND Event='{eventName}'
                    AND StartDate='{eventDate}'
                    """

        print(eventsQuery)

        events = pd.read_sql(eventsQuery, self.mysql)

        if len(events) > 1:
            raise ValueError('Duplicate Events!!! Exiting...')

        print(events)
        event = Event(events['UserName'].tolist()[0],
                      events['Event'].tolist()[0],
                      events['StartTime'].tolist()[0],
                      events['EndTime'].tolist()[0],
                      events['StartDate'].tolist()[0])

        eventHrs = event.endTime - event.startTime
        eventHrs = eventHrs.total_seconds()/3600 # convert eventHrs to hr float

        # change username on the event in EVENT_TABLE
        updateCmd = f"""
                    UPDATE EVENT_TABLE
                    SET UserName='{self.userName}'
                    WHERE UserName='{otherUser}'
                    AND Event='{eventName}'
                    AND StartDate='{eventDate}'
                    """
        print()
        print("update comm: ", updateCmd)
        print()

        cursor.execute(updateCmd)
        #self.mysql.commit()

        # get relevant rows in OWE_TABLE and check figure out if you owe the otherUser
        getOwes = f"""
                    SELECT *
                    FROM OWE_TABLE
                    WHERE owes='{otherUser}'
                    AND ower='{self.userName}'
                    """

        oweTable = pd.read_sql(getOwes, self.mysql)

        if len(oweTable) > 0:
            hoursOwed = oweTable['amount'].tolist()[0]
        else:
            hoursOwed = 0

        # now calculate who owes what hours and insert
        if hoursOwed - eventHrs == 0:
            deleteEvent = f"""
                    DELETE FROM OWE_TABLE
                    WHERE ower = '{self.userName}'
                    AND owes = '{otherUser}'
                    """
            cursor.execute(deleteEvent)
            #self.mysql.commit()

        elif hoursOwed - eventHrs < 0:
            # first remove old owed hours
            deleteEvent = f"""
                    DELETE FROM OWE_TABLE
                    WHERE ower = '{self.userName}'
                    AND owes = '{otherUser}'
                    """
            cursor.execute(deleteEvent)
            #self.mysql.commit()

            # then add new row with conjugate
            addEvent = f"""
                        INSERT INTO OWE_TABLE VALUES {(otherUser, self.userName, eventHrs-hoursOwed)}
                        """
            cursor.execute(addEvent)
            #self.mysql.commit()

        else:
            owesUpdate = f"""
                        UPDATE OWE_TABLE
                        SET amount='{hoursOwed-eventHrs}'
                        WHERE ower='{self.userName}'
                        AND owes='{otherUser}'
                        """

            cursor.execute(owesUpdate)

        self.mysql.commit()

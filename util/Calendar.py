
import os
from util.IO import IO
from util.Event import Event
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
from datetime import date, timedelta, datetime
import pandas as pd


class Calendar:

    def __init__(self, username):

        self.usernames = username
        io = IO(self.usernames)
        self.mysql = io.dbConnect()

    def plotEvents(self, today, defaultUserName=None):
        '''
        defaultUserName : the current user
        '''
        otherEvents = []
        if defaultUserName != None:

            query = f"""
                    SELECT *
                    FROM REQUESTS
                    WHERE Requestor != '{defaultUserName}'
                    """

            reqTable = pd.read_sql(query, self.mysql)

            for ii, row in reqTable.iterrows():
                event = Event(row['Requestor'], row['EventName'], row['StartTime'], row['EndTime'], row['StartDate'])
                otherEvents.append(event)


        colors = ['firebrick', 'dodgerblue', 'seagreen']

        colorIdx = 0
        #raise ValueError('made it')
        fig, axs = plt.subplots(1, 7, figsize=(30, 15))


        # get new ioObj
        io = IO(self.usernames)

        # generate list of next 7 days
        datesList = [today + timedelta(days=i) for i in range(7)]

        # generate plot of the users schedule for the next 7 days

        strTimes = [f"{ii}:00" for ii in range(24)]
        axs[0].set_ylabel('Time [hh:mm]', fontsize=30)

        x = [0, 1]

        for ax, dd in zip(axs, datesList):
            ax.set_title(dd.strftime("%m/%d"), fontsize=24)
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_ylim(24)

            for jj in range(24):
                ax.axhline(jj, x[0], x[1], ls='--', color='k', alpha=0.5)

            for event in io.events:
                if event.startTime.strftime("%m/%d") == dd.strftime("%m/%d"):
                    startHr = int(event.startTime.strftime("%H"))
                    startMin = int(event.startTime.strftime("%M"))
                    endHr = int(event.endTime.strftime("%H"))
                    endMin = int(event.endTime.strftime("%M"))
                    ax.fill_between(x, startHr + startMin/60, endHr + endMin/60, color=colors[0], alpha=0.5)
                    midpoint = (startHr + startMin/60 + endHr + endMin/60)/2
                    ax.text(0, midpoint, event.eventName, color='w', fontsize=24)

            for event in otherEvents:
                if event.startTime.strftime("%m/%d") == dd.strftime("%m/%d"):
                    startHr = int(event.startTime.strftime("%H"))
                    startMin = int(event.startTime.strftime("%M"))
                    endHr = int(event.endTime.strftime("%H"))
                    endMin = int(event.endTime.strftime("%M"))
                    ax.fill_between(x, startHr + startMin/60, endHr + endMin/60, color=colors[1], alpha=0.5)
                    midpoint = (startHr + startMin/60 + endHr + endMin/60)/2
                    ax.text(0, midpoint, event.eventName, color='w', fontsize=24)

                    cursor = self.mysql.cursor()

                    # get other User name
                    getNames = f"""
                                    SELECT *
                                    FROM USERNAME
                                    WHERE UserName='{event.userName}'
                                    """
                    userInfo = pd.read_sql(getNames, self.mysql)
                    first = userInfo['FirstName'].tolist()[0]
                    last = userInfo['LastName'].tolist()[0]


                    ax.text(0, midpoint+1, first+" "+last, color='w', fontsize=24)

        axs[0].set_yticks(np.arange(len(strTimes)), labels=strTimes, fontsize=24)
        fig.suptitle("Year: " + datesList[0].strftime("%Y"), fontsize=36)

        return fig

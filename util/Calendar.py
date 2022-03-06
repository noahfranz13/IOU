
import os
from util.IO import IO
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
from datetime import date, timedelta, datetime


class Calendar:

    def __init__(self, username):

        self.usernames = username

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

        fig, axs = plt.subplots(1, 7, figsize=(30, 15))

        # get new ioObj
        io = IO(self.usernames)

        # generate list of next 7 days
        datesList = [today + timedelta(days=i) for i in range(7)]

        # generate plot of the users schedule for the next 7 days
        font = {'family' : 'DejaVu Sans',
                'weight' : 'bold',
                'size' : 24}
        rc('font', **font)

        strTimes = [f"{ii}:00" for ii in range(24)]
        axs[0].set_ylabel('Time [hh:mm]', fontsize=30)

        x = [0, 1]

        for ax, dd in zip(axs, datesList):
            ax.set_title(dd.strftime("%m/%d"))
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_ylim(24)

            for jj in range(24):
                ax.axhline(jj, x[0], x[1], ls='--', color='k', alpha=0.5)

            print(io.events+otherEvents)
            for event in io.events+otherEvents:
                if event.startTime.strftime("%m/%d") == dd.strftime("%m/%d"):
                    startHr = int(event.startTime.strftime("%H"))
                    startMin = int(event.startTime.strftime("%M"))
                    endHr = int(event.endTime.strftime("%H"))
                    endMin = int(event.endTime.strftime("%M"))
                    ax.fill_between(x, startHr + startMin/60, endHr + endMin/60, color=colors[colorIdx], alpha=0.5)
                    midpoint = (startHr + startMin/60 + endHr + endMin/60)/2
                    ax.text(0, midpoint, event.eventName, color='w')

        axs[0].set_yticks(np.arange(len(strTimes)), labels=strTimes)
        fig.suptitle("Year: " + datesList[0].strftime("%Y"), fontsize=36)

        return fig

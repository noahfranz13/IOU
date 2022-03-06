
import os
from util.IO import IO
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
from datetime import date, timedelta, datetime


class Calendar:

    def __init__(self, usernames):

        if type(usernames) == str:
            usernames = [usernames]

        if len(usernames) > 3:
            raise ValueError('Please only enter up to 3 usernames')

        self.today = date.today()
        self.usernames = usernames

    def plotEvents(self, today):

        colors = ['firebrick', 'dodgerblue', 'seagreen']

        fig, axs = plt.subplots(1, 7, figsize=(30, 15))

        for colorIdx, user in enumerate(self.usernames):

            # get new ioObj
            io = IO(user)

            # generate list of next 7 days
            datesList = [today + timedelta(days=i) for i in range(7)]

            # generate plot of the users schedule for the next 7 days
            font = {'family' : 'DejaVu Sans',
                    'weight' : 'normal',
                    'size' : 20}
            rc('font', **font)

            strTimes = [f"{ii}:00" for ii in range(24)]
            axs[0].set_ylabel('Time [hh:mm]')

            x = [0, 1]

            for ax, dd in zip(axs, datesList):
                ax.set_title(dd.strftime("%m/%d"))
                ax.set_xticks([])
                ax.set_yticks([])
                ax.set_ylim(24)

                for ii in range(24):
                    ax.axhline(ii, x[0], x[1], ls='--', color='k', alpha=0.5)

                for event in io.events:
                    if event.startTime.strftime("%m/%d") == dd.strftime("%m/%d"):
                        startHr = int(event.startTime.strftime("%H"))
                        startMin = int(event.startTime.strftime("%M"))
                        endHr = int(event.endTime.strftime("%H"))
                        endMin = int(event.endTime.strftime("%M"))
                        ax.fill_between(x, startHr + startMin/60, endHr + endMin/60, color=colors[colorIdx], alpha=0.5)
                        midpoint = (startHr + startMin/60 + endHr + endMin/60)/2
                        ax.text(0, midpoint, event.eventName, color='w')

            axs[0].set_yticks(np.arange(len(strTimes)), labels=strTimes)
            fig.suptitle("Year: " + datesList[0].strftime("%Y"))

        return fig

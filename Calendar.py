from IO import IO
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
from datetime import date, timedelta, datetime


class Calendar:

    def __init__(self, username):

        ioObj = IO(username)
        self.events = ioObj.events
        self.userName = ioObj.userName
        self.today = date.today()

    def plotEvents(self, filename='today.png'):

        # generate list of next 7 days
        datesList = [self.today + timedelta(days=i) for i in range(7)]

        # generate plot of the users schedule for the next 7 days
        font = {'family' : 'DejaVu Sans',
                'weight' : 'normal',
                'size' : 20}
        rc('font', **font)

        fig, axs = plt.subplots(1, 7, figsize=(30, 15))
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

            for event in self.events:
                if event.startTime.strftime("%m/%d") == dd.strftime("%m/%d"):
                    startHr = int(event.startTime.strftime("%H"))
                    startMin = int(event.startTime.strftime("%M"))
                    endHr = int(event.endTime.strftime("%H"))
                    endMin = int(event.endTime.strftime("%M"))
                    ax.fill_between(x, startHr + startMin/60, endHr + endMin/60)
                    midpoint = (startHr + startMin/60 + endHr + endMin/60)/2
                    ax.text(0, midpoint, event.eventName, color='w')

        axs[0].set_yticks(np.arange(len(strTimes)), labels=strTimes)
        fig.suptitle("Year: " + datesList[0].strftime("%Y"))
        fig.savefig(filename)

    def plotPrevious(self):
        self.today = self.today-timedelta(days=1)
        self.plotEvents(filename='previous.png')

    def plotNext(self):
        self.today = self.today+timedelta(days=1)
        self.plotEvents(filename='next.png')

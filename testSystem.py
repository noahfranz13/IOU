import sys
from IO import IO
from Calendar import Calendar
def main():

    queryObj = IO('ssmall')

    print(queryObj.userName)

    cal = Calendar(queryObj.userName)
    cal.plotEvents()
    cal.plotNext()
    cal.plotPrevious()

if __name__ == '__main__':
    sys.exit(main())

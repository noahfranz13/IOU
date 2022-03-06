import sys
from util.IO import IO
from util.Calendar import Calendar
def main():

    queryObj = IO('ssmall')

    print(queryObj.userName)

    cal = Calendar(queryObj.userName)
    cal.plotEvents()
    cal.plotNext()
    cal.plotPrevious()

if __name__ == '__main__':
    sys.exit(main())

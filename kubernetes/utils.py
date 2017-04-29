import time
from datetime import datetime

class TimeUtils:
    @staticmethod
    def ConvertFromGoTime(goTimeStr):
        ''' Convert go time str to python datetime '''
        return datetime.strptime(goTimeStr, '%Y-%m-%dT%H:%M:%SZ')


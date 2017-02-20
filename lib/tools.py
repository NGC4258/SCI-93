import json
import redis
import time

from datetime import datetime
from datetime import timedelta

class DataProcess(object):

    def google(self, content):
        data = content.strip("\n").split("\n")
        columns = []
        results = []
        resultsApd = results.append
        axis = 0

        for datum in data:
            if str(datum[0]).isupper():
                #fetch COLUMNS
                if str(datum[0]) == "C":
                    columns = datum.split("=")[1]
                    colNames = columns.split(",")
                    continue
                else:
                    continue

            if datum[0] == "a":
                numbers = datum.split(",")
                #fetch the axis of date
                axis = datetime.utcfromtimestamp(int(str(numbers[0])[1:]))
                date = axis.strftime("%Y-%m-%d")
            else:
                numbers = datum.split(",")
                date = (axis + timedelta(days=int(numbers[0]))).strftime("%Y-%m-%d")

            resultsApd({
                colNames[0]: date,
                colNames[1]: numbers[1],
                colNames[2]: numbers[2],
                colNames[3]: numbers[3],
                colNames[4]: numbers[4],
                colNames[5]: numbers[5]
            })

        return results

class DataManage(object):

    def __init__(self):
        self.r = redis.StrictRedis(host='localhost', port=6379, db=0)
        self.today = datetime.today()

    def get_stocks(self):
        stocks = self.r.keys()

        for stock in stocks:
            if stock.isdigit():
                yield stock

    def scarcity_in_half_year(self, stock):
        date = sorted(self.r.hkeys(stock))

        if len(date) == 1:
            return 365

        y, m, d = date[-1].split("-")
        lastDay = datetime(int(y), int(m), int(d))

        return (self.today - lastDay).days

    def store(self, stock, data):
        for datum in data:
            date = datum.pop("DATE")
            self.r.hset(stock, date, json.dumps(datum))

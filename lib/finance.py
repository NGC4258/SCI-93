import requests

class Google(object):

    def __init__(self):
        self.uri = "http://www.google.com/finance/getprices?q=%(stock)s&x=TPE&i=86400&p=%(duration)s&f=d,c,h,l,o,v"

    def request(self, stock, duration):
        resp = requests.request("GET", self.uri % {"stock": str(stock), "duration": duration})

        return resp.status_code, resp.content

    def get(self, scarcity, stock):
        if scarcity >= 365:
            return self.getSixYears(stock)

        if scarcity > 30 and scarcity < 365:
            return self.getOneYear(stock)

        return self.getOneMonth(stock)

    def getOneMonth(self, stock):
        return self.request(stock, "1M")

    def getOneYear(self, stock):
        return self.request(stock, "1Y")

    def getSixYears(self, stock):
        return self.request(stock, "6Y")
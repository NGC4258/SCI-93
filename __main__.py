#!/usr/bin/env python

import logging
import sys
import time

from os import environ
from os import listdir
from os import mkdir
from os.path import abspath
from os.path import basename
from os.path import dirname
from os.path import isdir
from os.path import isfile
from os.path import join as pjoin
from os.path import realpath
from os.path import split

def check_environment():
    return 0

def data_camp():

    def check_out_scarcity(stock):
        try:
            scarcity = dm.scarcity_in_half_year(stock)
        except Exception as e:
            log.error(e)
        else:
            return scarcity

        return

    def fetch_values_from_google(scarcity, stock):
        try:
            log.info("Fetching %s, %s day(s)" % (stock, scarcity))
            code, content = google.get(scarcity, stock)
        except Exception as e:
            log.error(e)
        else:
            if code == 200:
                return content
            else:
                log.error("code: %s, %s" % (code, content))

        return

    def data_process(content):
        try:
            results = dp.google(content)
        except Exception as e:
            log.error(e)
        else:
            return results

        return

    def store_data_to_redis(stock, results):
        try:
            dm.store(stock, results)
        except Exception as e:
            log.error(e)

    n = 0

    for stock in dm.get_stocks():
        scarcity = check_out_scarcity(stock)

        if not scarcity:
            continue
            
        content = fetch_values_from_google(scarcity, stock)

        if not content:
            continue

        results = data_process(content)

        if results:
            store_data_to_redis(stock, results)

        n = n + 1

    log.info("%s stock(s) to camp" % n)

    return 0

def main():

    startT = time.time()

    procedure = (
        check_environment,
        data_camp
    )

    log.info("$" * 50)
    log.info("$ Start {0:40} $".format(pName))
    log.info("$" * 50)

    for process in procedure:
        log.info("-" * 40)
        log.info("| {0:36} |".format(process.__name__))
        log.info("-" * 40)

        result = process()

        if result:
            log.error("Error, %s" % result)

    log.info("-" * 40)
    log.info("Finished, total time taken: %s" % round(time.time() - startT, 2))

if __name__ == "__main__":
    #Fetch project location
    path = split(realpath(__file__))[0]

    #Fetch parent path of project
    pName = basename(path)
    pPath = abspath(dirname(path))

    #Determine logging location
    logName = "%s.log" % pName
    logPath = pjoin(pPath, logName)

    #Initial logging
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    log = logging.getLogger()
    log.setLevel(logging.INFO)
    fh = logging.FileHandler(logPath)
    formatter = logging.Formatter("%(asctime)s %(levelname)s "
                                  "- %(message)s", "%Y-%m-%d %H:%M:%S"
    )
    fh.setFormatter(formatter)
    log.addHandler(fh)

    #Load libaries
    try:
        from lib.finance import Google
        from lib.tools import DataProcess
        from lib.tools import DataManage
    except Exception as e:
        sys.exit("%s, error: %s" % (__name__, str(e)))
    else:
        google = Google()
        dp = DataProcess()
        dm = DataManage()

    main()

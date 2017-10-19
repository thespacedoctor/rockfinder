#!/usr/local/bin/python
# encoding: utf-8
"""
rockfinder can be used to generate ephemerides for your favourite asteroids

Usage:
    rockfinder where [-eo] [csv|md|rst|json|yaml] <obscode> <objectId> <mjd>

Options:
    obscode               the observatory code to use for ephemeris generation
    csv                   output results in csv format
    md                    output results as a markdown table
    rst                   output results as a restructured text table
    json                  output results in json format
    yaml                  output results in yaml format

    -e, --extra           return extra ephemeris info (verbose)
    -o, --orbfit          use orbfit instead of JPL to generate ephemerides (requires bespoke orbfit `ephem` executable)
    -h, --help            show this help message
"""
################# GLOBAL IMPORTS ####################

import sys
import os
os.environ['TERM'] = 'vt100'
import readline
import glob
import pickle

from docopt import docopt
from fundamentals import tools, times
from fundamentals.renderer import list_of_dictionaries
# from ..__init__ import *


def main(arguments=None):
    """
    *The main function used when ``cl_utils.py`` is run as a single script from the cl, or when installed as a cl command*
    """

    # setup the command-line util settings
    su = tools(
        arguments=arguments,
        docString=__doc__,
        logLevel="WARNING",
        options_first=False,
        projectName="rockfinder",
        defaultSettingsFile=True
    )
    arguments, settings, log, dbConn = su.setup()

    # unpack remaining cl arguments using `exec` to setup the variable names
    # automatically
    for arg, val in arguments.iteritems():
        if arg[0] == "-":
            varname = arg.replace("-", "") + "Flag"
        else:
            varname = arg.replace("<", "").replace(">", "")
        if isinstance(val, str) or isinstance(val, unicode):
            exec(varname + " = '%s'" % (val,))
        else:
            exec(varname + " = %s" % (val,))
        if arg == "--dbConn":
            dbConn = val
        log.debug('%s = %s' % (varname, val,))

    ## START LOGGING ##
    startTime = times.get_now_sql_datetime()
    log.info(
        '--- STARTING TO RUN THE cl_utils.py AT %s' %
        (startTime,))

    # CALL FUNCTIONS/OBJECTS

    if where and orbfitFlag:
        from rockfinder import orbfit_ephemeris
        eph = orbfit_ephemeris(
            log=log,
            objectId=objectId,
            mjd=mjd,
            obscode=obscode,
            settings=settings,
            verbose=extraFlag
        )
    else:
        from rockfinder import jpl_horizons_ephemeris
        eph = jpl_horizons_ephemeris(
            log=log,
            objectId=objectId,
            mjd=mjd,
            obscode=obscode,
            verbose=extraFlag
        )

    dataSet = list_of_dictionaries(
        log=log,
        listOfDictionaries=eph
    )
    # xfundamentals-render-list-of-dictionaries

    output = dataSet.table(filepath=None)
    if csv:
        output = dataSet.csv(filepath=None)
    elif json:
        output = dataSet.json(filepath=None)
    elif yaml:
        output = dataSet.yaml(filepath=None)
    elif md:
        output = dataSet.markdown(filepath=None)
    elif rst:
        output = dataSet.reST(filepath=None)

    print output

    if "dbConn" in locals() and dbConn:
        dbConn.commit()
        dbConn.close()
    ## FINISH LOGGING ##
    endTime = times.get_now_sql_datetime()
    runningTime = times.calculate_time_difference(startTime, endTime)
    log.info('-- FINISHED ATTEMPT TO RUN THE cl_utils.py AT %s (RUNTIME: %s) --' %
             (endTime, runningTime, ))

    return


if __name__ == '__main__':
    main()

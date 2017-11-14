#!/usr/local/bin/python
# encoding: utf-8
"""
*Generate Ephemerides using the `ephem` command from the Orbfit5.0 fork*

:Author:
    David Young

:Date Created:
    September 28, 2017
"""
################# GLOBAL IMPORTS ####################
import sys
import os
os.environ['TERM'] = 'vt100'
from fundamentals import tools
from subprocess import Popen, PIPE, STDOUT
from os.path import expanduser
import collections
from fundamentals import fmultiprocess


def _generate_one_ephemeris(
        cmd):
    """generate one orbfit ephemeris

    **Key Arguments:**
        - ``cmd`` -- the command to execute [cmd, object]

    **Return:**
        - ``result`` -- the single ephemeris
    """
    p = Popen(cmd[0], stdout=PIPE, stderr=PIPE, shell=True)
    stdout, stderr = p.communicate()

    p.stdout.close()
    p.stderr.close()

    if len(stderr) and len(stderr.split()) != 15:
        print stderr, len(stderr.split())
        return None
    elif "!!WARNING! WARNING! WARNING! WARNING!!" in stdout:
        print "%(stdout)s was not found in astorb.dat" % locals()
        return None

    # SPLIT RESULTS INTO LIST OF DICTIONARIES
    r = stdout.strip().split("\n")
    keys = r[0].strip().split(',')
    lines = r[1:]
    for l in lines:
        # CREATE DICTIONARY FROM KEYS AND VALUES
        values = l.strip().split(',')
        for k, v in zip(keys, values):
            v = v.strip().replace("/", "")
            try:
                v = float(v)
            except:
                pass
        result = dict(zip(keys, values))
        result["object_name"] = cmd[1]
    return result


def orbfit_ephemeris(
        log,
        objectId,
        mjd,
        settings,
        obscode=500,
        verbose=False,
        astorbPath=False):
    """Given a known solar-system object ID (human-readable name or MPC number but *NOT* an MPC packed format) or list of names and one or more specific epochs, return the calculated ephemerides

    **Key Arguments:**
        - ``log`` -- logger
        - ``objectId`` -- human-readable name, MPC number or solar-system object name, or list of names
        - ``mjd`` -- a single MJD, or a list MJDs to generate an ephemeris for
        - ``settings`` -- the settings dictionary for rockfinder
        - ``obscode`` -- the observatory code for the ephemeris generation. Default **500** (geocentric)
        - ``verbose`` -- return extra information with each ephemeris
        - ``astorbPath`` -- override the default path to astorb.dat orbital elements file

    **Return:**
        - ``resultList`` -- a list of ordered dictionaries containing the returned ephemerides

    **Usage:**

        To generate a an ephemeris for a single epoch run,using ATLAS Haleakala as your observatory:

        .. code-block:: python

            from rockfinder import orbfit_ephemeris
            eph = orbfit_ephemeris(
                log=log,
                objectId=1,
                obscode="T05"
                mjd=57916.,
            )

        or to generate an ephemeris for multiple epochs:

        .. code-block:: python

            from rockfinder import orbfit_ephemeris
            eph = orbfit_ephemeris(
                log=log,
                objectId="ceres",
                mjd=[57916.1,57917.234,57956.34523]
                verbose=True
            )

        Note by passing `verbose=True` the essential ephemeris data is supplimented with some extra data

        It's also possible to pass in an array of object IDs:

        .. code-block:: python

            from rockfinder import orbfit_ephemeris
            eph = orbfit_ephemeris(
                log=log,
                objectId=[1,5,03547,"Shikoku"],
                mjd=[57916.1,57917.234,57956.34523]
            )

        And finally you override the default path to astorb.dat orbital elements file by passing in a custom path (useful for passing in a trimmed orbital elements database):

        .. code-block:: python

            from rockfinder import orbfit_ephemeris
            eph = orbfit_ephemeris(
                log=log,
                objectId=[1,5,03547,"Shikoku"],
                mjd=[57916.1,57917.234,57956.34523],
                astorbPath="/path/to/astorb.dat"
            )

    """
    log.info('starting the ``orbfit_ephemeris`` function')

    # MAKE SURE MJDs ARE IN A LIST
    if not isinstance(mjd, list):
        mjdList = [str(mjd)]
    else:
        mjdList = mjd

    if not isinstance(objectId, list):
        objectList = [objectId]
    else:
        objectList = objectId

    ephem = settings["path to ephem binary"]
    home = expanduser("~")

    results = []
    cmdList = []
    for o in objectList:
        for m in mjdList:
            if not isinstance(o, int) and "'" in o:
                cmd = """%(ephem)s %(obscode)s %(m)s "%(o)s" """ % locals()
            else:
                cmd = """%(ephem)s %(obscode)s %(m)s '%(o)s'""" % locals()

            if astorbPath:
                cmd += " '%(astorbPath)s'" % locals()

            cmdList.append([cmd, o])

    # DEFINE AN INPUT ARRAY
    results = fmultiprocess(log=log, function=_generate_one_ephemeris,
                            inputArray=cmdList)

    if verbose == True:
        order = ["object_name", "mjd", "ra_deg", "dec_deg", "apparent_mag", "observer_distance", "heliocentric_distance",
                 "phase_angle",  "obscode", "sun_obs_target_angle", "galactic_latitude", "ra_arcsec_per_hour", "dec_arcsec_per_hour"]
    else:
        order = ["object_name", "mjd", "ra_deg", "dec_deg", "apparent_mag", "observer_distance", "heliocentric_distance",
                 "phase_angle"]

    # ORDER THE RESULTS
    resultList = []
    for r in results:
        if not r:
            continue

        orderDict = collections.OrderedDict({})
        for i in order:
            orderDict[i] = r[i]

        resultList.append(orderDict)

    log.info('completed the ``orbfit_ephemeris`` function')
    return resultList

    # xt-class-method

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


def orbfit_ephemeris(
        log,
        objectId,
        mjd,
        settings,
        verbose=False):
    """Given a known solar-system object ID (human-readable name or MPC number but *NOT* an MPC packed format) or list of names and one or more specific epochs, return the calculated ephemerides 

    **Key Arguments:**
        - ``log`` -- logger
        - ``objectId`` -- human-readable name, MPC number or solar-system object name, or list of names
        - ``mjd`` -- a single MJD, or a list MJDs to generate an ephemeris for
        - ``settings`` -- the settings dictionary for rockfinder
        - ``verbose`` -- return extra information with each ephemeris

    **Return:**
        - ``resultList`` -- a list of ordered dictionaries containing the returned ephemerides

    **Usage:**

        To generate a an ephemeris for a single epoch run:

        .. code-block:: python 

            from rockfinder import orbfit_ephemeris
            eph = orbfit_ephemeris(
                log=log,
                objectId=1,
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

    # CHECK ASTORB IN CONFIG DIR
    exists = os.path.exists(
        "%(home)s/.config/rockfinder/astorb.dat" % locals())
    if not exists:
        log.warning(
            'Please make sure you have an up-to-date astorb.dat orbital elements file in `"%(home)s/.config/rockfinder`' % locals())
        sys.exit(0)

    results = []
    for o in objectList:
        for m in mjdList:

            cmd = """%(ephem)s T05 %(m)s '%(o)s'""" % locals()
            print cmd
            p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True,
                      cwd="%(home)s/.config/rockfinder" % locals())
            stdout, stderr = p.communicate()
            log.debug('output: %(stdout)s' % locals())
            if len(stderr):
                log.error(stderr)
                continue
            elif "!!WARNING! WARNING! WARNING! WARNING!!" in stdout:
                log.error(stdout)
                continue

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
                row = dict(zip(keys, values))
                row["object_name"] = str(o)
                results.append(row)

    if verbose == True:
        order = ["mjd", "ra_deg", "dec_deg", "apparent_mag", "observer_distance", "heliocentric_distance", "sun_obs_target_angle",
                 "phase_angle", "galactic_latitude", "ra_arcsec_per_hour", "dec_arcsec_per_hour", "object_name", "obscode"]
    else:
        order = ["mjd", "ra_deg", "dec_deg", "apparent_mag", "observer_distance", "heliocentric_distance", "sun_obs_target_angle",
                 "phase_angle", "galactic_latitude", "ra_arcsec_per_hour", "dec_arcsec_per_hour", "object_name", "obscode"]

    # ORDER THE RESULTS
    resultList = []
    for r in results:

        orderDict = collections.OrderedDict({})
        for i in order:
            orderDict[i] = r[i]

        resultList.append(orderDict)

    log.info('completed the ``orbfit_ephemeris`` function')
    return resultList

    # xt-class-method

#!/usr/local/bin/python
# encoding: utf-8
"""
*Given a known solar-system object ID (human-readable name, MPC number or MPC packed format) and one or more specific epochs, return the calculated ephemerides*

:Author:
    David Young

:Date Created:
    August  1, 2017
"""
################# GLOBAL IMPORTS ####################
import sys
import os
os.environ['TERM'] = 'vt100'
from fundamentals import tools
from fundamentals.renderer import list_of_dictionaries
import grequests
import re
import collections
import copy


def whereami(
        log,
        objectId,
        mjd,
        verbose=False):
    """Given a known solar-system object ID (human-readable name, MPC number or MPC packed format) and one or more specific epochs, return the calculated ephemerides 

    **Key Arguments:**
        - ``log`` -- logger
        - ``objectId`` -- human-readable name, MPC number or MPC packed format id of the solar-system object
        - ``mjd`` -- a single MJD, or a list of up to 10,000 MJDs to generate an ephemeris for
        - ``verbose`` -- return extra information with each ephemeris

    **Return:**
        - ``resultList`` -- a list of ordered dictionaries containing the returned ephemerides

    **Usage:**

        To generate a an ephemeris for a single epoch run:

        .. code-block:: python 

            from rockfinder import whereami
            eph = whereami(
                log=log,
                objectId=1,
                mjd=57916.,
            )

        or to generate an ephemeris for multiple epochs:

        .. code-block:: python 

            from rockfinder import whereami
            eph = whereami(
                log=log,
                objectId="ceres",
                mjd=[57916.1,57917.234,57956.34523]
                verbose=True
            )

        Note by passing `verbose=True` the essential ephemeris data is supplimented with some extra data

        It's also possible to pass in an array of object IDs:

        .. code-block:: python 

            from rockfinder import whereami
            eph = whereami(
                log=log,
                objectId=[1,5,03547,"Shikoku","K10B11A"],
                mjd=[57916.1,57917.234,57956.34523]
            )
    """
    log.info('starting the ``whereami`` function')

    # MAKE SURE MJDs ARE IN A LIST
    if not isinstance(mjd, list):
        mjd = [str(mjd)]

    mjd = (" ").join(map(str, mjd))

    if not isinstance(objectId, list):
        objectList = [objectId]
    else:
        objectList = objectId

    keys = ["jd", "solar_presence", "lunar_presence",  "ra_deg", "dec_deg", "ra_arcsec_per_hour", "dec_arcsec_per_hour",  "apparent_mag", "surface_brightness", "heliocentric_distance", "heliocentric_motion", "observer_distance", "observer_motion",
            "sun_obs_target_angle", "apparent_motion_relative_to_sun",  "sun_target_obs_angle", "ra_3sig_error", "dec_3sig_error", "true_anomaly_angle", "phase_angle", "phase_angle_bisector_long", "phase_angle_bisector_lat"]
    if verbose == True:
        order = ["requestId", "objectId", "mjd", "ra_deg", "dec_deg", "ra_3sig_error", "dec_3sig_error", "ra_arcsec_per_hour",  "dec_arcsec_per_hour", "apparent_mag",  "heliocentric_distance", "heliocentric_motion", "observer_distance", "observer_motion", "phase_angle", "true_anomaly_angle", "surface_brightness",
                 "sun_obs_target_angle",  "sun_target_obs_angle", "apparent_motion_relative_to_sun", "phase_angle_bisector_long", "phase_angle_bisector_lat"]
    else:
        order = ["requestId", "objectId", "mjd", "ra_deg", "dec_deg", "ra_3sig_error", "dec_3sig_error", "ra_arcsec_per_hour",
                 "dec_arcsec_per_hour", "apparent_mag",  "heliocentric_distance", "observer_distance", "phase_angle"]

    params = {
        "COMMAND": "",
        "OBJ_DATA": "'NO'",
        "MAKE_EPHEM": "'YES'",
        "TABLE_TYPE": "'OBS'",
        "CENTER": "'T05'",
        "TLIST": mjd,
        "QUANTITIES": "'1,3,9,19,20,23,24,36,41,43'",
        "REF_SYSTEM": "'J2000'",
        "CAL_FORMAT": "'JD'",
        "ANG_FORMAT": "'DEG'",
        "APPARENT": "'REFRACTED'",
        "TIME_DIGITS": "'FRACSEC'",
        "TIME_ZONE": "'+00:00'",
        "RANGE_UNITS": "'AU'",
        "SUPPRESS_RANGE_RATE": "'NO'",
        "EXTRA_PREC": "'YES'",
        "CSV_FORMAT": "'YES'",
        "batch": "1",
    }

    resultList = []
    paramList = []
    for objectId in objectList:
        requestId = objectId
        # FIX THE COMMAND FOR NUMBERED OBJECTS
        try:
            thisId = int(objectId)
            objectId = "%(thisId)s;" % locals()
        except Exception as e:
            pass

        theseparams = copy.deepcopy(params)
        theseparams["COMMAND"] = objectId
        paramList.append(theseparams)

    rs = [grequests.get("https://ssd.jpl.nasa.gov/horizons_batch.cgi", params=p)
          for p in paramList]
    returns = grequests.map(rs, size=1)

    for result, requestId in zip(returns, objectList):
        r = result.content

        match = re.search(
            r'Target body name:\s(.*?)\{',
            r,
            flags=re.S  # re.S
        )

        if not match:
            log.warning(
                "Horizons could not find a match for `%(requestId)s`" % locals())
            print result.url
            continue

        horizonsId = match.group(1).replace("(", "").replace(")", "").strip()

        match = re.search(
            r'\$\$SOE\n(.*?)\n\$\$EOE',
            r,
            flags=re.S  # re.S
        )

        lines = match.group(1).split("\n")
        for line in lines:
            vals = line.split(",")
            objectDict = {}
            for k, v in zip(keys, vals):
                v = v.strip().replace("/", "")
                try:
                    v = float(v)
                except:
                    pass
                objectDict[k] = v

            objectDict["mjd"] = objectDict["jd"] - 2400000.5
            objectDict["objectId"] = horizonsId
            objectDict["requestId"] = requestId

            orderDict = collections.OrderedDict({})
            for i in order:
                orderDict[i] = objectDict[i]

            resultList.append(orderDict)

    log.info('completed the ``whereami`` function')
    return resultList

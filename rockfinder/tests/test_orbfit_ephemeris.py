import os
import nose2
import shutil
import unittest
import yaml
from rockfinder import orbfit_ephemeris, cl_utils
from rockfinder.utKit import utKit

from fundamentals import tools

su = tools(
    arguments={"settingsFile": None},
    docString=__doc__,
    logLevel="DEBUG",
    options_first=False,
    projectName="rockfinder"
)
arguments, settings, log, dbConn = su.setup()

# # load settings
# stream = file(
#     "/Users/Dave/.config/rockfinder/rockfinder.yaml", 'r')
# settings = yaml.load(stream)
# stream.close()

# SETUP AND TEARDOWN FIXTURE FUNCTIONS FOR THE ENTIRE MODULE
moduleDirectory = os.path.dirname(__file__)
utKit = utKit(moduleDirectory)
log, dbConn, pathToInputDir, pathToOutputDir = utKit.setupModule()
utKit.tearDownModule()

# load settings
stream = file(
    pathToInputDir + "/example_settings.yaml", 'r')
settings = yaml.load(stream)
stream.close()

import shutil
try:
    shutil.rmtree(pathToOutputDir)
except:
    pass
# COPY INPUT TO OUTPUT DIR
shutil.copytree(pathToInputDir, pathToOutputDir)

# Recursively create missing directories
if not os.path.exists(pathToOutputDir):
    os.makedirs(pathToOutputDir)

# xt-setup-unit-testing-files-and-folders


class test_orbfit_ephemeris(unittest.TestCase):

    def test_orbfit_ephemeris_function(self):

        from rockfinder import orbfit_ephemeris
        this = orbfit_ephemeris(
            log=log,
            settings=settings,
            objectId=1,
            mjd=57916.,
            verbose=True
        )
        print this

        from rockfinder import orbfit_ephemeris
        this = orbfit_ephemeris(
            log=log,
            settings=settings,
            objectId=1,
            mjd=[57916., 57916.1, 57916.2]
        )
        print this

    def test_orbfit_ephemeris_w_custom_oe_file_function(self):

        from rockfinder import orbfit_ephemeris
        this = orbfit_ephemeris(
            log=log,
            settings=settings,
            objectId=1,
            mjd=57916.,
            verbose=True,
            astorbPath=pathToInputDir + "/astorb-partial.dat"
        )
        print this

        from rockfinder import orbfit_ephemeris
        this = orbfit_ephemeris(
            log=log,
            settings=settings,
            objectId=1,
            mjd=[57916., 57916.1, 57916.2],
            astorbPath=pathToInputDir + "/astorb-partial.dat"
        )
        print this

    def test_orbfit_ephemeris_function02(self):

        from rockfinder import orbfit_ephemeris
        this = orbfit_ephemeris(
            log=log,
            settings=settings,
            objectId=range(1500),
            mjd=57916.,
            verbose=True
        )
        print this

    def test_orbfit_ephemeris_function_exception(self):

        from rockfinder import orbfit_ephemeris
        try:
            this = orbfit_ephemeris(
                log=log,
                settings=settings,
                fakeKey="break the code"
            )
            this.get()
            assert False
        except Exception, e:
            assert True
            print str(e)

        # x-print-testpage-for-pessto-marshall-web-object

    # x-class-to-test-named-worker-function

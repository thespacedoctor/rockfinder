import os
import nose2
import shutil
import unittest
import yaml
from rockfinder import jpl_horizons_ephemeris, cl_utils
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
# stream = file(
#     pathToInputDir + "/example_settings.yaml", 'r')
# settings = yaml.load(stream)
# stream.close()

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


class test_jpl_horizons_ephemeris(unittest.TestCase):

    def test_jpl_horizons_ephemeris_function(self):

        from rockfinder import jpl_horizons_ephemeris
        this = jpl_horizons_ephemeris(
            log=log,
            objectId=1,
            mjd=57916.,
            verbose=True
        )
        print this

        from rockfinder import jpl_horizons_ephemeris
        this = jpl_horizons_ephemeris(
            log=log,
            objectId=1,
            mjd=[57916., 57916.1, 57916.2]
        )
        print this

    def test_jpl_horizons_ephemeris_function02(self):

        from rockfinder import jpl_horizons_ephemeris
        this = jpl_horizons_ephemeris(
            log=log,
            objectId=[1, 2, 3, 4, 5],
            mjd=57916.,
            verbose=True
        )
        print this

        # from rockfinder import jpl_horizons_ephemeris
        # this = jpl_horizons_ephemeris(
        #     log=log,
        #     objectId=1,
        #     mjd=[57916., 57916.1, 57916.2]
        # )
        # print this

    def test_jpl_horizons_ephemeris_function_exception(self):

        from rockfinder import jpl_horizons_ephemeris
        try:
            this = jpl_horizons_ephemeris(
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

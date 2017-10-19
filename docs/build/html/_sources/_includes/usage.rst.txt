Command-Line Usage
==================

.. code-block:: bash 
   
    
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
    

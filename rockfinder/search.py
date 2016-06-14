#!/usr/local/bin/python
# encoding: utf-8
"""
*Search the MPChecker for known objects at the sky-position and epoch*

:Author:
    David Young

:Date Created:
    March  2, 2016

.. todo::
    
    @review: when complete pull all general functions and classes into dryxPython
"""
################# GLOBAL IMPORTS ####################
import sys
import os
os.environ['TERM'] = 'vt100'
from fundamentals import tools


class search():
    """
    *The worker class for the search module*

    **Key Arguments:**
        - ``log`` -- logger
        - ``settings`` -- the settings dictionary
        - ``ra`` -- ra of the object in question
        - ``dec`` -- dec of the object in question

    .. todo::

        - @review: when complete, clean search class
        - @review: when complete add logging
        - @review: when complete, decide whether to abstract class to another module
    """
    # Initialisation
    # 1. @flagged: what are the unique attrributes for each object? Add them
    # to __init__

    def __init__(
            self,
            log,
            settings=False,

    ):
        self.log = log
        log.debug("instansiating a new 'search' object")
        self.settings = settings
        self.ra = ra
        self.dec = dec
        # xt-self-arg-tmpx

        # 2. @flagged: what are the default attrributes each object could have? Add them to variable attribute set here
        # Variable Data Atrributes

        # 3. @flagged: what variable attrributes need overriden in any baseclass(es) used
        # Override Variable Data Atrributes

        # Initial Actions

        return None

    # 4. @flagged: what actions does each object have to be able to perform? Add them here
    # Method Attributes
    def get(self):
        """
        *get the search object*

        **Return:**
            - ``search``

        .. todo::

            - @review: when complete, clean get method
            - @review: when complete add logging
        """
        self.log.info('starting the ``get`` method')

        search = None

        self.log.info('completed the ``get`` method')
        return search

    def build_url_and_return_content(
            self):
        """
        *build url and return content*

        **Key Arguments:**
            # -

        **Return:**
            - None

        .. todo::

            - @review: when complete, clean build_url_and_return_content method
            - @review: when complete add logging
        """
        self.log.info('starting the ``build_url_and_return_content`` method')
        import requests
        try:
            response = requests.get(
                url="http://www.minorplanetcenter.net/cgi-bin/mpcheck.cgi",
                params={
                    "year": "2016",
                    "month": "03",
                    "day": "02.68",
                    "which": "pos",
                    "ra": "14 10 48.46",
                    "decl": "-12 37 08.4",
                    "TextArea": " ",
                    "radius": "15",
                    "limit": "20.0",
                    "oc": "500",
                    "sort": "d",
                    "mot": "h",
                    "tmot": "s",
                    "pdes": "u",
                    "needed": "f",
                    "ps": "n",
                    "type": "p",
                },
            )
            print('Response HTTP Status Code: {status_code}'.format(
                status_code=response.status_code))
            print('Response HTTP Response Body: {content}'.format(
                content=response.content))
        except requests.exceptions.RequestException:
            print('HTTP Request failed')

        self.log.info('completed the ``build_url_and_return_content`` method')
        return None

    # use the tab-trigger below for new method
    # xt-class-method

    # 5. @flagged: what actions of the base class(es) need ammending? ammend them here
    # Override Method Attributes
    # method-override-tmpx

pyflapjack
==========

.. image:: https://travis-ci.org/tryagainconcepts/pyflapjack.svg?branch=master
    :target: https://travis-ci.org/tryagainconcepts/pyflapjack

Flapjack Python API. Supports Flapjack 1.x


Features
--------
* Send events to flapjack Redis
* Flapjack JSONAPI

Known issues
------------
* Flapjack API can return success (204) when it should report fail when
  removing links with PATCH that don't exist.

pyflapjack
==========

.. image:: https://travis-ci.org/tryagainconcepts/pyflapjack.svg?branch=master
    :target: https://travis-ci.org/tryagainconcepts/pyflapjack

Flapjack Python API. Supports Flapjack 1.x


Features
--------
* Send events to flapjack Redis
* Flapjack JSONAPI

Known bugs
----------
* Removing contacts' links with PATCH doesn't work. This is a bug with
  flapjack. Upon receiving such a request, flapjack returns a 204, but the
  contact resource remains unchanged.


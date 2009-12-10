.. app documentation master file, created by
   sphinx-quickstart on Wed Oct 21 13:18:22 2009.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Django Object Permissions' documentation!
====================================================

Django Object Permissions is a way to add a custom set of user-object or group-object permissions. It does not replace Django's built-in permissions. Instead it augments them by adding additional ways to manage access to specific objects.

It uses an efficient method of storing permissions; it requires only one row per user-object combination, regardless of the number of permissions granted.

Goals:

* Have an easy way to set read/write/owner permissions on an object or row
* Easy to discover if a given user has a level of permission
* Customizable permissions
* Admin viewing/editing integration

Contents:

.. toctree::
   :maxdepth: 2
   :glob:
   
   getting_started

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. _flow:

Flow - definition and guide
===========================

.. contents:: :local:

Flow object deals with scenario, which is represented as some abstract
container (in most cases list or graph) with executable objects aka
"stages". All you can do with an instance of Flow object is specify some
exact scenario and run it by calling flow.run() method, which is
responsible for going through stages of the scenario and executing them.


Abstract Flow
-------------

.. autoclass:: fuel_ci.flow.base.AbstractFlow

Base (Linear) Flow
------------------

.. autoclass:: fuel_ci.flow.base.BaseFlow
    :special-members: __init__

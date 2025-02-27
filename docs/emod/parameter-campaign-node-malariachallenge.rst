================
MalariaChallenge
================

The **MalariaChallenge** intervention class is a node-level intervention similar to
:doc:`parameter-campaign-node-outbreak`. However, instead of distributing infections, it distributes
malaria challenges by either tracking numbers of sporozoites or infectious mosquito bites.

.. include:: ../reuse/warning-case.txt

.. include:: ../reuse/campaign-example-intro.txt

.. csv-table::
    :header: Parameter, Data type, Minimum, Maximum, Default, Description, Example
    :widths: 10, 5, 5, 5, 5, 20, 5
    :file: ../csv/campaign-malariachallenge.csv

.. literalinclude:: ../json/campaign-malariachallenge.json
   :language: json
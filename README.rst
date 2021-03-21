Introduction
------------

NOTE: This is an `OASIS TC Open
Repository <https://www.oasis-open.org/resources/open-
repositories/>`_.
See the `Governance`_ section below for more information.

This repository contains commonly used STIX 2.1 objects that can be used by STIX content producers and consumers.

Using these objects, instead of each producer creating their own, will reduce the number of duplicates shared and enable producers to share information using just the identifier reference of these common objects.  Consumers can incorporate these object instances locally in order to resolve those identifiers.

The following describes the contents of the repository and how to query and manipulate it. 

STIX 2.1 is expressed using JSON, which can be easily consumed using Python or other programming languages. If you are using Python, the `python-stix2 <https://github.com/oasis-open/cti-python-stix2>`_ library can help you work with the content as shown in the examples below.  

What type of STIX content can be found in this repository
---------------------------------------------------------

The current objects were created via a script found at `generate_common_objects.py <generate_common_objects.py>`_.

Location objects
~~~~~~~~~~~~~~~~

- All countries (compiled from Python pycountry package)
- All US States (constant in script)
- All Canadian Provinces (constant in script)
- All regions in `region-ov <https://docs.oasis-open.org/cti/stix/v2.1/cs02/stix-v2.1-cs02.html#_i1sw27qw1v0s>`_

Identity objects
~~~~~~~~~~~~~~~~

-    One for the object creator (currently `OASIS <identity/identity--8ce3f695-d5a4-4dc8-9e93-a65af453a31a.json>`_)
-    All sectors in `industry-sector-ov <https://docs.oasis-open.org/cti/stix/v2.1/cs02/stix-v2.1-cs02.html#_oogrswk3onck>`_

Vulnerability objects
~~~~~~~~~~~~~~~~~~~~~

-    All “published” CVEs (updated daily).  As of 3/11/2021, there are approximately 150,000 objects.

Using Python and STIX 2.1
-------------------------

In this section, we will describe how to query and manipulate STIX that has been retrieved from this repository using Python. Other programming languages can also be used.

A Python library has been created for using and creating STIX 2.1 content.
This library abstracts storage and transport details so that the same code can be used to interact with data locally on the filesystem or in memory, or remotely via `TAXII <https://oasis-open.github.io/cti-documentation/taxii/intro>`_.
The source code, installation instructions, and basic documentation for the library can be found `here <https://github.com/oasis-open/cti-python-stix2>`_.
There is a more thorough `API documentation <http://stix2.readthedocs.io/en/latest/overview.html>`_ as well.

*There is currently no TAXII server set up to distribute the content in this repository.*

Python Library
~~~~~~~~~~~~~~

To begin querying STIX 2.1 data, you must first have a `DataSource <http://stix2.readthedocs.io/en/latest/guide/datastore.html>`_.
For these examples, we will simply use a `FileSystemSource <http://stix2.readthedocs.io/en/latest/guide/filesystem.html>`_.

*The repository contents must first be cloned or downloaded from GitHub.*

Creating a DataStore
~~~~~~~~~~~~~~~~~~~~

Once the stix2 Python library is installed and the content is acquired, we need to open the DataStore for querying:

.. code-block:: python

    from stix2 import FileSystemSource
    fs = FileSystemSource(<the directory containing the contents of the repository>)



*For a production system, a DataStore to process objects from Github that integrates with your implemenation is suggested.*

Querying
~~~~~~~~

To perform a query, we must define a `Filter <http://stix2.readthedocs.io/en/latest/guide/datastore.html#Filters>`_. As of this writing, a filter must, at a minimum, specify object `id`'s or an object `type`.  The following filter can be used to retrieve all CVE Vulnerabilities:

.. code-block:: python

    from stix2 import Filter
    filt = Filter('type', '=', 'vulnerability')


Once this filter is defined, you can pass it to the DataSource `query` function in order to actually query the data:

.. code-block:: python

    vulnerabilities = fs.query([filt])

*This query will process approximately 150,000 objects, which takes about 2 minutes.*

Notice that the `query` function takes a **list** of filters.  These filters are logically AND'd together during the query. 

*For the remaining examples, these imports and the FileSystemStore initialization will be omitted.*

Get the Location object for a country
*************************************

In this example, the country name must be passed into the function. Here we query for the Location object for France.

.. code-block:: python

    def get_location_for_country(store, country_name):
        filt = [
            Filter('type', '=', 'location'),
            Filter('name', '=', country_name),
        ]
        return store.query(filt)

    get_location_for_country(fs, "France")


Get the latest Vulnerability objects
************************************

Here we query for all of Vulnerability objects added after midnight on 2/28/2021.

.. code-block:: python

    def get_new_vulnerabilties(store, added_after_date):
        filt = [
            Filter('type', '=', 'vulnerability'),
            Filter("created", ">=", added_after_date)
        ]
        return store.query(filt)

    get_new_vulnerabilties(fs, "2021-02-28T00:00:00.000Z")

Governance
----------

This GitHub public repository `cti-stix-common-objects <https://github.com/oasis-open/cti-stix-common-objects>`_ was created at the request of the `OASIS Cyber Threat Intelligence (CTI) TC <https://www.oasis-open.org/committees/cti/>`_ as an `OASIS TC Open Repository <https://www.oasis-open.org/resources/open-repositories/>`_ to support development of open source resources related to Technical Committee work.

While this TC Open Repository remains associated with the sponsor TC, its development priorities, leadership, intellectual property terms, participation rules, and other matters of governance are separate and distinct from the OASIS TC Process and related policies.

All contributions made to this TC Open Repository are subject to open source license terms expressed in `BSD-3-Clause License <https://www-legacy.oasis-open.org/sites/www.oasis-open.org/files/BSD-3-Clause.txt>`_. That license was selected as the declared `Applicable License <https://www.oasis-open.org/resources/open-repositories/licenses>`_ when the TC voted to create this Open Repository.

As documented in `Public Participation Invited <https://github.com/oasis-open/cti-stix-common-objects/blob/master/CONTRIBUTING.md#public-participation-invited>`_, contributions to this TC Open Repository are invited from all parties, whether affiliated with OASIS or not. Participants must have a GitHub account, but no fees or OASIS membership obligations are required.  Participation is expected to be consistent with the `OASIS TC Open Repository Guidelines and Procedures <https://www.oasis-open.org/policies-guidelines/open-repositories>`_, the open source `LICENSE.md <LICENSE.md>`_ designated for this particular repository, and the requirement for an `Individual Contributor License Agreement <https://cla-assistant.io/oasis-open/Open-Repo-admin>`_ that governs intellectual property.

Maintainers
~~~~~~~~~~~

The current maintainers of this TC Open Repository are: 

* `Rich Piazza <mailto:rpiazza@mitre.org>`_, GitHub ID: rpiazza, `The MITRE Corporation <https://www.mitre.org/>`_
* `Chris Lenk <mailto:clenk@mitre.org>`_, GitHub ID: clenk, `The MITRE Corporation <https://www.mitre.org/>`_

TC Open Repository `maintainers <https://www.oasis-open.org/resources/open-repositories/maintainers-guide>`_ are responsible for oversight of this project's community development activities, including evaluation of GitHub `pull requests <https://github.com/oasis-open/cti-stix-common-objects/blob/master/CONTRIBUTING.md#fork-and-pull-collaboration-model>`_ and `preserving <https://www.oasis-open.org/policies-guidelines/open-repositories#repositoryManagement>`_ open source principles of openness and fairness. Maintainers are recognized and trusted experts who serve to implement community goals and consensus design preferences.

Initially, the TC members designated one or more persons to serve as Maintainer(s); subsequently, participating community members may select additional or substitute Maintainers by `consensus agreement <https://www.oasis-open.org/resources/open-repositories/maintainers-guide#additionalMaintainers>`_.

About OASIS TC Open Repositories
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* `TC Open Repositories: Overview and Resources <https://www.oasis-open.org/resources/open-repositories/>`_
* `Frequently Asked Questions <https://www.oasis-open.org/resources/open-repositories/faq>`_
* `Open Source Licenses <https://www.oasis-open.org/resources/open-repositories/licenses>`_
* `Maintainers' Guidelines and Agreement <https://www.oasis-open.org/resources/open-repositories/maintainers-guide>`_

Feedback
~~~~~~~~

Questions or comments about this TC Open Repository's activities should be composed as GitHub issues or comments. If use of an issue/comment is not possible or appropriate, questions may be directed by email to the Maintainer(s) listed above. Please send general questions about TC Open Repository participation to OASIS Staff at `repository-admin@oasis-open.org <mailto:repository-admin@oasis-open.org>`_ and any specific CLA-related questions to `repository-cla@oasis-open.org <mailto:repository-cla@oasis-open.org>`_.

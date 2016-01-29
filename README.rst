django-alexa
============

.. image:: https://badge.fury.io/py/py-alexa.svg
    :target: https://badge.fury.io/py/py-alexa
    :alt: Current Version

.. image:: https://travis-ci.org/rocktavious/py-alexa.svg?branch=master
    :target: https://travis-ci.org/rocktavious/py-alexa
    :alt: Build Status

.. image:: https://coveralls.io/repos/rocktavious/py-alexa/badge.svg?branch=master&service=github
  :target: https://coveralls.io/github/rocktavious/py-alexa?branch=master

.. image:: https://requires.io/github/rocktavious/py-alexa/requirements.svg?branch=master
     :target: https://requires.io/github/rocktavious/py-alexa/requirements/?branch=master
     :alt: Requirements Status

Tools for writing Amazon Alexa Skills Kit integration for other frameworks

.. code-block:: bash

    $ pip install py-alexa

You now can leverage certain api tools to help build your alexa integrations
for other frameworks.  The current best example is the library
https://github.com/rocktavious/django-alexa

Inform thhe end user to set environment variables to configure the validation needs
ALEXA_APP_IDS_* = Your Amazon Alexa App ID

response_builder.py
-------------------

This contains a class that can be used by end users to generate proper response
data.  This class is completely self contained and should just be exposed to the
end user of the framework your writing

intents_schema.py
-----------------

This contains the logic for building up the intents data and has some utility
methods for registering and retreving the data in certain formats.

The main use case for this class is to utilize this class for performing the
intent routing where it will call the desired intent's method and give you its
response data, which you then need to shuffle through your framework and finally
get it put out as a valid HTTP Response

Example from django-alexa

.. code-block: python

    from py_alexa.api import IntentsSchema

    data = IntentsSchema.route(session, app, intent_name, intent_kwargs)
    return Response(data=data, status=HTTP_200_OK)

The end user uses the decorator provided by this class to register an intent
with this class

Example from django-alexa

.. code-block: python

    from py_alexa.api import intent, ResponseBuilder

    @intent
    def HelpIntent(session):
        """
        Default Help Intent
        ---
        help
        info
        information
        """
        return ResponseBuilder.create_response(message="No help was configured!")

You can also use this class to generate data for the alexa skill configuration
by utilizing the functions provided on the class.  You can hook this up to your
frameworks command channel

Example from django-alexa

.. code-block: python

    data = IntentsSchema.generate_schema(app=app)
    self.stdout.write(json.dumps(data, indent=4, sort_keys=True) + "\n")

fields.py
---------

The py-alexa lib use classes to determine valid slot types, so the classes in
this file need to be mixed in with the kind of field validation your framework
uses.

Example from django-alexa (using django-rest-framework)

.. code-block:: python

    from rest_framework import serializers
    from py_alexa.api import fields

    class AmazonCustom(fields.AmazonCustom, serializers.ChoiceField):

        def get_slot_name(self):
            return self.label

validation.py
-------------

This provides a bunch of utility functions to perform alexa skills kit specific
validation.  There is a environment variable that can be set that will enable/disable
the request validation function.  ALEXA_REQUEST_VERIFICATON
This allow end users to opt into request verification, which is mainly tied to
debugging or testing their endpoint.

Example from django-alexa

.. code-block:: python

    from rest_framework import serializers
    from py_alexa.api import validate_app_ids, validate_char_limit

    class ASKApplicationSerializer(serializers.Serializer):
        applicationId = serializers.CharField(validators=[validate_app_ids])

Contributing
------------

- The master branch is meant to be stable. I usually work on unstable stuff on a personal branch.
- Fork the master branch ( https://github.com/rocktavious/py-alexa/fork )
- Create your branch (git checkout -b my-branch)
- Commit your changes (git commit -am 'added fixes for something')
- Push to the branch (git push origin my-branch)
- Create a new Pull Request (Travis CI will test your changes)
- And you're done!

- Features, Bug fixes, bug reports and new documentation are all appreciated!
- See the github issues page for outstanding things that could be worked on.


Credits: Kyle Rockman 2016

import json
import unittest2 as unittest
from py_alexa.api import IntentsSchema, intent, ResponseBuilder

@intent
def TestIntent(session):
    """
    ---
    test
    """
    return ResponseBuilder.create_response(message="Hello")


class TestIntentsSchema(unittest.TestCase):

    def test_get_intent(self):
        self.assertEquals((TestIntent, None),
                          IntentsSchema.get_intent("base", "TestIntent"))

    def test_route(self):
        data = {
            'version': '',
            'response': {
                'outputSpeech': {
                    'text': 'Hello',
                    'type': 'PlainText'
                },
                'shouldEndSession': True
            },
            'sessionAttributes': {}
        }
        self.assertEquals(data,
                          IntentsSchema.route({}, 'base', 'TestIntent', {}))

    def test_register(self):
        pass

    def test_generate_schema(self):
        data = {
            'intents': [{
                'intent': 'TestIntent', 'slots': []
            }]
        }
        self.assertEqual(data,
                         IntentsSchema.generate_schema())

    def test_generate_utterances(self):
        data = ['TestIntent test']
        self.assertEqual(data,
                         IntentsSchema.generate_utterances())

    def test_generate_custom_slots(self):
        data = []
        self.assertEqual(data,
                         IntentsSchema.generate_custom_slots())
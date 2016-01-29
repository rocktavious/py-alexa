import json
import unittest2 as unittest
from py_alexa.api import ResponseBuilder


class TestResponseBuilder(unittest.TestCase):

    def test_user_facing_create_response(self):
        data = {
            'version': '',
            'response': {
                'outputSpeech': {
                    'text': 'Testing Reprompt',
                    'type': 'PlainText'
                },
                'shouldEndSession': True,
                'reprompt': {
                    'outputSpeech': {
                        'text': 'Reprompt',
                        'type': 'PlainText'
                    }
                },
                'card': {
                    'content': 'Doc String',
                    'type': 'Simple',
                    'title': 'Hello World'
                }
                },
            'sessionAttributes': {
                'extra_arg': 1
            }
        }
        response = ResponseBuilder.create_response(message="Testing",
                                                   reprompt="Reprompt",
                                                   title="Hello World",
                                                   content="""Doc String""",
                                                   end_session=True,
                                                   extra_arg=1)
        self.assertEquals(data, response)

    def test_user_facing_create_response_ssml(self):
        data = {
            'version': '',
            'response': {
                'outputSpeech': {
                    'ssml': '<speak>Testing Reprompt</speak>',
                    'type': 'SSML'
                },
                'shouldEndSession': False,
                'reprompt': {
                    'outputSpeech': {
                        'ssml': '<speak>Reprompt</speak>',
                        'type': 'SSML'
                    }
                },
                'card': {
                    'content': 'Doc String',
                    'type': 'LinkedAccount',
                    'title': 'Hello World'
                }
            },
            'sessionAttributes': {
                'extra_arg': 1
            }
        }
        response = ResponseBuilder.create_response(message="Testing",
                                                   message_is_ssml=True,
                                                   reprompt="Reprompt",
                                                   reprompt_is_ssml=True,
                                                   title="Hello World",
                                                   content="""Doc String""",
                                                   card_type="LinkedAccount",
                                                   end_session=False,
                                                   extra_arg=1)
        self.assertEquals(data, response)

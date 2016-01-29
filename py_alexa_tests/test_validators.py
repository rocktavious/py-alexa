import json
import pytest
from datetime import datetime
import unittest2 as unittest
from py_alexa.api import validate_app_ids, validate_char_limit, validate_reponse_limit, validate_alexa_request, InternalError, ResponseBuilder


class TestValidation(unittest.TestCase):

    def test_validate_app_ids(self):
        self.assertFalse(validate_app_ids('qazwsxedc'))
        self.assertRaises(InternalError, validate_app_ids, 'pl,okm')

    def test_validate_char_limit(self):
        data = '*' * 8001
        data = dict({"Test": data})
        self.assertFalse(validate_char_limit(dict({"Test":"Test"})))
        self.assertRaises(InternalError, validate_char_limit, data)

    def test_validate_reponse_limit(self):
        valid_response = json.dumps(ResponseBuilder.create_response(message="Testing, One, Two, Three!"))
        invalid_response = json.dumps(ResponseBuilder.create_response(message="*" * 192000))
        self.assertFalse(validate_reponse_limit(valid_response))
        self.assertRaises(InternalError, validate_reponse_limit, invalid_response)

    def test_validate_alexa_request(self):
        # I cannot figure out how to get a good request to go though
        pass

    def test_validate_alexa_request_bad_cert_chain(self):
        example_request_body = json.dumps({
            "version": "1.0",
            "session": {
                "new": True,
                "sessionId": "session1234",
                "application": {
                    "applicationId": "amzn1.echo-sdk-ams.app.1234"
                    },
                "attributes": {},
                "user": {
                    "userId": "amzn1.echo-sdk-account.1234"
                }
                },
            "request": {
                "type": "LaunchRequest",
                "requestId": "request5678",
                "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
            }
        })
        example_request_headers = {
            "HTTP_SIGNATURECERTCHAINURL": "https://notamazon.com/echo.api/echo-api-cert.pem",
            "HTTP_SIGNATURE": "1234567890"
        }
        self.assertRaises(InternalError,
                          validate_alexa_request,
                          example_request_headers,
                          example_request_body)

    def test_validate_alexa_request_bad_timestamp(self):
        example_request_body = json.dumps({
            "version": "1.0",
            "session": {
                "new": True,
                "sessionId": "session1234",
                "application": {
                    "applicationId": "amzn1.echo-sdk-ams.app.1234"
                    },
                "attributes": {},
                "user": {
                    "userId": "amzn1.echo-sdk-account.1234"
                }
                },
            "request": {
                "type": "LaunchRequest",
                "requestId": "request5678",
                "timestamp": '2016-01-29T19:09:13Z'
            }
        })
        example_request_headers = {
            "HTTP_SIGNATURECERTCHAINURL": "https://notamazon.com/echo.api/echo-api-cert.pem",
            "HTTP_SIGNATURE": "1234567890"
        }
        self.assertRaises(InternalError,
                          validate_alexa_request,
                          example_request_headers,
                          example_request_body)
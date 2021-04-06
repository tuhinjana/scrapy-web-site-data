import json
from unittest import TestCase
from unittest.mock import Mock, patch


# factory method that cranks out the Mocks
def mock_requests_factory(response_stub: str, status_code: int = 200):
    return Mock(**{
        'json.return_value': json.loads(response_stub),
        'text.return_value': response_stub,
        'status_code': status_code,
        'ok': status_code == 200
    })


def mock_requests_get(*args, **kwargs):
    if args[0].endswith('/history/'):
        return mock_requests_factory(mock_history_data)
    elif args[0].endswith('/latest/'):
        return mock_requests_factory(LIST_OF_WIDGETS)
    
    raise MockNotSupported


mock_history_data = '{"rates" : {"2021-02-10": {"GBP": 1.232, "RUB": 2.2323, "USD": 1.232}}, "base" : "EUR" }'

expected_data = [{'GBP': 1.232, 'RUB': 2.2323, 'USD': 1.232, 'date': '2021-02-10'}]


# exception class when an unknown URL is mocked
class MockNotSupported(Exception):
  pass


class ExchangeRateTestClass(TestCase):

    def test_main_method(self):
        with patch("main.requests.get") as mock_get:
            mock_get.side_effect = mock_requests_get
            import main
            test_result = main.fetch_history_exchange_data("2021-01-01", "2021-02-28")
            print(expected_data)
            self.assertEqual(expected_data, test_result)



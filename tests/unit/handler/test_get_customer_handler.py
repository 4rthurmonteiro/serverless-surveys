import pytest
import json
from tests.utils.dynamodb import mocked_table


class Context:
    pass


good_event = {
    'pathParameters': {
        'customer_id': '1'
    }
}


@pytest.fixture(scope='function')
def setup_table_item(dynamodb_table):
    table = mocked_table()
    item = {
        'PK': 'CUSTOMER#1',
        'SK': 'PROFILE#1',
        'customer_id': '1',
        'profile_data': {'some': 'data'}
    }
    table.put_item(Item=item)


def test_get_customer_handler_has_cors_headers(setup_table_item):
    from src.handlers.get_customer_handler import handler
    result = handler(good_event, Context)
    assert result['headers'] == {'Access-Control-Allow-Origin': '*'}


def test_get_customer_handler_has_json_body(setup_table_item):
    from src.handlers.get_customer_handler import handler
    result = handler(good_event, Context)
    assert isinstance(json.loads(result['body']), dict)


def test_get_customer_handler_returns_schema_validation_error(setup_table_item):
    from src.handlers.get_customer_handler import handler
    result = handler({"bad": "input"}, Context)
    assert result['statusCode'] == 400
    assert 'RequestValidationError' in result['body']

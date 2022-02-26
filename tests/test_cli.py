import pytest

from pgbackup import cli

url = "pgbackup postgres://bob@example.com:5432/db_one"

@pytest.fixture
def parser():
    return cli.create_parser()

def test_parser_without_driver(parser):
    """
    Wihout a specified driver the parser will exit
    """
    with pytest.raises(SystemExit):
        parser.parse_args([url])

def test_parser_with_driver(parser):
    """
    The parser will exit if it receives a driver without a destination
    """
    with pytest.raises(SystemExit):
        parser.parse_args([url, "--driver", "local"])

def test_parser_with_driver_and_destination(parser):
    """
    The parser will not exit if it receives a driver and destinantion
    """
    args = parser.parse_args(["--driver","local",url,'/some/path'])

    assert args.db_url == url
    assert args.driver == 'local'
    assert args.destination == '/some/path'

def test_parser_with_unknown_driver(parser):
    """
    The parser will exit if driver name is unknown
    """

    with pytest.raises(SystemExit):
        parser.parse_args([url,'--driver','GCP','destination'])

def test_parser_with_known_driver(parser):
    """
    The parser won't exit if driver name is unknown
    """
    
    for driver in ['Local','S3','Azure']:
        assert parser.parse_args([url,"--driver",driver,'destination'])


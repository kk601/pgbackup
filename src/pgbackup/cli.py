from argparse import ArgumentParser, Action

known_drivers = ['local','s3','azure']

class DriverAction(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        driver, destination = values
        if driver.lower() not in known_drivers:
            parser.error(f"Unknown driver {driver} available drivers are 'local','S3' & 'Azure'")
        namespace.driver = driver.lower()
        namespace.destination = destination
    

def create_parser():
    parser = ArgumentParser()
    parser.add_argument('url',help='URL of postgreSQL database to backup ')
    parser.add_argument('--driver',
        help='How and where store the backup',
        required=True,
        nargs = 2,
        action=DriverAction
        )
    return parser
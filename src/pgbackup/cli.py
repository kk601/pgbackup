from argparse import ArgumentParser, Action
import sys

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
    parser.add_argument('--driver','-d',
        help='How and where store the backup',
        required=True,
        nargs = 2,
        action=DriverAction,
        metavar=('driver','destination')
        )
    return parser

def main():
    from pgbackup import pgdump, storage

    args = create_parser().parse_args()
    dump = pgdump.dump(args.url)
    if args.driver == 's3':
        import time
        import boto3
        import botocore.exceptions

        client = boto3.client('s3')
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%S")
        file_name = pgdump.dump_file_name(args.url,timestamp)
        print(f"Backing database up to {args.destination} in S3 as {file_name}")

        try:
            storage.s3(client, dump.stdout, args.destination, file_name)
        except(botocore.exceptions.NoCredentialsError) as err:
            print(f"Error: Unable to locate aws credentials")
            sys.exit(1)
        else:
            print(f"Error: {err}")
            sys.exit(1)

    else:
        outfile = open(args.destination,'wb')
        storage.local(dump.stdout, outfile)
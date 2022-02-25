from argparse import ArgumentParser, Action
import sys
import tempfile

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
    parser.add_argument('--connectionstring','-k',help='Connection string for azure storage account') #TODO add option to use azure cli credentials,sas key,just account acces key, Azure AD authentication
    return parser

def main():
    from pgbackup import pgdump, storage
    import time

    args = create_parser().parse_args()
    dump = pgdump.dump(args.url)
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%S")
    file_name = pgdump.dump_file_name(args.url,timestamp)
    if args.driver == 's3':
        import time
        import boto3
        import botocore.exceptions

        client = boto3.client('s3')
        print(f"Backing database up to {args.destination} in S3 as {file_name}")

        try:
            storage.s3(client, dump.stdout, args.destination, file_name)
        except(botocore.exceptions.NoCredentialsError) as err:
            print(f"Error: Unable to locate aws credentials")
            sys.exit(1)
        else:
            print(f"Error: {err}")
            sys.exit(1)

    elif args.driver == 'azure':
        from azure.storage.blob import BlobClient
        if not args.connectionstring:
            connection_string = input("Enter storage account connection string\n").rstrip()
        else:
            connection_string = args.connectionstring
        try:
            blob_client = BlobClient.from_connection_string(connection_string,args.destination,file_name)
            storage.azure(blob_client,dump.stdout.read())
        except Exception as err:
            print(f"Error: {err}")
            sys.exit(1)

    else:
        outfile = open(args.destination,'wb')
        storage.local(dump.stdout, outfile)
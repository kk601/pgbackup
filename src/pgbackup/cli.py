from argparse import ArgumentParser, Action
import sys
import tempfile

known_drivers = ['local','s3','azure']

class DriverAction(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        driver = values
        if driver.lower() not in known_drivers:
            parser.error(f"Unknown driver {driver} available drivers are 'local','S3' & 'Azure'")
        namespace.driver = driver.lower()  

def create_parser():
    parser = ArgumentParser(usage="pgbackup [-h] --driver DRIVER db_url destination [--accesskey ACCESSKEY]")
    parser.add_argument('db_url',help='URL of postgreSQL database to backup ')
    parser.add_argument('--driver','-d',
        help="Available drivers are 'local','S3' & 'Azure'",
        required=True,
        action=DriverAction
        )
    parser.add_argument('destination', help='Location of backup - Local: path_to_file, S3: bucket_name, Azure: container_url')
    parser.add_argument('--accesskey','-k',help='Access key for azure storage account') #TODO Support for SAS auth
    return parser

def main():
    from pgbackup import pgdump, storage
    import time

    args = create_parser().parse_args()
    dump = pgdump.dump(args.db_url)
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%S")
    file_name = pgdump.dump_file_name(args.db_url,timestamp)
    if args.driver == 's3':
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
        import json
        url_split = args.destination.split('/')
        destination_container = url_split[-1]
        storage_account_name = url_split[-2].split('.')[0]
        storage_account_url = f"https://{storage_account_name}"
        print(f"Backing database up to {destination_container} in {storage_account_name} as {file_name}")
        #Get storage account key
        if args.accesskey:
            storage_account_key = args.accesskey
        else:
            #Get storage account key using azure account credentials
            from azure.identity import DefaultAzureCredential
            from azure.mgmt.storage import StorageManagementClient
            from azure.mgmt.subscription import SubscriptionClient
            from azure.core import exceptions

            #Search for storage account in subscriptions
            try:
                credentials = DefaultAzureCredential()
                subscription_client = SubscriptionClient(credentials)
                subscriptions = list(subscription_client.subscriptions.list())
                for subscription in subscriptions:
                    subscription_id = subscription.id.split('/')[-1]   
                    storage_client = StorageManagementClient(credentials, subscription_id)       
                    for item in storage_client.storage_accounts.list():
                        if item.name == storage_account_name:
                            rg = item.id.split('/')[4]
                            storage_client = StorageManagementClient(credentials, subscription_id)
                            storage_account_key = storage_client.storage_accounts.list_keys(rg, item.name).keys[0].value
            except exceptions.ClientAuthenticationError:
                storage_account_key = input("Azure account credentials not found enter storage account access key:\n").rstrip()
            except error as err:
                print(f"Error {err}")
                sys.exit(1)

        try:
            blob_client = BlobClient(url_split[-2],destination_container,file_name,credential=storage_account_key)
            storage.azure(blob_client,dump.stdout.read())
        except Exception as err:
            print(f"Error: {err}")
            sys.exit(1)

    elif args.driver == 'local':
        outfile = open(args.destination,'wb')
        storage.local(dump.stdout, outfile)
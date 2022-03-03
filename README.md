# Pgbackup

Extended version of guided project from [Python 3 Scripting for System Administrators](https://https://acloudguru.com/course/python-3-scripting-for-system-administrators) course.

CLI tool for postgreSQL database backup locally, to AWS S3(Not tested) or Azure blob storage.
Requires pg_dump utility and aws cli for remote backups.

---
 ## Preparing the development environment
1. Ensure ```pip``` and ```pipenv``` are installed
2. Clone repository: ```git clone https://github.com/kk601/pgbackup```
3. ```cd``` into the repository
4. Fetch development dependencies: ```make install```
5. Activate virtualenv: ```pipenv shell``` 
---
## Try tool in docker container(local driver support only)
Docker repository - https://hub.docker.com/r/kk601/pgbackup
```
$ docker run --name pgbackup -it kk601/pgbackup:1.1.0base 
$ pgbackup --driver local postgres://root:Password1234@localhost:5432/test_db dump.sql
```
---
## Usage
Pass in a driver postgres db url and destination
### Local example w/ local path
```
pgbackup --driver local postgres://bob@example.com:5432/db_one /var/local/db_one/backups/dump.sql
```
### Remote example w/ S3 - authentication with aws cli
```
pgbackup --driver s3 postgres://bob@example.com:5432/db_one bucket1 
```
### Remote example w/ Azure - authentication with account credentials(Environment variables,managed identity, Azure CLI and Azure Powershell supported) or storage access key
```
pgbackup --driver azure postgres://bob@example.com:5432/db_one https://storageaccount.blob.core.windows.net/container
```
### Remote example w/ Azure - authentication with SAS token
```
pgbackup --driver azure postgres://bob@example.com:5432/db_one 'https://storageaccount.blob.core.windows.net/container?sp=c&st=2022-02-31T21:37:00Z&se=2022-03-00T25:61::Z&sip=172.10.0.0&spr=https&sv=2020-08-04&sr=c&sig=#fdY4NWafJpkxEzFXb%#FyQisfbCrnQfsf#buaAYH%2FbUmhc%3a#'
```
---
## Running tests
### Run tests locally using ```make``` if virtualenv is active:
```
make
```
### If virtualenv isn't active then use:
```
pipenv run make
```




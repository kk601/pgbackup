# Pgbackup

Guided project from [Python 3 Scripting for System Administrators](https://https://acloudguru.com/course/python-3-scripting-for-system-administrators) course.

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
## Usage
Pass in a full database URL, the storage driver and the destination
### Local example w/ local path
```
pgbackup postgres://bob@example.com:5432/db_one --driver local /var/local/db_one/backups/dump.sql
```
### Remote example w/ S3
```
pgbackup postgres://bob@example.com:5432/db_one  --driver s3 bucket1 
```
### Remote example w/ Azure
```
pgbackup postgres://bob@example.com:5432/db_one  --driver s3 bucket1 
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




# Pgbackup

Guided project from [Python 3 Scripting for System Administrators](https://https://acloudguru.com/course/python-3-scripting-for-system-administrators) course.

CLI for backup up remote postgreSQL database either locally, to AWS S3 or to Azure storage.

---
 ## Preparing the Development
1. Ensure ```pip``` and ```pipenv``` are installed
2. Clone repository:``` git clone https://github.com/kk601/pgbackup```

3. ```cd``` into the repository
4. Fetch development dependencies: ```make install```
5. Activate virtualenv: ```pipenv shell``` 

---
 ## Usage
Pass in a full database URL, the storage driver, and the destination
### Local example w/ local path
```
pgbackup postgres://bob@example.com:5432/db_one --driver local /var/local/db_one/backups/dump.sql
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




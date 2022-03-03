#!/bin/bash

service postgresql start
psql -c "create database $POSTGRES_DB"
psql -c "CREATE ROLE root WITH LOGIN SUPERUSER PASSWORD 'Password1234'"
psql $POSTGRES_DB < sample_db.sql
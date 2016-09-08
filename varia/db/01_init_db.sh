#!/bin/bash

ADMIN="stefan"
ADMINPWD="ziegler12"
USER="mspublic"
USERPWD="mspublic"

DB_NAME="veriso_nplso"
PG_VERSION="9.3"

echo "Create database user"
sudo -u postgres psql -d postgres -c "CREATE ROLE $ADMIN CREATEDB LOGIN PASSWORD '$ADMINPWD';"
sudo -u postgres psql -d postgres -c "CREATE ROLE $USER LOGIN PASSWORD '$USERPWD';"

echo "Delete database: $DB_NAME"
sudo -u postgres dropdb ${DB_NAME}

echo "Create database: $DB_NAME"
sudo -u postgres createdb --owner ${ADMIN} ${DB_NAME}

echo "Load postgis"
sudo -u postgres psql -d ${DB_NAME} -c "CREATE EXTENSION postgis;"

echo "Grant tables to..."
sudo -u postgres psql -d ${DB_NAME} -c "GRANT ALL ON SCHEMA public TO $ADMIN;"
sudo -u postgres psql -d ${DB_NAME} -c "ALTER TABLE geometry_columns OWNER TO $ADMIN;"
sudo -u postgres psql -d ${DB_NAME} -c "GRANT ALL ON geometry_columns TO $ADMIN;"
sudo -u postgres psql -d ${DB_NAME} -c "GRANT ALL ON spatial_ref_sys TO $ADMIN;"
sudo -u postgres psql -d ${DB_NAME} -c "GRANT ALL ON geography_columns TO $ADMIN;"
sudo -u postgres psql -d ${DB_NAME} -c "GRANT ALL ON raster_columns TO $ADMIN;"
sudo -u postgres psql -d ${DB_NAME} -c "GRANT ALL ON raster_overviews TO $ADMIN;"

sudo -u postgres psql -d ${DB_NAME} -c "GRANT SELECT ON geometry_columns TO $USER;"
sudo -u postgres psql -d ${DB_NAME} -c "GRANT SELECT ON spatial_ref_sys TO $USER;"
sudo -u postgres psql -d ${DB_NAME} -c "GRANT SELECT ON geography_columns TO $USER;"
sudo -u postgres psql -d ${DB_NAME} -c "GRANT SELECT ON raster_columns TO $USER;"


